* timing
.include /home/vhdani/openlayout/models/asap7_ngspice/7nm_TT.pm
.include /tmp/xs/cim1.pex.spice
VDD VDD 0 0.7
VBL BL 0 pwl(0 0.7 2n 0.7 2.1n 0)
VBLB BLB 0 pwl(0 0 2n 0 2.1n 0.7)
VWL WL 0 pwl(0 0 0.5n 0 0.6n 0.7 1.5n 0.7 1.6n 0 2.5n 0 2.6n 0.7 3.5n 0.7 3.6n 0)
VXB XB 0 pulse(0.7 0 4n 20p 20p 0.5n 1n)
X1 BL BLB P VDD 0 WL XB SRAMCIMsbc
.tran 1p 12n
.control
run
meas tran tp when v(P)=0.35 rise=1
.endc
.end
