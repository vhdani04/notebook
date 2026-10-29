source ~/openlayout/flow/env/openlayout.sh >/dev/null 2>&1; ulimit -v 4500000; cd /home/vhdani/papers/notebook/data/hier-pex/sim
/usr/bin/time -f "%e s wall %M KB" timeout 2400 ngspice -b tb_a64x80_c_32_40.sp > tb_a64x80_c_32_40.log 2>&1; echo "exit $?"; grep "^p_at\|^tp\|^trise\|^tfall\|rror" tb_a64x80_c_32_40.log; tail -2 tb_a64x80_c_32_40.log; echo ALLDONE
