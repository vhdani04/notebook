import collections, math, sys
d = sys.argv[1]
panels = collections.defaultdict(list)
cnt = collections.Counter()
small = []
for f in ("cond0.qui", "cond1.qui", "iface0.qui"):
    for line in open(f"{d}/{f}"):
        t = line.split()
        if not t or t[0] not in ("Q", "T"):
            continue
        n = t[1] if f != "iface0.qui" else "IFACE"
        v = [round(float(x), 6) for x in t[2:]]
        pts = [tuple(v[i:i + 3]) for i in range(0, len(v), 3)]
        key = tuple(sorted(pts))
        panels[key].append((f, n))
        cnt[n] += 1
        e = min(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))
        if e < 0.0005:
            small.append((n, e, pts))
dup = [(k, v) for k, v in panels.items() if len({x[1] for x in v}) > 1 or len(v) > 1]
print(d, "panels", sum(cnt.values()), "duplicated panels:", len(dup), "edges < 0.5 nm:", len(small))
by = collections.Counter(tuple(sorted({x[1] for x in v})) for k, v in dup)
for k, c in by.most_common(8):
    print("  dup between", k, c)
for s in small[:5]:
    print("  small", s)
