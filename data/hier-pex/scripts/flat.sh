# flat PEX reference of a labelled tile: flat.sh <a1x8|a2x8|...>
source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export PYTHONPATH=$OPENLAYOUT_HOME/python OMP_NUM_THREADS=2
cd /tmp/xs; T=$1; C=A${T#a}
echo "== flat $T start $(date +%T)"
/usr/bin/time -f "%e s wall %U s cpu %M KB" ~/openlayout/venv/bin/python3 -m openlayout.pex $T.gds --cell $C --cap flat --out /home/vhdani/papers/notebook/data/hier-pex/flat/$T.flat.pex.spice 2>&1 | grep -v "^RESULT"
echo "ALLDONE $(date +%T)"
