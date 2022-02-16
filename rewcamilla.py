#!/usr/bin/env python
# Currently only works with peaking filters.

import argparse

parser = argparse.ArgumentParser(
    description="Convert REW Generic EQ files to filters and a pipeline for CamillaDSP."
)
parser.add_argument("input", help="Generic EQ .txt file from REW.")
parser.add_argument(
    "-g",
    "--gain",
    help="add gain reduction filter equal to maximum peak gain.",
    action="store_true",
)

args = parser.parse_args()

with open(args.input, "r") as f:
    data = [l.rstrip("\n") for l in f.readlines()]

filters = []
hg = 0

for line in data:
    if ("Filter" in line) and ("ON" in line):
        l = line[line.find("Fc") + 2 :]
        freq = float(l[: l.find("Hz")])
        gain = l[l.find("Gain") + 4 :]
        gain = float(gain[: gain.find("dB")])
        if args.gain and gain > hg:
            hg = gain
        q = float(l[l.find("Q") + 1 :])
        filters.append([freq, gain, q])

filterstr = "filters:\n"
if args.gain:
    filterstr += f"\teqgain:\n\t\ttype: Gain\n\t\tparameters:\n\t\t\tgain: -{hg}\n\t\t\tinverted: false\n"

pipelinestr = "pipeline:\n"

ch0 = ""
ch1 = ""
if args.gain:
    ch0 = "\t- type: Filter\n\t  channel: 0\n\t  names:\n\t  \t- eqgain\n"
    ch1 = "\t- type: Filter\n\t  channel: 1\n\t  names:\n\t  \t- eqgain\n"

for filter in filters:
    filterstr += f"\tpeak_{int(filter[0])}:\n"
    filterstr += "\t\ttype: Biquad\n\t\tparameters:\n\t\t\ttype: Peaking\n"
    filterstr += (
        f"\t\t\tfreq: {int(filter[0])}\n\t\t\tq: {filter[2]}\n\t\t\tgain: {filter[1]}\n"
    )
    ch0 += f"\t  \t- peak_{int(filter[0])}\n"
    ch1 += f"\t  \t- peak_{int(filter[0])}\n"

pipelinestr += ch0 + ch1


out = filterstr + "\n\n\n" + pipelinestr
print(out.replace("\t", "    "))
