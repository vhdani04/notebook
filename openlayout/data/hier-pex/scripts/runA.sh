source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export PYTHONPATH=$OPENLAYOUT_HOME/python
export OMP_NUM_THREADS=6
for h in 0.15 0.1; do echo "== windowed 4x8 halo $h $(date +%T)"; /usr/bin/time -f "%e s wall %U s cpu %M KB" ~/openlayout/venv/bin/python3 -m openlayout.pex t4x8.gds --out /tmp/xs/w4x8_$h.pex.spice --no-cache --halo $h 2>&1 | grep "windows:\|cpu\|extracted"; grep -c "^C" w4x8_$h.pex.spice; done
echo "== flat 4x8 $(date +%T)"; /usr/bin/time -f "%e s wall %U s cpu %M KB" ~/openlayout/venv/bin/python3 -m openlayout.pex t4x8.gds --out /tmp/xs/t4x8.pex.spice --cap flat 2>&1 | grep -v "^RESULT"; grep -c "^C" t4x8.pex.spice
for h in 0.15 0.1; do echo "== 4x8 halo $h vs flat"; ~/openlayout/venv/bin/python3 cmp.py t4x8.pex.spice w4x8_$h.pex.spice; done; echo "ALLDONE $(date +%T)"
