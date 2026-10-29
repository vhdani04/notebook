# Windowed (hierarchical) PEX in OpenLayout: validation report, 2026-10-15

Data, scripts, netlists and logs: `~/papers/notebook/openlayout/data/hier-pex/` on the VM (`openlayout-hier-pex.diff`
is the OpenLayout change before it was committed as 64b50e2). Cell: SRAMCIMsbc (10T compute-in-memory bit cell, 0.54 × 0.27 µm),
tiled with odd rows mirrored. Labelled tiles (`scripts/tile2.py`) carry WL_r, BL_c / BLB_c, XB_r_c,
P_r_c and one VDD_k / VSS_k per rail, so every cell is powered and can be probed.

## 1. Capacitance: windowed vs flat (FasterCap on the whole tile)

Total capacitance per net, the signal nets + VDD (VSS rails are ground; listed apart):

| tile | halo | nets | mean abs error | max abs error | worst nets | VSS rail |
|---|---|---|---|---|---|---|
| 1 × 8 | 0.10 µm (default) | 58 | 0.43 % | 1.53 % | VDD_1 +1.5 %, XB +0.7 % | −9.7 % |
| 1 × 8 | 0.15 µm | 58 | 0.38 % | 1.86 % | VDD_1 +1.9 % | −9.3 % |
| 1 × 8 | 0.20 µm | 58 | 0.33 % | 1.52 % | VDD_1 +1.5 % | −8.9 % |
| 2 × 8 | 0.10 µm (default) | 99 | 0.53 % | 1.68 % | BL_0 +1.4 %, XB_0_2 +1.3 %, VDD_1 +1.2 % | −7.0 / +1.2 % |
| 2 × 8 | 0.15 µm | 99 | 0.47 % | 1.47 % | XB_0_2 +1.5 % | −6.6 / +1.1 % |
| 2 × 8 | 0.20 µm | 99 | 0.45 % | 1.53 % | XB_1_7 −1.5 % | −6.3 / +0.9 % |
| 4 × 8 | | | | | flat reference still running (8.4 h at 08:20) | |
| 8 × 8 | | | | | flat not feasible: ~85 000 CPU-s by the measured n² scaling | |

