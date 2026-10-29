import collections, re
txt = open("out.txt").read()
i = txt.index("Capacitance matrix is:")
rows = {}
for line in txt[i:].splitlines()[2:52]:
    t = line.split()
    rows[t[0][3:]] = list(map(float, t[1:]))
names = list(rows)
boxes = collections.defaultdict(lambda: [9, 9, 9, -9, -9, -9])
npan = collections.Counter()
for f in ("cond0.qui", "cond1.qui"):
    for line in open(f):
        t = line.split()
        if not t or t[0] not in ("Q", "T"):
            continue
        v = list(map(float, t[2:]))
        b = boxes[t[1]]; npan[t[1]] += 1
        for k in range(0, len(v), 3):
            for a in range(3):
                b[a] = min(b[a], v[k + a]); b[a + 3] = max(b[a + 3], v[k + a])
for k, n in enumerate(names):
    diag = rows[n][k]
    bad = diag < 0 or abs(diag) > 8e-11
    print(("BAD " if bad else "ok  ") + n, f"{diag:.2e}", "box", [round(x, 3) for x in boxes[n]], "panels", npan[n])
