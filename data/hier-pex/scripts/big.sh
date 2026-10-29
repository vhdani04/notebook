source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export PYTHONPATH=$OPENLAYOUT_HOME/python OMP_NUM_THREADS=1
cd /tmp/xs
echo "== a64x80 rc halo 0.1 $(date +%T)"
/usr/bin/time -f "%e s wall %M KB" ~/openlayout/venv/bin/python3 /home/vhdani/papers/notebook/data/hier-pex/scripts/run_win.py a64x80.gds A64x80 0.1 /home/vhdani/papers/notebook/data/hier-pex/big/a64x80.h0.1.pex.spice 2 2>&1 | grep -v "^ \|^PEX\|^RESULT"
echo "== a64x80 c-only halo 0.1 $(date +%T)"
/usr/bin/time -f "%e s wall %M KB" ~/openlayout/venv/bin/python3 -m openlayout.pex a64x80.gds --cell A64x80 --mode c --halo 0.1 --out /home/vhdani/papers/notebook/data/hier-pex/big/a64x80.c.h0.1.pex.spice 2>&1 | grep "windows:\|wall\|capacitance:"
echo "ALLDONE $(date +%T)"
