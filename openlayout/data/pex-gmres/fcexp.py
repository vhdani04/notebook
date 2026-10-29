# One FasterCap pass (no -a auto loop) on a window's input, optionally modified; prints how sane the
# capacitance matrix is: negative diagonals and the largest diagonal (sane windows: ~1e-11 .. 7e-11).
import os, re, shutil, subprocess, sys, time

src, variant = sys.argv[1], sys.argv[2]
d = f"/tmp/fcexp/{os.path.basename(src)}_{variant}"
shutil.rmtree(d, ignore_errors=True)
shutil.copytree(src, d)
lst = open(f"{d}/list.lst").read().splitlines()

if variant == "onediel":                 # one dielectric: both conductor files in k=4.6, no interface
    lst = [l.replace(" 3.23 ", " 4.6 ") for l in lst if not l.startswith("D ")]
elif variant == "nosub":                 # without the substrate plate (the conductor at the lowest z)
    pass
open(f"{d}/list.lst", "w").write("\n".join(lst) + "\n")

if variant == "nosub":
    lowest = None
    for f in ("cond0.qui", "cond1.qui"):
        for line in open(f"{d}/{f}"):
            t = line.split()
            if t and t[0] in ("Q", "T"):
                z = min(map(float, t[4::3]))
                if lowest is None or z < lowest[0]:
                    lowest = (z, t[1])
    for f in ("cond0.qui", "cond1.qui"):
        lines = [l for l in open(f"{d}/{f}") if not (len(l.split()) > 1 and l.split()[0] in ("Q", "T")
                                                       and l.split()[1] == lowest[1])]
        open(f"{d}/{f}", "w").writelines(lines)
    print("removed", lowest[1])

argv = ["FasterCap", "-b", "-d0.5", "-m0.5", "-f2", "-ap", "list.lst"]
if variant == "galerkin":
    argv.insert(2, "-g")
t = time.time()
r = subprocess.run(argv, cwd=d, capture_output=True, text=True, timeout=1800)
out = r.stdout + r.stderr
dt = time.time() - t
i = out.rfind("Capacitance matrix is:")
if i < 0:
    print(variant, "no matrix", out[-300:])
    sys.exit()
rows = [l.split() for l in out[i:].splitlines()[2:] if l.startswith("g")]
diag = [float(r_[k + 1]) for k, r_ in enumerate(rows)]
neg = sum(1 for x in diag if x < 0)
nonconv = out.count("not converging")
print(f"{os.path.basename(src)} {variant}: {dt:.0f} s, {len(rows)} conductors, negative diagonals {neg}, "
      f"max diag {max(diag):.2e}, GMRES not converging {nonconv}")
