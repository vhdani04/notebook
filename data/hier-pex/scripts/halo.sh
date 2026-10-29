source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export OMP_NUM_THREADS=1 PYTHONPATH=/tmp/xs/olpkg
probe() { nice -n 19 ionice -c3 ~/openlayout/venv/bin/python3 -m openlayout.pex ~/designs/mac8/libraries/sram_6t/SRAMCIMsbc/SRAMCIMsbc.gds --out /tmp/xs/probe.spice --cap flat 2>&1 | grep "capacitance" | sed "s/^/probe /"; }
for t in 1x8 2x8; do probe
/usr/bin/time -f "%e s wall %U s cpu" nice -n 19 ionice -c3 ~/openlayout/venv/bin/python3 -m openlayout.pex t$t.gds --out /tmp/xs/h$t.pex.spice --no-cache --halo 0.1 2>&1 | grep "windows:\|cpu"
~/openlayout/venv/bin/python3 cmp.py t$t.pex.spice h$t.pex.spice | tail -4; done; probe; echo ALLDONE
