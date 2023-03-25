"""
SerialsHoldValidator.py

NACSIS-CATの雑誌所蔵の形式をチェックする
"""

import re
import sys


def SerialsHoldValidator(hlv):
    plus_mark = 0
    rtncd = 0
    checked_vol = ""
    checkd_split_vols = []
    if hlv == '*':
        checked_vol = '*'
        rtncd = 0
    else:
        if hlv.endswith("+"):
            hlv = hlv[:-1]
            plus_mark = 1
        for split_vol in hlv.split(";"):
            rtncd, checked_split_vol = check_vol(split_vol)
            checkd_split_vols.append(checked_split_vol)
        checked_vol = ';'.join(checkd_split_vols)
        if plus_mark:
            checked_vol = checked_vol + '+'
    return (rtncd, checked_vol)


def check_vol(vol):
    rtncd = 0
    switch = 0
    token = ""
    checked_vol = []
    start_tag = '<Ng>'
    end_tag = '</Ng>'

    for partOfVol in vol.split(","):
        number = ""
        # 4(4,3,5) のような形式に対応させる
        # 4(4
        if partOfVol.startswith('(') and partOfVol.endswith(')'):
            token = token + partOfVol + ','
            switch = 1
            next
        if switch == 1:
            # 5)
            if (not partOfVol.startswith('(')) and partOfVol.endswith(')'):
                partOfVol = token + partOfVol
                switch = 0
                token = ""
            # 3
            else:
                token = token + partOfVol + ','
                next
        if re.match("^\d+$", partOfVol):
            checked_vol.append(partOfVol)
        elif re.match("^\d+\-\d+$", partOfVol):
            checked_vol.append(partOfVol)
        elif re.match("^\d+\(.*\)$", partOfVol):
            checked_number = []
            number = partOfVol
            vol = re.search("^\d+", number).group()
            number = re.sub("^\d+\(", "", number)
            number = number[:-1]
            for partOfNumber in number.split(","):
                if re.match("^\d+$", partOfNumber):
                    checked_number.append(partOfNumber)
                elif re.match("^\d+\-\d+$", partOfNumber):
                    checked_number.append(partOfNumber)
                elif partOfNumber == "":
                    checked_number.append(partOfNumber)
                else:
                    rtncd = 1
                    work = start_tag + partOfNumber + end_tag
                    checked_number.append(work)
            work = vol + '(' + ','.join(checked_number) + ')'
            checked_vol.append(work)
        else:
            rtncd = 1
            work = start_tag + partOfVol + end_tag
            checked_vol.append(work)
    result = ','.join(map(str, checked_vol))
    return (rtncd, result)


if __name__ == '__main__':
    infile = open(sys.argv[1], "r", encoding="utf-8")
    # infile = open("testinput.txt", "r", encoding="utf-8")
    for line in infile:
        line = line.rstrip("\n")
        rtncd, checked_vol = SerialsHoldValidator(line)
        print(rtncd, checked_vol)
