source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export PYTHONPATH=$OPENLAYOUT_HOME/python OMP_NUM_THREADS=1
cd /tmp/xs
for h in 0.1 0.15 0.2; do for t in a1x8 a2x8 a4x8 a8x8; do ~/openlayout/venv/bin/python3 /home/vhdani/papers/notebook/data/hier-pex/scripts/run_win.py $t.gds A${t#a} $h /home/vhdani/papers/notebook/data/hier-pex/win/$t.h$h.pex.spice 2 2>&1 | grep -v "^ \|^PEX\|^RESULT"; done; done; echo "ALLDONE $(date +%T)"
