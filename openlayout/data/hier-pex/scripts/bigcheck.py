"""Sanity of a large windowed PEX netlist of a labelled SRAMCIMsbc tile:
- every node has a DC path (resistors / transistor channels) to a pin or a supply, none only on capacitors;
- every multi-node net's R network is one piece;
- per-net totals against a small tile scaled: WL_r per cell, BL_c / BLB_c per row, XB / P per cell.
  bigcheck.py <big.pex.spice> <rows> <cols> <small.pex.spice> <small rows> <small cols>"""
import re
import statistics
import sys
from collections import defaultdict


def parse(path):
    totals, pins, R, devs, Cnodes = {}, [], [], [], set()
    for l in open(path):
        if l.startswith("* total capacitance per net"):
            totals = {a.split()[0]: float(a.split()[1]) for a in l.split(":", 1)[1].split(",")}
        elif l.startswith(".subckt"):
            pins = l.split()[2:]
        elif l.startswith("R"):
            t = l.split()
            R.append((t[1], t[2]))
        elif l.startswith("N"):
            t = l.split()
            devs.append(t[1:5])
        elif l.startswith("C"):
            t = l.split()
            Cnodes.update(t[1:3])
    return totals, pins, R, devs, Cnodes


big, R0, C0 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
small, R1, C1 = sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
totals, pins, R, devs, Cnodes = parse(big)
parent = {}


def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    parent[find(a)] = find(b)


for a, b in R:
    union(a, b)
for d, g, s, b in devs:
    union(d, s)                                   # the channel: a DC path between drain and source
    find(g), find(b)
roots = {find(p) for p in pins}
nodes = set(parent) | Cnodes
dc_less = [n for n in nodes if find(n) not in roots]
cap_only = [n for n in Cnodes if n not in parent]
print(f"{big}: {len(pins)} pins, {len(nodes)} nodes, {len(R)} resistors, {len(devs)} transistors, {len(Cnodes)} nodes with capacitors")
print(f"  nodes on capacitors only (floating): {len(cap_only)} {cap_only[:5]}")
print(f"  nodes without a DC path to a pin: {len(dc_less)} {dc_less[:5]}")
# each net's R network in one piece: group nodes by net name prefix (<net> or <net>_<k>)
by_net = defaultdict(set)
for n in parent:
    m = re.fullmatch(r"(.+?)(?:_(\d+))?", n)
    base = n if n in totals else (re.sub(r"_\d+$", "", n) if re.sub(r"_\d+$", "", n) in totals else None)
    if base:
        by_net[base].add(n)
rgraph = defaultdict(set)
for a, b in R:
    rgraph[a].add(b)
    rgraph[b].add(a)
split = []
for net, ns in by_net.items():
    if len(ns) < 2:
        continue
    seen, todo = set(), [next(iter(ns))]
    while todo:
        x = todo.pop()
        if x in seen:
            continue
        seen.add(x)
        todo += [y for y in rgraph[x] if y in ns]
    if seen != ns:
        split.append(net)
print(f"  nets whose R network is in more than one piece: {len(split)} {split[:5]}")

st = parse(small)[0]
print(f"per-net totals against {small} ({R1}x{C1}), scaled:")


def group(t, pat):
    return [v for k, v in t.items() if re.fullmatch(pat, k)]


rows = [("WL per cell (WL_r / cols)", [v / C0 for v in group(totals, r"WL_\d+")], [v / C1 for v in group(st, r"WL_\d+")]),
        ("BL per row (BL_c / rows)", [v / R0 for v in group(totals, r"BL_\d+")], [v / R1 for v in group(st, r"BL_\d+")]),
        ("BLB per row", [v / R0 for v in group(totals, r"BLB_\d+")], [v / R1 for v in group(st, r"BLB_\d+")]),
        ("XB per cell", group(totals, r"XB_\d+_\d+"), group(st, r"XB_\d+_\d+")),
        ("P per cell", group(totals, r"P_\d+_\d+"), group(st, r"P_\d+_\d+")),
        ("VDD rail per cell (VDD_k / cols)", [v / C0 for v in group(totals, r"VDD_\d+")], [v / C1 for v in group(st, r"VDD_\d+")])]
for name, b, s in rows:
    if b and s:
        print(f"  {name:34s} big: n={len(b):5d} median {statistics.median(b):.4f} fF (min {min(b):.4f}, max {max(b):.4f})"
              f"   small: median {statistics.median(s):.4f} fF   ratio {statistics.median(b) / statistics.median(s):.3f}")
