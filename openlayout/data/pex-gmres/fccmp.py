# w0 (a window auto mode finished): auto -a0.05 vs fixed-mesh passes; compare each conductor's
# total capacitance (the matrix diagonal) against auto mode.
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

src = "/tmp/ol_pex_fv6rv_xf/fastercap/w0"
RUNS = {"auto": ["-a0.05"], "m0.5": ["-m0.5"], "m0.3": ["-m0.3"], "m0.2": ["-m0.2"]}


def run(name):
    d = f"/tmp/fccmp/{name}"
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(src, d)
    argv = ["FasterCap", "-b", *RUNS[name], "-d0.5", "-f2", "-ap", "list.lst"]
    t = time.time()
    out = subprocess.run(argv, cwd=d, capture_output=True, text=True, timeout=7200).stdout
    dt = time.time() - t
    i = out.rfind("Capacitance matrix is:")
    rows = [l.split() for l in out[i:].splitlines()[2:] if l.startswith("g")]
    return name, dt, {r[0]: float(r[k + 1]) for k, r in enumerate(rows)}, out.count("not converging")


with ThreadPoolExecutor(4) as pool:
    res = {n: (dt, diag, nc) for n, dt, diag, nc in pool.map(run, RUNS)}
ref = res["auto"][1]
for n, (dt, diag, nc) in res.items():
    errs = [abs(diag[k] / ref[k] - 1) * 100 for k in ref if abs(ref[k]) > 0]
    print(f"{n:5s} {dt:6.0f} s  not converging {nc}  vs auto: mean {sum(errs) / len(errs):.2f} %, max {max(errs):.2f} %")
