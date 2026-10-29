source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export OMP_NUM_THREADS=2; ulimit -v 6000000
/usr/bin/time -f "ngspice 64x80: %e s wall %M KB" ngspice -b tb64.sp > sim64.log 2>&1; tail -5 sim64.log; echo ALLDONE
