source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export PYTHONPATH=$OPENLAYOUT_HOME/python
export OMP_NUM_THREADS=2
echo "== windowed 64x80 halo 0.15 $(date +%T)"; /usr/bin/time -f "%e s wall %U s cpu %M KB" ~/openlayout/venv/bin/python3 -m openlayout.pex t64x80.gds --out /tmp/xs/w64x80_15.pex.spice --halo 0.15 --mode rc 2>&1 | grep -v "^RESULT"; ls -la w64x80_15.pex.spice; echo "ALLDONE $(date +%T)"
