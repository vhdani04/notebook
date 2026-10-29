source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export OMP_NUM_THREADS=1 PYTHONPATH=/tmp/xs/olpkg
for h in 0.12 0.15; do /usr/bin/time -f "halo $h: %U s cpu" nice -n 19 ionice -c3 ~/openlayout/venv/bin/python3 -m openlayout.pex invarray.gds --mode c --cap window --halo $h --no-cache --out /tmp/xs/inv_$h.spice 2>&1 | grep "cpu"; ~/openlayout/venv/bin/python3 cmp.py invarray_flat.spice inv_$h.spice | python3 -c "
import sys,re
L=sys.stdin.read().splitlines(); e=[float(re.search(r\"\(([-+0-9.]+)%\)\",l).group(1)) for l in L if re.match(r\"  [AY]\d\d\",l)]
print(\"  A/Y pins:\", len(e), \"worst %+.1f%%\" % max(e,key=abs), \"mean %+.2f%%\" % (sum(e)/len(e)))"; done; echo ALLDONE
