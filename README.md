# Lab notebooks

My research lab notebooks, one folder per project. Every design decision and every measurement
gets one entry when it happens: the question, the options, the method (with the script that
reproduces it), the result, the decision and what would reopen it. Claims that are reasoning but
not yet measured are marked *to verify*.

They are rendered live at [danielvigna.com/notebook](https://danielvigna.com/notebook), and each
project's PDF is attached to the [`latest` release](https://github.com/vhdani04/notebook/releases/tag/latest) on every push.

| Project | Folder | PDF |
| --- | --- | --- |
| SRAM compute-in-memory macro in ASAP7, built with [OpenLayout](https://github.com/vhdani04/OpenLayout) | [`sram-cim/`](sram-cim) | [sram-cim.pdf](https://github.com/vhdani04/notebook/releases/download/latest/sram-cim.pdf) |
| ML-based floor-planning for a small-scale SoC | [`ml-soc/`](ml-soc) | [ml-soc.pdf](https://github.com/vhdani04/notebook/releases/download/latest/ml-soc.pdf) |
| [OpenLayout](https://github.com/vhdani04/OpenLayout), the open-source ASAP7 custom-layout flow the other projects are built with: its bugs, fixes and measurements | [`openlayout/`](openlayout) | [openlayout.pdf](https://github.com/vhdani04/notebook/releases/download/latest/openlayout.pdf) |

Each folder holds `notebook.tex` (the single source for the PDF and the web page), plus
`scripts/` and `data/` for whatever the entries reference.

## Build a PDF

```sh
cd sram-cim
latexmk -pdf notebook.tex
```

Needs a TeX Live with `booktabs`, `enumitem`, `hyperref`, `float` and `xcolor`. `latexmk -c` cleans up.

## Entry format

The macros are defined at the top of each `notebook.tex` and the web page parses them, so keep to them.
Entries are appended at the end, in date order:

```latex
\entry{D4. 1-bit 10T cell instead of the 2-bit cell}{2026-10-14}{d4}{Bitcell}
\field{Question} ...
\field{Options} ...
\field{Method} ... \file{scripts/bbox.rb} ...
\field{Result} ... \verify{claim not yet measured}
\field{Decision} ...
\field{Revisit if} ...
```

- **ID** (in the title): `D` decision, `M` measurement, `O` open, `T` tooling, numbered in order.
- **Date**: `YYYY-MM-DD`. A new date starts a new day heading in the PDF and a new day on the page.
- **Anchor**: the third argument, e.g. `danielvigna.com/notebook/sram-cim#d4`.
- **Topic**: the fourth argument, a short label such as `Bitcell` or `Verification`. The PDF lists
  entries by topic at the end (`\topicindex`), and the page can filter by it.
- `\file{}` paths under the project's `scripts/` and `data/` become links into this repo.
- The `\section*{Open items}` list feeds the project's "Now" block on the page.

## Adding a project

Copy a folder's `notebook.tex` preamble into a new folder, add the folder to the table above,
and add it to the project list on the site (`lib/notebook/projects.ts` in the site repo).
The PDF workflow picks up every `*/notebook.tex` automatically.

ASAP7 is © Arizona State University and Arm under its own license; no PDK files are included here.
