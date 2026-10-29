* ring oscillator, 51 stages (cells)
.include /home/vhdani/openlayout/models/asap7_ngspice/7nm_TT.pm
Vdd vdd 0 0.7
.include INVx1.ref.ngspice.sp
X0 0 vdd s0 s1 INVREF
X1 0 vdd s1 s2 INVREF
X2 0 vdd s2 s3 INVREF
X3 0 vdd s3 s4 INVREF
X4 0 vdd s4 s5 INVREF
X5 0 vdd s5 s6 INVREF
X6 0 vdd s6 s7 INVREF
X7 0 vdd s7 s8 INVREF
X8 0 vdd s8 s9 INVREF
X9 0 vdd s9 s10 INVREF
X10 0 vdd s10 s11 INVREF
X11 0 vdd s11 s12 INVREF
X12 0 vdd s12 s13 INVREF
X13 0 vdd s13 s14 INVREF
X14 0 vdd s14 s15 INVREF
X15 0 vdd s15 s16 INVREF
X16 0 vdd s16 s17 INVREF
X17 0 vdd s17 s18 INVREF
X18 0 vdd s18 s19 INVREF
X19 0 vdd s19 s20 INVREF
X20 0 vdd s20 s21 INVREF
X21 0 vdd s21 s22 INVREF
X22 0 vdd s22 s23 INVREF
X23 0 vdd s23 s24 INVREF
X24 0 vdd s24 s25 INVREF
X25 0 vdd s25 s26 INVREF
X26 0 vdd s26 s27 INVREF
X27 0 vdd s27 s28 INVREF
X28 0 vdd s28 s29 INVREF
X29 0 vdd s29 s30 INVREF
X30 0 vdd s30 s31 INVREF
X31 0 vdd s31 s32 INVREF
X32 0 vdd s32 s33 INVREF
X33 0 vdd s33 s34 INVREF
X34 0 vdd s34 s35 INVREF
X35 0 vdd s35 s36 INVREF
X36 0 vdd s36 s37 INVREF
X37 0 vdd s37 s38 INVREF
X38 0 vdd s38 s39 INVREF
X39 0 vdd s39 s40 INVREF
X40 0 vdd s40 s41 INVREF
X41 0 vdd s41 s42 INVREF
X42 0 vdd s42 s43 INVREF
X43 0 vdd s43 s44 INVREF
X44 0 vdd s44 s45 INVREF
X45 0 vdd s45 s46 INVREF
X46 0 vdd s46 s47 INVREF
X47 0 vdd s47 s48 INVREF
X48 0 vdd s48 s49 INVREF
X49 0 vdd s49 s50 INVREF
X50 0 vdd s50 s0 INVREF
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