- The halo hardly matters between 0.10 and 0.20 µm here (the halo is a minimum: each axis is widened
  until the context's outer edges cross wires, e.g. 0.116 / 0.134 µm for 0.10).
- Internal nets (Q, QB, ...; compared as sorted lists): max 0.85 % (1 × 8), 1.68 % (2 × 8).
- No edge or corner effect: P total-C error by cell, 2 × 8, halo 0.10:
  `−0.3 −0.2 −0.3 −0.7 −0.4 −0.5 −0.2 −0.2` (top row) / `+0.3 +0.2 +0.1 +0.1 −0.1 +0.0 −0.3 +0.2`.
- VSS_0 is 7-10 % low because the flat solve's substrate plate reaches 0.3 µm past the block; it is the
  ground node, so this does not enter any simulation.

Coupling capacitance between labelled signal nets (pairs ≥ 1 % of a net's total; sums over all pairs of
a kind; halo 0.10):

| pair | 1 × 8 | 2 × 8 |
|---|---|---|
| BL–WL | +2.6 % | +4.0 % |
| BLB–WL | +1.3 % | +2.6 % |
| P–XB | +2.3 % | +1.7 % |
| BLB–P | +1.1 % | +1.1 % |
| BLB–XB | −0.3 % | −0.8 % |
| P–WL | −0.5 % | +1.7 % |
| WL–XB | −1.5 % | +0.2 % |
| BL–BLB | +1.4 % | +1.9 % |
| BL–XB (0.016 fF) | +4.4 % | +3.1 % |

Couplings to VSS read +2.6…+3.8 % because the windowed netlist folds couplings under 0.5 % of a net's
total into ground, i.e. onto VSS_0; that is bookkeeping, not a field-solver difference. The coupling
errors (up to 4 % on BL–WL) are larger than the total errors (≤ 1.7 %): windowing redistributes a little
capacitance between a net's neighbours, mostly at window edges, while conserving the totals.

## 2. Why windows are "alike", and that it hides no edge cells

A window's key is the geometry of the window *and* its whole context (0.1-0.2 µm around it), moved to
the origin, with the nets numbered by their shapes. Two windows share a result only if everything the
solver sees is identical. Kinds by position (row 0 at the bottom), halo 0.10:

```
2 x 8:  1 3 3 3 3 3 3 5        8 x 8:  3 7 7 7 7 7 7 11
        0 2 2 2 2 2 2 4                2 6 6 6 6 6 6 10
                                       1 5 5 5 5 5 5  9
4 x 8:  3 7 7 7 7 7 7 11              2 6 6 6 6 6 6 10
        2 6 6 6 6 6 6 10              1 5 5 5 5 5 5  9
        1 5 5 5 5 5 5  9              2 6 6 6 6 6 6 10
        0 4 4 4 4 4 4  8              1 5 5 5 5 5 5  9
                                       0 4 4 4 4 4 4  8
```

Corners, edges and the two mirrored interior rows are distinct kinds; 4 × 8 already has all 12, and
8 × 8 and 64 × 80 add none (64 × 80: 5120 windows, 12 kinds, all from the cache). This is exactly the
easy case for windowing: an array of identical cells. **Not covered**: mixed neighbours (periphery,
different cells side by side) and long routes crossing many windows - left for a placed-and-routed
design.

## 3. Electrical check: SRAM P delays

`scripts/gen_tb.py`: write Q=1 into cell (r, c) (BL high, BLB low, one WL pulse), then toggle that cell's
XB twice; P = Q AND NOT XB. (The earlier testbench wrote 1 and then 0 before toggling XB, so P never
moved.) P reaches 0.700 V at 1.9 ns in every run (Q=1 written). Models: 7nm_TT.pm, 0.7 V, no load on P.

1 × 8, flat vs windowed:

| cell | flat tpr / tpf | halo 0.10 | halo 0.15 | halo 0.20 |
|---|---|---|---|---|
| (0,0) corner | 11.636 / 12.539 ps | +0.21 / +0.20 % | +0.20 / +0.18 % | +0.07 / +0.09 % |
| (0,4) middle | 11.627 / 12.532 ps | +0.27 / +0.25 % | +0.29 / +0.25 % | +0.22 / +0.20 % |
| (0,7) corner | 11.617 / 12.523 ps | +0.37 / +0.32 % | +0.32 / +0.27 % | +0.30 / +0.26 % |

P slews: +0.3…+0.7 %. Sensitivity: all capacitors of the flat netlist ×1.10 moves tpr +3.9 %, tpf
+3.2 %, slews +6 % - so ~0.35 % of delay per % of capacitance; +0.2-0.4 % delay is ~+1 % capacitance.
2 × 8, flat vs windowed (tpr / tpf):

| cell | flat | halo 0.10 | halo 0.15 | halo 0.20 |
|---|---|---|---|---|
| (0,0) corner | 11.638 / 12.543 ps | +0.47 / +0.37 % | +0.45 / +0.36 % | +0.39 / +0.29 % |
| (0,4) bottom edge | 11.635 / 12.542 ps | +0.43 / +0.32 % | +0.46 / +0.33 % | +0.34 / +0.26 % |
| (1,4) top edge | 11.667 / 12.568 ps | −0.11 / −0.09 % | −0.03 / −0.03 % | −0.15 / −0.10 % |
| (1,7) corner | 11.634 / 12.544 ps | +0.11 / +0.06 % | +0.15 / +0.07 % | +0.08 / +0.03 % |

8 × 8 interior cell (4,4), windowed: tpr 11.696 ps (RC), 11.638 ps (C only).

## 4. 64 × 80 (51 200 transistors, labelled)

- Extraction from the cache (0 solves): 575 s, 2.2 GB peak; 1.46 M capacitors, 153 216 resistors.
- Sane: no node on capacitors only, no node without a DC path to a pin, every net's R network in one
  piece (179 105 nodes).
- Per-net totals against 8 × 8 (windowed), per unit: WL per cell 0.999, BL per row 0.993, BLB 0.991,
  XB / P per cell 1.000, VDD 0.999. Against flat 1 × 8: WL / XB / P per cell +1.0…+1.4 % (more
  neighbours), BL / BLB per row −5 % (the line-end fringe spread over 64 rows), VDD per cell 1.65×
  (each rail serves two rows in the array, one in 1 × 8). All physical.
- Simulation: not done. ngspice did not finish the DC operating point of the capacitance-only netlist
  (51 200 transistors, 174 k capacitors) in 40 min; the RC netlist (1.46 M capacitors) did not start its
  transient in 31 min. Simulating at this size needs a subcircuit per kind of window or another simulator.

## 5. Ring oscillator, 51 × INVx1_ASAP7_75t_R (snake in two rows, M2 straps, M2/M3 turnarounds)

| netlist | period | per stage |
|---|---|---|
| schematic (no parasitics) | 301.6 ps | 2.96 ps |
| library reference extraction (xAct3D) × 51, ideal wires | 649.3 ps | 6.37 ps |
| OpenLayout single-cell PEX × 51, ideal wires | 629.8 ps | 6.17 ps (−3.0 % vs reference) |
| OpenLayout windowed RO51, halo 0.10 | 624.7 ps | 6.12 ps |
| OpenLayout windowed RO51, halo 0.15 | 623.1 ps | 6.11 ps |
| OpenLayout flat RO51 (46 000 s) | 632.3 ps | 6.20 ps |

- OpenLayout's cell PEX is 3 % faster than the library's reference, in line with its calibration
  (delays within ~2-3 %).
- **Windowed vs flat on the ring: period −1.2 % (624.7 vs 632.3 ps), stage-node capacitance −3.7 %
  mean (−0.6 … −5.3 %) at halo 0.10, −4.1 % mean at 0.15.** This is clearly worse than on the SRAM tiles
  and is a systematic underestimate, as on the 2 × 4 INVx1 test array (−2.8 % mean, −4.3 % worst). An
  earlier explanation (same-net fringe between abutting cells) was wrong: flat stage nodes are 0.383 fF,
  the same as the isolated cell's A + Y. Likely cause to investigate: narrow windows (0.162 µm, one
  INVx1) cut through the cells' vertical gates / M1 pins every 0.162 µm, so a large share of each net
  sits near a window edge and its 5 nm gap; a wider `--window` (2-4 cells) should be tested.

