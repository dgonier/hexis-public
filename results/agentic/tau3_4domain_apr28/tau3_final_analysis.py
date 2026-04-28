"""Canonical 3-judge analysis script for tau3 4-domain bench (Apr 28 result).

Inputs:
  results/tau3_full_asym_1777300323.jsonl      — bench output
  results/tau3_full_asym_1777300323.audit.jsonl — Sonnet audit on disputed trials
  results/tau3_full_asym_1777300323.opus.jsonl  — Opus tiebreak where Sonnet disagrees with hard

Final verdict per trial:
  - hard==soft (undisputed Haiku): trust hard_pass
  - hard!=soft + Sonnet agrees with hard: trust hard_pass
  - hard!=soft + Sonnet disagrees: 3-judge majority of (hard, sonnet, opus)

Outputs:
  - Per-domain pass-rate table on full panel and on filtered panel (excl airline t1, t3)
  - McNemar paired tests for C3 vs baseline and C5 vs baseline on both panels

The airline t1, t3 exclusion is documented as judge-variance handling — see
appendix Tau3 Benchmark Protocol section in the paper.
"""
import json
import sys
from collections import defaultdict
from math import comb

BENCH = 'results/tau3_full_asym_1777300323.jsonl'
AUDIT = 'results/tau3_full_asym_1777300323.audit.jsonl'
OPUS = 'results/tau3_full_asym_1777300323.opus.jsonl'

INFRA = ['RateLimit','Throttl','Too many tokens','BedrockException','bedrock error',
         '500 Internal','502','503','504','TimeoutError','Connection']

def is_infra(r):
    e = str(r.get('error') or '') + ' ' + str(r.get('soft_reason') or '')
    return any(p in e for p in INFRA)

def run_id_of(r):
    return f'{r.get("domain")}_t{r.get("task_id")}_{r.get("config")}_trial{r.get("trial")}'

def load_audits():
    audit_by_rid = {}
    for line in open(AUDIT):
        r = json.loads(line)
        audit_by_rid[r['run_id']] = r
    opus_by_rid = {}
    for line in open(OPUS):
        r = json.loads(line)
        opus_by_rid[r['run_id']] = r
    return audit_by_rid, opus_by_rid

def final_verdict(r, audit_by_rid, opus_by_rid):
    rid = run_id_of(r)
    h = bool(r.get('hard_pass'))
    s = r.get('soft_pass')
    if h == s:
        return h
    sonnet_rec = audit_by_rid.get(rid)
    if not sonnet_rec:
        return h  # missing audit fallback (shouldn't happen)
    sv = sonnet_rec.get('sonnet_verdict')
    sonnet_pass = (sv == 'PASS')
    opus_rec = opus_by_rid.get(rid)
    if opus_rec:
        ov = opus_rec.get('opus_verdict')
        opus_pass = (ov == 'PASS')
        return sum([h, sonnet_pass, opus_pass]) >= 2
    return h  # Sonnet agreed with hard → no Opus needed

def load_records():
    audit_by_rid, opus_by_rid = load_audits()
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

def tally(records):
    t = defaultdict(lambda: defaultdict(lambda: [0,0]))
    for r in records:
        t[r['domain']][r['config']][0] += int(r['pass'])
        t[r['domain']][r['config']][1] += 1
    return t

def print_table(records, title):
    t = tally(records)
    print('=' * 75)
    print(title)
    print('=' * 75)
    print(f'{"domain":20s} {"baseline":>15s} {"C3_teacher":>15s} {"C5_t+verify":>15s}')
    overall = defaultdict(lambda: [0,0])
    for d in sorted(t):
        line = f'{d:20s} '
        for c in ['baseline','C3_teacher_only','C5_teacher_plus_verify']:
            p, n = t[d][c]
            pct = 100*p/n if n else 0
            line += f' {p:>3}/{n:<3} ({pct:>4.1f}%) '
            overall[c][0] += p
            overall[c][1] += n
        print(line)
    print('-' * 75)
    line = f'{"OVERALL":20s} '
    for c in ['baseline','C3_teacher_only','C5_teacher_plus_verify']:
        p, n = overall[c]
        line += f' {p:>3}/{n:<3} ({100*p/n:>4.1f}%) '
    print(line)
    print()

def by_pair(records, c1, c2):
    keyed = defaultdict(dict)
    for r in records:
        if r['config'] not in (c1, c2): continue
        k = (r['domain'], r['task_id'], r['trial'])
        keyed[k][r['config']] = r['pass']
    return [(v[c1], v[c2]) for v in keyed.values() if c1 in v and c2 in v]

def mcnemar(pairs):
    b = sum(1 for a,c in pairs if a and not c)
    c = sum(1 for a,d in pairs if not a and d)
    n = b + c
    if n == 0: return None
    k = min(b, c)
    p1 = sum(comb(n, i) for i in range(k+1)) / (2**n)
    return {'n_pairs': len(pairs), 'b': b, 'c': c, 'n_disc': n, 'delta': c-b,
            'p_exact_two_sided': min(1.0, 2*p1)}

def print_mcnemar(records, title):
    print('=' * 75)
    print(title)
    print('=' * 75)
    for c2 in ['C3_teacher_only', 'C5_teacher_plus_verify']:
        pairs = by_pair(records, 'baseline', c2)
        res = mcnemar(pairs)
        if res:
            print(f'  baseline vs {c2}:')
            print(f'    pairs={res["n_pairs"]}  baseline_only={res["b"]}  '
                  f'arm_only={res["c"]}  disc={res["n_disc"]}  '
                  f'delta=+{res["delta"]}  p={res["p_exact_two_sided"]:.4f}')
    print()

if __name__ == '__main__':
    records = load_records()
    print_table(records, '3-JUDGE AUDITED RESULT (full panel)')
    print_mcnemar(records, 'McNEMAR PAIRED TESTS (full panel)')

    filtered = [r for r in records if not (r['domain']=='airline' and r['task_id'] in (1,3))]
    print_table(filtered, '3-JUDGE AUDITED RESULT (excl airline t1, t3 — judge variance)')
    print_mcnemar(filtered, 'McNEMAR PAIRED TESTS (excl airline t1, t3)')
