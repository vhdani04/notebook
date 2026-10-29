# INT8_ARRAY parasitic extraction (notebook entry M4)

OpenLayout windowed PEX (FasterCap 3D, -pj, mode rc) of the 4 x 8 array of 2-bit SRAM cells, 2026-10-29.

| File | What |
| --- | --- |
| `INT8_ARRAY.pex.spice.gz` | the post-layout netlist (640 transistors, 3706 R, 46683 C) |
| `totals.csv` | total capacitance per net (fF), with the kind of net |
| `header.txt` | the netlist's header: extraction settings and counts |

VDD / VSS have no pins yet (the rails are not strapped), so they appear as two unnamed nets.
