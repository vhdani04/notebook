# FasterCap GMRES failures on INT8_ARRAY windows (notebook entry M3)

Inputs were the FasterCap working directories of a windowed `openlayout pex` run of INT8_ARRAY
(4 x 8 array of 2-bit SRAM cells, mac8 library), kept under /tmp on the VM; not included here.

| File | What |
| --- | --- |
| `w8_auto_ap_4min.log` | FasterCap `-a0.05 -ap` on window w8 for 4 min: the first pass's matrix, then the GMRES failures (iteration lists dropped) |
| `fixed_mesh_vs_auto_w0.txt` | one fixed-mesh pass (`-m0.5/0.3/0.2`) against auto mode on window w0 (`fccmp.py`) |
| `options_w8.txt`, `options_w0.txt` | auto mode with other solver options (`fcopt.py`) |
| `fcexp.py` | one fixed-mesh pass on a window, plain or modified (one dielectric, no substrate, Galerkin) |
| `fcrows.py`, `fcgeo.py`, `fcover.py`, `fciface.py` | the geometry and matrix checks of the stuck windows |
