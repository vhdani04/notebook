source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; export OMP_NUM_THREADS=1
for v in w t; do /usr/bin/time -f "$v %e s wall" nice -n 19 ionice -c3 ngspice -b tbs_$v.sp > sims_$v.log 2>&1; grep -h "^tp\|wall" sims_$v.log; done; echo ALLDONE
