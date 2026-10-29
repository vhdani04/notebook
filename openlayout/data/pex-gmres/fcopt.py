# Auto mode (-a0.05) on a stuck window with different solver options: does GMRES converge, how long,
# and the totals against a reference run (argv[2] = a variant name, once all have run).
import json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

src = sys.argv[1]
VARIANTS = {
    "base": ["-a0.05", "-d0.5", "-m0.5", "-f2", "-ap"],
    "pj": ["-a0.05", "-d0.5", "-f2", "-pj"],
    "ps2048": ["-a0.05", "-d0.5", "-f2", "-ps2048"],
    "galerkin": ["-a0.05", "-d0.5", "-f2", "-ap", "-g"],
    "d1": ["-a0.05", "-f2", "-ap"],
}
LIMIT = 900


def run(name):
    d = f"/tmp/fcopt/{os.path.basename(src)}_{name}"
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(src, d)
    t = time.time()
    proc = subprocess.Popen(["FasterCap", "-b", *VARIANTS[name], "list.lst"], cwd=d, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    lines, failed = [], 0
    for line in proc.stdout:
        lines.append(line)
        failed += "not converging" in line
        if failed or time.time() - t > LIMIT:
            proc.kill()
            break
    proc.wait()
    out = "".join(lines)
    dt = time.time() - t
    i = out.rfind("Capacitance matrix is:")
    diag = {}
    if i >= 0 and not failed and dt <= LIMIT:
        rows = [l.split() for l in out[i:].splitlines()[2:] if l.startswith("g")]
        diag = {r[0]: float(r[k + 1]) for k, r in enumerate(rows)}
    passes = out.count("Iteration number #")
    return name, dt, failed, passes, diag


with ThreadPoolExecutor(len(VARIANTS)) as pool:
    res = list(pool.map(run, VARIANTS))
ok = {n: diag for n, dt, f, p, diag in res if diag}
ref = next(iter(ok.values()), None)
for n, dt, f, p, diag in res:
    state = "GMRES failed" if f else ("time limit" if not diag else "converged")
    cmp = ""
    if diag and ref:
        errs = [abs(diag[k] / ref[k] - 1) * 100 for k in ref if ref[k]]
        cmp = f"vs {next(iter(ok))}: mean {sum(errs) / len(errs):.2f} %, max {max(errs):.2f} %"
    print(f"{n:9s} {state:12s} {dt:5.0f} s, {p} passes {cmp}")
json.dump({n: d for n, d in ok.items()}, open(f"/tmp/fcopt/{os.path.basename(src)}.json", "w"))
