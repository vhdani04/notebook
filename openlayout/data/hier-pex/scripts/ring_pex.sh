source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export PYTHONPATH=$OPENLAYOUT_HOME/python OMP_NUM_THREADS=2
cd /tmp/xs
echo "== windowed RO51 $(date +%T)"
for h in 0.1 0.15; do ~/openlayout/venv/bin/python3 /home/vhdani/papers/notebook/data/hier-pex/scripts/run_win.py ro51.gds RO51 $h /home/vhdani/papers/notebook/data/hier-pex/ring/ro51.h$h.pex.spice 2 2>&1 | grep -v "^ \|^PEX\|^RESULT"; done
echo "== single INVx1 PEX $(date +%T)"
~/openlayout/venv/bin/python3 -m openlayout.pex $ASAP7_STDCELLS/GDS/asap7sc7p5t_28_R_220121a.gds --cell INVx1_ASAP7_75t_R --out /home/vhdani/papers/notebook/data/hier-pex/ring/INVx1.pex.spice 2>&1 | grep RESULT
echo "== flat RO51 $(date +%T)"
/usr/bin/time -f "%e s wall %U s cpu %M KB" ~/openlayout/venv/bin/python3 -m openlayout.pex ro51.gds --cell RO51 --cap flat --out /home/vhdani/papers/notebook/data/hier-pex/ring/ro51.flat.pex.spice 2>&1 | grep -v "^RESULT"
echo "ALLDONE $(date +%T)"