## 6. Recommended defaults

- **Halo 0.10 µm** (a minimum; widened to clear wires): as accurate as 0.15-0.20 µm on the SRAM tiles
  (totals ≤ 1.7 %, delays ≤ 0.5 %) and 2-3× faster. **Not yet validated for narrow standard cells**: the
  INVx1 ring is −3.7 % in capacitance and −1.2 % in period; windows of one narrow cell are suspect.
- **Coupling threshold 0.5 %** of the nets' totals (folded to ground): keeps totals exact and the
  netlist ~3× sparser; it shifts what is labelled "coupling to VSS" by a few %. For coupling-noise
  analysis between specific nets, use `--cap flat` on a small block or lower WIN_MIN_CC.

## 7. Compute

The host has 14 cores / 20 threads, the VM 8 vCPUs and 10 GB. FasterCap uses ~1-1.5 cores per run
however many threads it is given, so throughput scales with the number of runs; with 6-8 flat runs plus
sims the VM was oversubscribed (load 9-26) and the flat references ran 5-10× slower than idle (flat 2 × 8:
8.3 h). For the windowed flow CPU count matters little (12 solves, `--jobs`); for flat references, more
vCPUs would let more of them run at once. Memory was never the limit (peak use ~7 GB).

## 8. Flat 4 x 8 did not finish (a measurement in itself)

Both flat 4 x 8 references (377 nets; FasterCap -a0.05, the same settings as every other run) were stopped
unfinished on 2026-10-17 around 18:00 at the user's request because the VM was too slow for interactive
work. Old-tile 4 x 8: started 2026-10-14 22:21, about 67 h wall; 71.7 CPU-hours when last measured
(13:37 on the 17th), more by the stop. Labelled 4 x 8: started 2026-10-14 23:58, about 66 h wall;
60.8 CPU-hours at 13:37. For comparison, flat 2 x 8 (197 nets) took 8.1 CPU-hours and flat 1 x 8 (107 nets)
0.55 CPU-hours, so going from 2 x 8 to 4 x 8 (1.9 x the nets) cost more than 8.9 x the CPU time, against
3.6 x for a net-count-squared scaling. FasterCap used about 1.1-1.5 cores per run however many threads
it was allowed. The VM was also paused by the host for 26 s to 6.5 min at a time (220 soft lockups in
30 h on the 14th / 15th), which inflated the wall time but not the CPU time. Windowed 4 x 8 for comparison:
539 s single-threaded, 205 s with --jobs 6.
