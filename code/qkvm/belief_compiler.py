"""
HEXIS v23: Belief Compiler + M-as-Curator.

Processes beliefs through the base model with M-modulated Q,
compresses the resulting hidden states into per-layer Q and V
modulation matrices. These compiled modulations carry belief
disposition + content without beliefs being in the main context.

The model sees: [system + question] (no beliefs)
M compiled from: [beliefs] (processed once, cached)

Key insight: V-modulation is ESSENTIAL here because there are
no belief tokens in the KV cache. V-modulation is the only
channel for belief content to enter the value stream.

Usage:
    compiler = BeliefCompiler(base_model, tokenizer, phi_writer,
                               m_read_head, btm_template, patched_layers)
    compiled = compiler.compile(topic, side="pro")
    text = compiler.generate(question_prompt, compiled)
"""

import torch
import torch.nn as nn


class CompiledMState:
    """Per-layer compiled Q and V modulation from belief processing."""

    def __init__(self):
        self.layers = {}  # {layer_idx: (M_A, M_B, E_A, E_B, q_scale, v_scale)}

    def add_layer(self, layer_idx, M_A, M_B, E_A, E_B, q_scale=1.0, v_scale=1.0):
        self.layers[layer_idx] = (M_A, M_B, E_A, E_B, q_scale, v_scale)

    def get_layer(self, layer_idx):
        return self.layers.get(layer_idx)


