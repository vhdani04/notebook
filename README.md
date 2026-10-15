# Lab notebook: SRAM compute-in-memory macro in ASAP7

My research lab notebook for a digital SRAM compute-in-memory (CIM) macro in the ASAP7
predictive 7 nm PDK, designed and verified with [OpenLayout](https://github.com/vhdani04/OpenLayout)
(xschem, KLayout, FasterCap, ngspice). Every design decision and every measurement gets one
entry when it happens: the question, the options, the method (with the script that reproduces
it), the result, the decision and what would reopen it. Claims that are reasoning but not yet
measured are marked *to verify*.

It is rendered live at [danielvigna.com/notebook](https://danielvigna.com/notebook), and the
latest PDF is attached to the [`latest` release](../../releases/tag/latest) on every push.

## Layout

| Path | What |
| --- | --- |
| `notebook.tex` | The notebook, the single source for the PDF and the web page |
| `scripts/` | Scripts and testbenches referenced by entries (`tile.py`, `bbox.rb`, `tb_*.sp`) |
| `data/cells/` | DRC (`.lyrdb`) and LVS (`.lvsdb`) reports for the bitcell, open in KLayout |
| `data/pex-scaling/` | M1: extracted netlists (`.pex.spice.gz`), ngspice logs, `measurements.csv` |

## Build the PDF

```sh
latexmk -pdf notebook.tex
```

Needs a TeX Live with `booktabs`, `enumitem`, `hyperref`, `float` and `xcolor`. `latexmk -c` cleans up.

## Entry format

The macros are defined at the top of `notebook.tex` and the web page parses them, so keep to them:

```latex
\section{Bitcell}
\entry{D4. 1-bit 10T cell instead of the 2-bit cell}{2026-10-14}{d4}
\field{Question} ...
\field{Options} ...
\field{Method} ... \file{scripts/bbox.rb} ...
\field{Result} ... \verify{claim not yet measured}
\field{Decision} ...
\field{Revisit if} ...
```

IDs: `D` decision, `M` measurement, `O` open, `T` tooling, numbered in order; the third argument
is the anchor (`danielvigna.com/notebook#d4`). `\file{}` paths under `scripts/` and `data/`
become links into this repo. The `Open items` section feeds the "Now" block on the page.

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

ASAP7 is © Arizona State University and Arm under its own license; no PDK files are included here.
