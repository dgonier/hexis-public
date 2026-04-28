"""Build the headline tau3 figure for the paper.

Produces a per-domain grouped bar chart (baseline / C3 / C5) plus an Overall column,
with Wilson 95% CIs as error bars and a McNemar p-value annotation on the C5 vs
baseline comparison. Saves as PDF + PNG to paper/figures/.
"""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from math import comb, sqrt

BENCH = '/home/dgonier/experiments/results/tau3_full_asym_1777300323.jsonl'
AUDIT = '/home/dgonier/experiments/results/tau3_full_asym_1777300323.audit.jsonl'
OPUS = '/home/dgonier/experiments/results/tau3_full_asym_1777300323.opus.jsonl'

OUT_DIR = '/home/dgonier/debaterhub/hexis/paper/figures'
OUT_BASE = 'fig-tau3-results'

INFRA = ['RateLimit','Throttl','Too many tokens','BedrockException','bedrock error',
         '500 Internal','502','503','504','TimeoutError','Connection']

def is_infra(r):
    e = str(r.get('error') or '') + ' ' + str(r.get('soft_reason') or '')
    return any(p in e for p in INFRA)

def run_id_of(r):
    return f'{r.get("domain")}_t{r.get("task_id")}_{r.get("config")}_trial{r.get("trial")}'

def final_verdict(r, audit_by_rid, opus_by_rid):
    rid = run_id_of(r)
    h = bool(r.get('hard_pass'))
    s = r.get('soft_pass')
    if h == s:
        return h
    sa = audit_by_rid.get(rid)
    if not sa:
        return h
    sp = (sa.get('sonnet_verdict') == 'PASS')
    op = opus_by_rid.get(rid)
    if op:
        opass = (op.get('opus_verdict') == 'PASS')
        return sum([h, sp, opass]) >= 2
    return h

def load_records():
    audit_by_rid = {json.loads(l)['run_id']: json.loads(l) for l in open(AUDIT)}
    opus_by_rid = {json.loads(l)['run_id']: json.loads(l) for l in open(OPUS)}
    records = []
    for line in open(BENCH):
        r = json.loads(line)
        if r.get('error'): continue
        if is_infra(r): continue
        v = final_verdict(r, audit_by_rid, opus_by_rid)
        records.append({
            'rid': run_id_of(r),
            'domain': r.get('domain'),
            'config': r.get('config'),
            'task_id': r.get('task_id'),
            'trial': r.get('trial'),
            'pass': v,
        })
    return records

def balance_to_5(records):
    """Per (domain, task_id), keep first 5 trials per arm only if all 3 arms have >=5."""
    by_cell = defaultdict(lambda: defaultdict(list))
    for r in records:
        by_cell[(r['domain'], r['task_id'])][r['config']].append(r)
    ARMS = ['baseline','C3_teacher_only','C5_teacher_plus_verify']
    out = []
    kept_tasks = []
    for (d, t), arms in by_cell.items():
        if all(len(arms.get(a, [])) >= 5 for a in ARMS):
            kept_tasks.append((d, t))
            for a in ARMS:
                trials = sorted(arms[a], key=lambda x: x['trial'])[:5]
                out.extend(trials)
    return out, kept_tasks

def wilson(p, n, z=1.96):
    if n == 0:
        return 0, 0
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    half = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
    return max(0, center - half), min(1, center + half)

def by_pair(records, c1, c2):
    keyed = defaultdict(dict)
    for r in records:
        if r['config'] not in (c1, c2): continue
        k = (r['domain'], r['task_id'], r['trial'])
        keyed[k][r['config']] = r['pass']
    return [(v[c1], v[c2]) for v in keyed.values() if c1 in v and c2 in v]

def mcnemar(pairs):
    b = sum(1 for a, c in pairs if a and not c)
    c = sum(1 for a, d in pairs if not a and d)
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    p1 = sum(comb(n, i) for i in range(k+1)) / (2**n)
    return {'n_pairs': len(pairs), 'b': b, 'c': c, 'n_disc': n, 'delta': c-b,
            'p_exact': min(1.0, 2*p1)}