class BeliefCompiler:
    """Compile beliefs into M/E modulation via forward pass + compression."""

    def __init__(self, base_model, tokenizer, phi_writer, m_read_head,
                 btm_template, patched_layers, d_node=128, rank=16):
        self.base_model = base_model
        self.tokenizer = tokenizer
        self.phi_writer = phi_writer
        self.m_read_head = m_read_head
        self.btm_template = btm_template
        self.patched_layers = patched_layers
        self.d_node = d_node
        self.rank = rank
        self.device = next(base_model.parameters()).device
        self.d_model = next(base_model.parameters()).shape[-1] if next(base_model.parameters()).dim() > 1 else 2560

        # Get d_model from config
        config = base_model.config
        if hasattr(config, "text_config"):
            config = config.text_config
        self.d_model = config.hidden_size

        # V-modulation projections (learnable, initialized from M projections)
        # These project pooled hidden states to E_A, E_B (value modulation)
        # For now, use the same architecture as M projections
        # In a trained version, these would be separate learned projections
        self.v_proj_A = nn.ModuleList([
            nn.Linear(self.d_model, self.d_model * rank)
            for _ in range(len(patched_layers))
        ]).to(self.device)
        self.v_proj_B = nn.ModuleList([
            nn.Linear(self.d_model, self.d_model * rank)
            for _ in range(len(patched_layers))
        ]).to(self.device)

        # Initialize V projections with small random weights
        for proj in list(self.v_proj_A) + list(self.v_proj_B):
            nn.init.normal_(proj.weight, std=0.01)

    def compile_from_hidden_states(self, belief_text):
        """Compile beliefs by running through base model and extracting hidden states.

        Returns CompiledMState with Q-modulation (from trained M) and
        V-modulation (from hidden state compression).
        """
        # Tokenize beliefs
        enc = self.tokenizer(belief_text, return_tensors="pt",
                             truncation=True, max_length=512).to(self.device)

        # Forward pass through base model — get hidden states at each layer
        with torch.no_grad():
            outputs = self.base_model(input_ids=enc["input_ids"],
                                       output_hidden_states=True)

        compiled = CompiledMState()

        for l_idx, layer_num in enumerate(self.patched_layers):
            # Hidden states at this layer for belief tokens
            h = outputs.hidden_states[layer_num + 1]  # +1 because index 0 is embeddings
            # Pool across belief positions (mean pool)
            h_pooled = h.mean(dim=1).squeeze(0).float()  # (d_model,)

            # Q-modulation: use the trained M from m_read_head
            # Get M_A, M_B from the existing trained M-state
            # (These are the same M matrices that work in the current architecture)
            M_A, M_B, mod_scale = self.m_read_head.m_proj_A[l_idx], self.m_read_head.m_proj_B[l_idx], self.m_read_head.mod_scales[l_idx]

            # For Q-mod, we use the trained M_A/M_B directly from m_read_head
            # The existing M-state is already a good Q-modulation

            # V-modulation: compress hidden states into E_A, E_B
            # This is the NEW channel — uses the pooled hidden state from belief processing
            with torch.no_grad():
                E_A_flat = torch.tanh(self.v_proj_A[l_idx](h_pooled))
                E_B_flat = torch.tanh(self.v_proj_B[l_idx](h_pooled))
                E_A = E_A_flat.reshape(self.d_model, self.rank)
                E_B = E_B_flat.reshape(self.d_model, self.rank)

                # Normalize to prevent explosion
                E_A = E_A * (1.5 / (E_A.norm() + 1e-8))
                E_B = E_B * (1.5 / (E_B.norm() + 1e-8))

            compiled.add_layer(layer_num, M_A.weight.data, M_B.weight.data,
                              E_A, E_B,
                              q_scale=mod_scale.item(),
                              v_scale=0.5)  # conservative V scale

        return compiled

    def compile_from_m_state(self, topic, side="pro"):
        """Compile using the existing M-state pipeline (phi + btm + m_read_head).

        This produces the SAME M_A/M_B as the current architecture,
        plus adds V-modulation from hidden state compression.
        """
        from qkvm.belief_tree_memory import build_topic_tree, get_pro_con_node_ids
        from qkvm.jeffrey_update import initialize_credences_from_zero_points

        # Build BTM and get M-state (same as current pipeline)
        tree = build_topic_tree(topic)
        pro_ids, con_ids = get_pro_con_node_ids(tree, n_pro=len(topic["experiences_A"]))
        btm = type(self.btm_template)(d_node=self.d_node, d_edge=64, n_message_passes=2)
        btm.edge_embedding = self.btm_template.edge_embedding
        btm.message_fn = self.btm_template.message_fn
        btm.update_fn = self.btm_template.update_fn
        btm.node_init_proj = self.btm_template.node_init_proj

        for nid, node in tree.nodes.items():
            enc = self.tokenizer(node.statement[:200], return_tensors="pt",
                                truncation=True, max_length=128)
            with torch.no_grad():
                out = self.base_model(input_ids=enc["input_ids"].to(self.device),
                                       output_hidden_states=True)
            h = out.hidden_states[-1].mean(1).float()
            btm._embeddings[nid] = btm.node_init_proj(h).squeeze(0).detach()
        btm.propagate(tree)

        exp_list = topic["experiences_A"] if side == "pro" else topic["experiences_B"]
        ev_ids = (pro_ids if side == "pro" else con_ids)[1:]
        persp_ids = pro_ids if side == "pro" else con_ids
        for exp, nid in zip(exp_list, ev_ids):
            enc = self.tokenizer(exp[:200], return_tensors="pt",
                                truncation=True, max_length=128)
            with torch.no_grad():
                out = self.base_model(input_ids=enc["input_ids"].to(self.device),
                                       output_hidden_states=True)
            h_exp = out.hidden_states[-1].mean(1).float().squeeze(0)
            with torch.no_grad():
                delta = self.phi_writer(h_exp, btm.get_embedding(nid))
            btm.set_embedding(nid, (0.95 * btm.get_embedding(nid) + 0.1 * delta).detach())
        btm.propagate(tree)
        for pid in persp_ids[1:]:
            tree.nodes[pid].credence = 0.80
        embed_s, cred_s = btm.get_perspective_embeddings(persp_ids, tree)
        with torch.no_grad():
            m_layers = self.m_read_head(embed_s, cred_s)

        # Now also get hidden states from belief text for V-modulation
        belief_text = topic.get(f"stance_{'A' if side == 'pro' else 'B'}", topic["probe"])
        for exp in exp_list:
            belief_text += " " + exp

        enc = self.tokenizer(belief_text[:500], return_tensors="pt",
                             truncation=True, max_length=256).to(self.device)
        with torch.no_grad():
            outputs = self.base_model(input_ids=enc["input_ids"],
                                       output_hidden_states=True)

        compiled = CompiledMState()

        for l_idx, layer_num in enumerate(self.patched_layers):
            M_A, M_B, mod_scale = m_layers[l_idx]

            # V-modulation from hidden states
            h = outputs.hidden_states[layer_num + 1]
            h_pooled = h.mean(dim=1).squeeze(0).float()

            with torch.no_grad():
                E_A_flat = torch.tanh(self.v_proj_A[l_idx](h_pooled))
                E_B_flat = torch.tanh(self.v_proj_B[l_idx](h_pooled))
                E_A = E_A_flat.reshape(self.d_model, self.rank)
                E_B = E_B_flat.reshape(self.d_model, self.rank)
                E_A = E_A * (1.5 / (E_A.norm() + 1e-8))
                E_B = E_B * (1.5 / (E_B.norm() + 1e-8))

            compiled.add_layer(layer_num, M_A, M_B, E_A, E_B,
                              q_scale=mod_scale.item(),
                              v_scale=0.3)  # V scale lower than Q

        return compiled

    def install_compiled_hooks(self, compiled):
        """Install Q+V modulation hooks from compiled state."""
        handles = []

        for layer_num, (M_A, M_B, E_A, E_B, q_scale, v_scale) in compiled.layers.items():
            l_idx = self.patched_layers.index(layer_num) if layer_num in self.patched_layers else -1
            if l_idx < 0:
                continue

            def make_qv_hook(ma, mb, ea, eb, qs, vs):
                def hook(module, args, kwargs=None):
                    x = args[0] if args else kwargs.get("hidden_states")
                    if x is None: return args, kwargs
                    dev, dt = x.device, x.dtype

                    # Q-modulation: x' = x + q_scale * (x @ M_A) @ M_B^T
                    q_mod = torch.matmul(torch.matmul(x, ma.to(dev, dt)), mb.to(dev, dt).T)

                    # V-modulation: x' += v_scale * (x @ E_A) @ E_B^T
                    v_mod = torch.matmul(torch.matmul(x, ea.to(dev, dt)), eb.to(dev, dt).T)

                    x_mod = x + qs * q_mod + vs * v_mod

                    if args: return (x_mod,) + args[1:], kwargs
                    kw = dict(kwargs) if kwargs else {}; kw["hidden_states"] = x_mod
                    return args, kw
                return hook

            handles.append(
                self.base_model.model.layers[layer_num].register_forward_pre_hook(
                    make_qv_hook(M_A, M_B, E_A, E_B, q_scale, v_scale),
                    with_kwargs=True))

        return handles

    def generate(self, prompt, compiled, max_new=200):
        """Generate with compiled Q+V modulation, no beliefs in prompt."""
        hooks = self.install_compiled_hooks(compiled)
        enc = self.tokenizer(prompt, return_tensors="pt",
                             truncation=True, max_length=3500).to(self.device)
        with torch.no_grad():
            out = self.base_model.generate(
                enc["input_ids"], max_new_tokens=max_new, do_sample=False,
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id)
        for h in hooks: h.remove()
        text = self.tokenizer.decode(out[0, enc["input_ids"].shape[1]:],
                                      skip_special_tokens=True)
        for marker in ["\nuser\n", "\nUser:", "\nassistant\n"]:
            if marker in text: text = text[:text.index(marker)]
        return text.strip()
