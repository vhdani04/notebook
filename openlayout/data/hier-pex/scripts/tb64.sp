* 64x80 windowed PEX netlist: load and a short transient
.include /home/vhdani/openlayout/models/asap7_ngspice/7nm_TT.pm
.include /tmp/xs/w64x80.pex.spice
VDD VDD 0 0.7
VBL BL 0 0.7
VBLB BLB 0 0
VWL WL 0 pwl(0 0 10p 0 20p 0.7)
VXB XB 0 0.7
X1 BL BLB P VDD 0 WL XB T64x80
.tran 1p 40p
.control
run
print v(P)[length(v(P))-1]
.endc
.end
