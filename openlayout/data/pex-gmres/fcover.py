import collections, sys
d = sys.argv[1]
planes = collections.defaultdict(list)     # (axis, coord) -> [(cond, rect)]
nonaxis = 0
for f in ("cond0.qui", "cond1.qui"):
    for line in open(f"{d}/{f}"):
        t = line.split()
        if not t or t[0] not in ("Q", "T"):
            continue
        v = list(map(float, t[2:]))
        pts = [v[i:i + 3] for i in range(0, len(v), 3)]
        for ax in range(3):
            if len({round(p[ax], 6) for p in pts}) == 1:
                o = [a for a in range(3) if a != ax]
                r = (min(p[o[0]] for p in pts), min(p[o[1]] for p in pts), max(p[o[0]] for p in pts), max(p[o[1]] for p in pts))
                planes[(ax, round(pts[0][ax], 6))].append((t[1], r))
                break
        else:
            nonaxis += 1
hits = collections.Counter()
touch = collections.Counter()
for key, items in planes.items():
    items.sort(key=lambda x: x[1][0])
    for i, (ca, a) in enumerate(items):
        for cb, b in items[i + 1:]:
            if b[0] >= a[2]:
                break
            if ca == cb:
                continue
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 1e-6 and oy > 1e-6:
                hits[tuple(sorted((ca, cb)))] += 1
print(d.split("/")[-1], "non-axis panels", nonaxis, "| coplanar overlapping panels of different conductors:", sum(hits.values()), dict(hits.most_common(6)))
