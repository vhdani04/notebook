# windowed PEX with FasterCap stubbed out: unique windows and the time of everything else
import sys, time
from openlayout import pex, fieldsolver
calls = []
def fake(conds, *a, **k):
    calls.append(len(conds)); n = len(conds)
    return list(conds), [[(1e-17 if i == j else -1e-19) for j in range(n)] for i in range(n)], 0
fieldsolver.capacitance_matrix = fake
t = time.time()
s = pex.extract(sys.argv[1], out=sys.argv[2], mode=sys.argv[3] if len(sys.argv) > 3 else "rc", cap="window", cache=False)
print("DRY", sys.argv[1], s["windows"], "conductors per solve", sorted(calls), f"{time.time()-t:.1f} s total")
