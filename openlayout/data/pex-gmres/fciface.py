import collections, sys
d = sys.argv[1]
zs = collections.Counter()
for line in open(f"{d}/iface0.qui"):
    t = line.split()
    if t and t[0] in ("Q", "T"):
        v = list(map(float, t[2:]))
        zs[tuple(sorted({round(v[i], 5) for i in range(2, len(v), 3)}))] += 1
print(d.split("/")[-1], "iface planes:", dict(zs.most_common(3)))
plane = [k for k in zs if len(k) == 1]
zp = plane[0][0] if plane else None
on = collections.Counter()
cross = collections.Counter()
for f in ("cond0.qui", "cond1.qui"):
    for line in open(f"{d}/{f}"):
        t = line.split()
        if not t or t[0] not in ("Q", "T"):
            continue
        v = list(map(float, t[2:]))
        z = {round(v[i], 5) for i in range(2, len(v), 3)}
        if z == {zp}:
            on[(f, t[1])] += 1
print("  conductor panels lying in the interface plane z =", zp, ":", sum(on.values()), "on", len(on), "conductors", list(on)[:6])
