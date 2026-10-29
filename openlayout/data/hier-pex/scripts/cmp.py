# compare per-net total capacitances of two PEX netlists: labelled nets by name, the
# unlabelled ones (names not stable between runs) as sorted distributions
import sys, statistics
def tot(p):
    for l in open(p):
        if l.startswith("* total capacitance per net"):
            return {a.split()[0]: float(a.split()[1]) for a in l.split(":", 1)[1].split(",")}
a, b = tot(sys.argv[1]), tot(sys.argv[2])
named = [n for n in a if not n.startswith("net") and n in b]
for n in named:
    print(f"  {n}: flat {a[n]:.4f} window {b[n]:.4f} ({(b[n]-a[n])/a[n]*100:+.2f}%)")
ua = sorted(v for n, v in a.items() if n.startswith("net"))
ub = sorted(v for n, v in b.items() if n.startswith("net"))
e = [(y - x) / x * 100 for x, y in zip(ua, ub)]
sig = [(b[n]-a[n])/a[n]*100 for n in named if n != "VSS"] + e
print(f"unlabelled nets {len(ua)}/{len(ub)} (sorted pairs): mean |err| {statistics.mean(map(abs, e)):.2f}%, max {max(map(abs, e)):.2f}%")
print(f"all signal nets: mean |err| {statistics.mean(map(abs, sig)):.2f}%, max {max(map(abs, sig)):.2f}%, mean {statistics.mean(sig):+.2f}%")
