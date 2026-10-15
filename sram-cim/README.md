# SRAM compute-in-memory macro in ASAP7

Lab notebook for a digital SRAM compute-in-memory (CIM) macro in the ASAP7 predictive 7 nm PDK,
designed and verified with [OpenLayout](https://github.com/vhdani04/OpenLayout) (xschem, KLayout,
FasterCap, ngspice). Read it at [danielvigna.com/notebook/sram-cim](https://danielvigna.com/notebook/sram-cim)
or as a [PDF](https://github.com/vhdani04/notebook/releases/download/latest/sram-cim.pdf).

| Path | What |
| --- | --- |
| `notebook.tex` | The notebook |
| `scripts/` | Scripts and testbenches referenced by entries (`tile.py`, `bbox.rb`, `tb_*.sp`) |
| `data/cells/` | DRC (`.lyrdb`) and LVS (`.lvsdb`) reports for the bitcell, open in KLayout |
| `data/pex-scaling/` | M1: extracted netlists (`.pex.spice.gz`), ngspice logs, `measurements.csv` |

## Reproducing entries

The scripts were run on an Ubuntu VM with OpenLayout installed; paths to the PDK models
(`~/openlayout/models/asap7_ngspice/7nm_TT.pm`) and to the cell layouts (in my design
library, not published here) are absolute, so adjust them to your setup.

- **D4, bitcell size**: `klayout -b -r scripts/bbox.rb` prints the bounding box of
  `SRAMCIMsbc.gds` and its width in gate pitches (54 nm CPP).
- **M1, flat PEX scaling**:
  1. Tile the cell: `python3 scripts/tile.py SRAMCIMsbc.gds 1 8 t1x8.gds` (rows, columns;
     0.54 µm pitch, odd rows mirrored). Needs the `klayout` Python module (`pip install klayout`).
  2. Extract: `openlayout pex` on each layout (FasterCap 3D, mode rc); the resulting netlists
     are in `data/pex-scaling/*.pex.spice.gz`.
  3. Simulate: `ngspice -b scripts/tb_t1x8.sp` (12 ns transient). The testbenches include the
     netlist from `/tmp/xs/`; point them at the unzipped files instead.
  4. Wall time, peak memory and element counts are in `data/pex-scaling/measurements.csv`,
     raw simulator output in `sim_*.log`.
