* A2x8: write 1 into cell (1, 7), toggle its XB, P delays (load 0 fF)
.include /home/vhdani/openlayout/models/asap7_ngspice/7nm_TT.pm
.include /home/vhdani/papers/notebook/data/hier-pex/win/a2x8.h0.2.pex.spice
VBLB_0 BLB_0 0 0.7
VBLB_1 BLB_1 0 0.7
VBLB_2 BLB_2 0 0.7
VBLB_3 BLB_3 0 0.7
VBLB_4 BLB_4 0 0.7
VBLB_5 BLB_5 0 0.7
VBLB_6 BLB_6 0 0.7
VBLB_7 BLB_7 0 0
VBL_0 BL_0 0 0.7
VBL_1 BL_1 0 0.7
VBL_2 BL_2 0 0.7
VBL_3 BL_3 0 0.7
VBL_4 BL_4 0 0.7
VBL_5 BL_5 0 0.7
VBL_6 BL_6 0 0.7
VBL_7 BL_7 0 0.7
VVDD_1 VDD_1 0 0.7
VVSS_0 VSS_0 0 0
VVSS_2 VSS_2 0 0
VWL_0 WL_0 0 0
VWL_1 WL_1 0 pwl(0 0 0.1n 0 0.12n 0.7 0.6n 0.7 0.62n 0)
VXB_0_0 XB_0_0 0 0.7
VXB_0_1 XB_0_1 0 0.7
VXB_0_2 XB_0_2 0 0.7
VXB_0_3 XB_0_3 0 0.7
VXB_0_4 XB_0_4 0 0.7
VXB_0_5 XB_0_5 0 0.7
VXB_0_6 XB_0_6 0 0.7
VXB_0_7 XB_0_7 0 0.7
VXB_1_0 XB_1_0 0 0.7
VXB_1_1 XB_1_1 0 0.7
VXB_1_2 XB_1_2 0 0.7
VXB_1_3 XB_1_3 0 0.7
VXB_1_4 XB_1_4 0 0.7
VXB_1_5 XB_1_5 0 0.7
VXB_1_6 XB_1_6 0 0.7
VXB_1_7 XB_1_7 0 pwl(0 0.7 1n 0.7 1.02n 0 2n 0 2.02n 0.7 3n 0.7 3.02n 0 4n 0 4.02n 0.7)
X1 BLB_0 BLB_1 BLB_2 BLB_3 BLB_4 BLB_5 BLB_6 BLB_7 BL_0 BL_1 BL_2 BL_3 BL_4 BL_5 BL_6 BL_7 P_0_0 P_0_1 P_0_2 P_0_3 P_0_4 P_0_5 P_0_6 P_0_7 P_1_0 P_1_1 P_1_2 P_1_3 P_1_4 P_1_5 P_1_6 P_1_7 VDD_1 VSS_0 VSS_2 WL_0 WL_1 XB_0_0 XB_0_1 XB_0_2 XB_0_3 XB_0_4 XB_0_5 XB_0_6 XB_0_7 XB_1_0 XB_1_1 XB_1_2 XB_1_3 XB_1_4 XB_1_5 XB_1_6 XB_1_7 A2x8
.tran 1p 4.6n
.control
set num_threads=1
run
meas tran p_at_1p9 find v(P_1_7) at=1.9n
meas tran p_at_2p9 find v(P_1_7) at=2.9n
meas tran tpr1 trig v(XB_1_7) val=0.35 fall=1 targ v(P_1_7) val=0.35 rise=1
meas tran tpf1 trig v(XB_1_7) val=0.35 rise=1 targ v(P_1_7) val=0.35 fall=1
meas tran tpr2 trig v(XB_1_7) val=0.35 fall=2 targ v(P_1_7) val=0.35 rise=2
meas tran tpf2 trig v(XB_1_7) val=0.35 rise=2 targ v(P_1_7) val=0.35 fall=2
meas tran trise trig v(P_1_7) val=0.14 rise=1 targ v(P_1_7) val=0.56 rise=1
meas tran tfall trig v(P_1_7) val=0.56 fall=1 targ v(P_1_7) val=0.14 fall=1
.endc
.end
