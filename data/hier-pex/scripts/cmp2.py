"""Compare two PEX netlists of a labelled tile (flat reference first): per-net total capacitance
(from the header) and per-pair coupling capacitance summed from the C elements.
  cmp2.py flat.pex.spice windowed.pex.spice [--json out.json]"""
import json
import re
import statistics
import sys
from collections import defaultdict


def load(path):
    totals, caps = {}, defaultdict(float)
    lines = open(path).read().splitlines()
    for l in lines:
        if l.startswith("* total capacitance per net"):
            totals = {a.split()[0]: float(a.split()[1]) for a in l.split(":", 1)[1].split(",")}

    def net_of(node):                  # <net> or <net>_<k> (a node of its R network)
        n = node
        while n not in totals:
            m = re.match(r"(.+)_\d+$", n)
            if not m:
                return node
            n = m.group(1)
        return n

    for l in lines:
        if l.startswith("C"):
            t = l.split()
            a, b = net_of(t[1]), net_of(t[2])
            if a != b:
                caps[tuple(sorted((a, b)))] += float(t[3].rstrip("f"))
    return totals, caps


(ta, ca), (tb, cb) = load(sys.argv[1]), load(sys.argv[2])
lab = lambda n: not n.startswith("net")
sup = lambda n: n.startswith(("VDD", "VSS"))
out = {}

e_lab = {n: (tb[n] / ta[n] - 1) * 100 for n in ta if lab(n) and n in tb and not n.startswith("VSS")}
ua = sorted(v for n, v in ta.items() if not lab(n))
ub = sorted(v for n, v in tb.items() if not lab(n))
e_unl = [(y / x - 1) * 100 for x, y in zip(ua, ub)]
allerr = list(e_lab.values()) + e_unl
worst = sorted(e_lab.items(), key=lambda x: -abs(x[1]))[:6]
print(f"total C, signal nets + VDD ({len(allerr)}): mean |err| {statistics.mean(map(abs, allerr)):.2f} %, "
      f"max {max(map(abs, allerr)):.2f} %, mean {statistics.mean(allerr):+.2f} %")
print("  worst labelled:", ", ".join(f"{n} {e:+.2f} %" for n, e in worst))
if e_unl:
    print(f"  unlabelled (internal Q / QB ..., sorted pairs, {len(e_unl)}): mean |err| "
          f"{statistics.mean(map(abs, e_unl)):.2f} %, max {max(map(abs, e_unl)):.2f} %")
vss = [(tb[n] / ta[n] - 1) * 100 for n in ta if n.startswith("VSS") and n in tb]
if vss:
    print(f"  VSS rails (not in the above): {', '.join(f'{e:+.1f} %' for e in vss)}")
out["total"] = {"n": len(allerr), "mean_abs": statistics.mean(map(abs, allerr)),
                "max_abs": max(map(abs, allerr)), "mean": statistics.mean(allerr),
                "unlabelled_max_abs": max(map(abs, e_unl)) if e_unl else None, "labelled": e_lab}
for g in ("WL", "BL", "BLB", "XB", "P", "VDD"):
    e = [v for n, v in e_lab.items() if n.split("_")[0] == g]
    if e:
        print(f"  {g:4s} total C: n={len(e):3d} mean {statistics.mean(e):+.2f} %, max |err| {max(map(abs, e)):.2f} %")

print("coupling C between labelled nets, pairs >= 1 % of either net's total (flat):")
rows = defaultdict(list)
for (a, b), c in ca.items():
    if not (lab(a) and lab(b)) or (sup(a) and sup(b)):
        continue
    if c < 0.01 * min(ta.get(a, 1e9), ta.get(b, 1e9)):
        continue
    rows[tuple(sorted((a.split("_")[0], b.split("_")[0])))].append((c, cb.get((a, b), 0.0), a, b))
out["coupling"] = {}
for k, v in sorted(rows.items(), key=lambda kv: -sum(x[0] for x in kv[1])):
    e = [(w / c - 1) * 100 for c, w, _, _ in v]
    wc = max(v, key=lambda x: abs(x[1] / x[0] - 1))
    fs, ws = sum(x[0] for x in v), sum(x[1] for x in v)
    print(f"  {k[0]:4s}-{k[1]:4s} n={len(v):3d}  flat {fs:8.4f} fF  windowed {ws:8.4f} fF ({(ws / fs - 1) * 100:+6.2f} %)"
          f"  per pair mean |err| {statistics.mean(map(abs, e)):5.2f} %, worst {wc[2]}-{wc[3]} {wc[0]:.4f} -> {wc[1]:.4f} fF")
    out["coupling"]["-".join(k)] = {"n": len(v), "flat_fF": fs, "win_fF": ws, "sum_err": (ws / fs - 1) * 100,
                                     "pair_mean_abs": statistics.mean(map(abs, e)),
                                     "pair_max_abs": max(map(abs, e))}
for g in ("P", "XB"):
    cells = {tuple(map(int, n.split("_")[1:])): e for n, e in e_lab.items() if re.fullmatch(rf"{g}_\d+_\d+", n)}
    if cells:
        R, C = max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1
        print(f"{g} total-C error by cell (%), top row first:")
        for r in reversed(range(R)):
            print("   " + " ".join(f"{cells.get((r, c), float('nan')):+5.1f}" for c in range(C)))
if "--json" in sys.argv:
    json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
