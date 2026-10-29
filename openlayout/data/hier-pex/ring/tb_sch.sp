* ring oscillator, 51 stages (schematic)
.include /home/vhdani/openlayout/models/asap7_ngspice/7nm_TT.pm
Vdd vdd 0 0.7
.subckt INVS A VDD VSS Y
N1 Y A VSS VSS nmos_rvt l=20n nfin=3
N2 Y A VDD VDD pmos_rvt l=20n nfin=3
.ends
X0 s0 vdd 0 s1 INVS
X1 s1 vdd 0 s2 INVS
X2 s2 vdd 0 s3 INVS
X3 s3 vdd 0 s4 INVS
X4 s4 vdd 0 s5 INVS
X5 s5 vdd 0 s6 INVS
X6 s6 vdd 0 s7 INVS
X7 s7 vdd 0 s8 INVS
X8 s8 vdd 0 s9 INVS
X9 s9 vdd 0 s10 INVS
X10 s10 vdd 0 s11 INVS
X11 s11 vdd 0 s12 INVS
X12 s12 vdd 0 s13 INVS
X13 s13 vdd 0 s14 INVS
X14 s14 vdd 0 s15 INVS
X15 s15 vdd 0 s16 INVS
X16 s16 vdd 0 s17 INVS
X17 s17 vdd 0 s18 INVS
X18 s18 vdd 0 s19 INVS
X19 s19 vdd 0 s20 INVS
X20 s20 vdd 0 s21 INVS
X21 s21 vdd 0 s22 INVS
X22 s22 vdd 0 s23 INVS
X23 s23 vdd 0 s24 INVS
X24 s24 vdd 0 s25 INVS
X25 s25 vdd 0 s26 INVS
X26 s26 vdd 0 s27 INVS
X27 s27 vdd 0 s28 INVS
X28 s28 vdd 0 s29 INVS
X29 s29 vdd 0 s30 INVS
X30 s30 vdd 0 s31 INVS
X31 s31 vdd 0 s32 INVS
X32 s32 vdd 0 s33 INVS
X33 s33 vdd 0 s34 INVS
X34 s34 vdd 0 s35 INVS
X35 s35 vdd 0 s36 INVS
X36 s36 vdd 0 s37 INVS
X37 s37 vdd 0 s38 INVS
X38 s38 vdd 0 s39 INVS
X39 s39 vdd 0 s40 INVS
X40 s40 vdd 0 s41 INVS
X41 s41 vdd 0 s42 INVS
X42 s42 vdd 0 s43 INVS
X43 s43 vdd 0 s44 INVS
X44 s44 vdd 0 s45 INVS
X45 s45 vdd 0 s46 INVS
X46 s46 vdd 0 s47 INVS
X47 s47 vdd 0 s48 INVS
X48 s48 vdd 0 s49 INVS
X49 s49 vdd 0 s50 INVS
X50 s50 vdd 0 s0 INVS
.ic v(s0)=0 v(s1)=0.7 v(s2)=0 v(s3)=0.7 v(s4)=0 v(s5)=0.7 v(s6)=0 v(s7)=0.7 v(s8)=0 v(s9)=0.7 v(s10)=0 v(s11)=0.7 v(s12)=0 v(s13)=0.7 v(s14)=0 v(s15)=0.7 v(s16)=0 v(s17)=0.7 v(s18)=0 v(s19)=0.7 v(s20)=0 v(s21)=0.7 v(s22)=0 v(s23)=0.7 v(s24)=0 v(s25)=0.7 v(s26)=0 v(s27)=0.7 v(s28)=0 v(s29)=0.7 v(s30)=0 v(s31)=0.7 v(s32)=0 v(s33)=0.7 v(s34)=0 v(s35)=0.7 v(s36)=0 v(s37)=0.7 v(s38)=0 v(s39)=0.7 v(s40)=0 v(s41)=0.7 v(s42)=0 v(s43)=0.7 v(s44)=0 v(s45)=0.7 v(s46)=0 v(s47)=0.7 v(s48)=0 v(s49)=0.7 v(s50)=0
.tran 1p 8n
.control
set num_threads=1
run
meas tran t4 when v(s0)=0.35 rise=4
meas tran t10 when v(s0)=0.35 rise=10
let period = (t10 - t4) / 6
let stage = period / 102
print period stage
.endc
.end