def make_figure(records, kept_tasks, exclude_t1t3=False, suffix=''):
    if exclude_t1t3:
        records = [r for r in records if not (r['domain']=='airline' and r['task_id'] in (1,3))]

    DOMAINS = ['airline', 'retail', 'banking_knowledge', 'telecom']
    DOMAIN_LABELS = {'airline':'Airline', 'retail':'Retail',
                     'banking_knowledge':'Banking', 'telecom':'Telecom'}
    ARMS = ['baseline', 'C3_teacher_only', 'C5_teacher_plus_verify']
    ARM_LABELS = ['Baseline', r'$C_3$ Teacher Only', r'$C_5$ Teacher + d$^*$']
    ARM_COLORS = ['#888888', '#4477aa', '#cc6677']

    # Tally per (domain, arm)
    domain_tally = {d: {a: [0,0] for a in ARMS} for d in DOMAINS}
    for r in records:
        d, a = r['domain'], r['config']
        if d in domain_tally and a in domain_tally[d]:
            domain_tally[d][a][0] += int(r['pass'])
            domain_tally[d][a][1] += 1

    # Overall
    overall = {a: [0,0] for a in ARMS}
    for r in records:
        if r['config'] in overall:
            overall[r['config']][0] += int(r['pass'])
            overall[r['config']][1] += 1

    # Plot
    fig, ax = plt.subplots(figsize=(8.5, 4.0))
    n_groups = len(DOMAINS) + 1  # +1 for overall
    x = np.arange(n_groups)
    width = 0.27

    rates_per_arm = {a: [] for a in ARMS}
    err_lo_per_arm = {a: [] for a in ARMS}
    err_hi_per_arm = {a: [] for a in ARMS}
    n_per_arm_per_group = {a: [] for a in ARMS}
    for d in DOMAINS:
        for a in ARMS:
            p, n = domain_tally[d][a]
            rate = p/n if n else 0
            lo, hi = wilson(rate, n)
            rates_per_arm[a].append(rate*100)
            err_lo_per_arm[a].append((rate-lo)*100)
            err_hi_per_arm[a].append((hi-rate)*100)
            n_per_arm_per_group[a].append(n)
    # Overall column
    for a in ARMS:
        p, n = overall[a]
        rate = p/n if n else 0
        lo, hi = wilson(rate, n)
        rates_per_arm[a].append(rate*100)
        err_lo_per_arm[a].append((rate-lo)*100)
        err_hi_per_arm[a].append((hi-rate)*100)
        n_per_arm_per_group[a].append(n)

    bars = []
    for i, (a, label, color) in enumerate(zip(ARMS, ARM_LABELS, ARM_COLORS)):
        offset = (i - 1) * width
        b = ax.bar(x + offset, rates_per_arm[a], width, label=label, color=color,
                   edgecolor='black', linewidth=0.7)
        ax.errorbar(x + offset, rates_per_arm[a],
                    yerr=[err_lo_per_arm[a], err_hi_per_arm[a]],
                    fmt='none', ecolor='black', capsize=3, linewidth=0.7)
        bars.append(b)
        # n labels under x-axis
        for xi, n in zip(x + offset, n_per_arm_per_group[a]):
            ax.text(xi, -7, f'n={n}', ha='center', va='top', fontsize=7, color='#444')

    # McNemar p annotations on overall column for C5 vs baseline
    overall_pairs = by_pair(records, 'baseline', 'C5_teacher_plus_verify')
    res = mcnemar(overall_pairs)
    if res:
        # Star annotation
        p = res['p_exact']
        if p < 0.001: stars = '***'
        elif p < 0.01: stars = '**'
        elif p < 0.05: stars = '*'
        elif p < 0.1: stars = '.'
        else: stars = 'n.s.'
        # Bracket from baseline (offset -width) to C5 (offset +width) at overall column
        x_overall = n_groups - 1
        x1, x2 = x_overall - width, x_overall + width
        y_top = max(rates_per_arm['baseline'][-1], rates_per_arm['C5_teacher_plus_verify'][-1]) + 8
        ax.plot([x1, x1, x2, x2], [y_top-2, y_top, y_top, y_top-2], 'k-', linewidth=0.8)
        ax.text((x1+x2)/2, y_top + 1, f'{stars} (p={p:.3f})', ha='center', va='bottom', fontsize=9)

    # Cosmetics
    ax.set_xticks(x)
    xtick_labels = [DOMAIN_LABELS[d] for d in DOMAINS] + ['Overall']
    ax.set_xticklabels(xtick_labels, fontsize=10)
    ax.set_ylabel('Audited Pass Rate (\\%)', fontsize=10)
    ax.set_ylim(-15, 110)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels([f'{y}' for y in [0, 20, 40, 60, 80, 100]])
    ax.legend(loc='upper left', fontsize=9, frameon=False, ncol=3, bbox_to_anchor=(0.0, 1.10))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axhline(0, color='k', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle=':', alpha=0.5)

    title = r'$\tau^3$-bench audited pass rates (3-judge majority on disputed trials)'
    if exclude_t1t3:
        title += '\n[excl.\\ airline t1, t3 — judge variance]'
    ax.set_title(title, fontsize=10, pad=18)

    plt.tight_layout()
    out_png = f'{OUT_DIR}/{OUT_BASE}{suffix}.png'
    out_pdf = f'{OUT_DIR}/{OUT_BASE}{suffix}.pdf'
    plt.savefig(out_png, dpi=200, bbox_inches='tight')
    plt.savefig(out_pdf, bbox_inches='tight')
    plt.close()
    print(f'wrote {out_png} and {out_pdf}')

if __name__ == '__main__':
    records = load_records()
    print(f'Loaded {len(records)} clean records')

    # Balanced primary panel
    balanced, kept = balance_to_5(records)
    print(f'Balanced 5x5x5 panel: {len(balanced)} records across {len(kept)} tasks')

    # Figure 1: balanced (primary)
    make_figure(balanced, kept, exclude_t1t3=False, suffix='-balanced')
    # Figure 2: balanced + excl t1,t3
    make_figure(balanced, kept, exclude_t1t3=True, suffix='-balanced-no-t1t3')
    # Figure 3: full panel for sensitivity
    make_figure(records, None, exclude_t1t3=False, suffix='-full-panel')
    # Figure 4: full + excl t1,t3
    make_figure(records, None, exclude_t1t3=True, suffix='-full-no-t1t3')
