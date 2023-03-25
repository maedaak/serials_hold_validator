"""
sample.py

Sample Script for SerialsHoldValidator.py
"""

import sys

import SerialsHoldValidator as SHV

# infile = open(sys.argv[1], "r", encoding="utf-8")
infile = open("testinput.txt", "r", encoding="utf-8")
for line in infile:
    line = line.rstrip("\n")
    rtncd, checked_vol = SHV.SerialsHoldValidator(line)
    print(rtncd, checked_vol)
