"""
sample.py

Sample Script for serials_hold_validator.py
"""

import sys

import serials_hold_validator as shv

infile = open(sys.argv[1], "r", encoding="utf-8")
# infile = open("testinput.txt", "r", encoding="utf-8")
for line in infile:
    line = line.rstrip("\n")
    code, checked = shv.serials_hold_validator(line)
    print(code, checked)
