# OpenLayout

Lab notebook for [OpenLayout](https://github.com/vhdani04/OpenLayout), my open-source full-custom
flow for the ASAP7 7 nm PDK (xschem, KLayout, FasterCap, ngspice): the bugs found while designing
the [SRAM CIM macro](../sram-cim), why they happened and how they were fixed, and the measurements
behind each new capability. Read it at [danielvigna.com/notebook/openlayout](https://danielvigna.com/notebook/openlayout)
or as a [PDF](https://github.com/vhdani04/notebook/releases/download/latest/openlayout.pdf).

| Path | What |
| --- | --- |
| `notebook.tex` | The notebook |
| `data/hier-pex/` | M1, M2: windowed vs flat PEX. `REPORT.md` is the full write-up; `scripts/`, comparisons (`cmp/`), netlists up to 8 × 8 (`win/`, `flat/`), delays (`sim/`), the ring oscillator (`ring/`), logs |

The 64 × 80 netlists (`data/hier-pex/big/`, `netlists/`, about 116 MB) are regenerable and kept
out of git. Scripts were run on an Ubuntu VM with OpenLayout installed and use absolute paths;
adjust them to your setup.
