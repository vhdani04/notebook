* ring oscillator, 51 stages (array)
.include /home/vhdani/openlayout/models/asap7_ngspice/7nm_TT.pm
Vdd vdd 0 0.7
.include ro51.flat.pex.spice
X1 s0 s1 s10 s11 s12 s13 s14 s15 s16 s17 s18 s19 s2 s20 s21 s22 s23 s24 s25 s26 s27 s28 s29 s3 s30 s31 s32 s33 s34 s35 s36 s37 s38 s39 s4 s40 s41 s42 s43 s44 s45 s46 s47 s48 s49 s5 s50 s6 s7 s8 s9 vdd 0 0 RO51
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
