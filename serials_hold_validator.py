"""
serials_hold_validator.py

NACSIS-CATの雑誌所蔵の形式をチェックする
"""

import re
import sys

START_TAG = '<Ng>'
END_TAG = '</Ng>'


def serials_hold_validator(hlv):
    plus_mark = 0
    rtncd = 0
    checked_vol_all = ""
    checkd_split_vols = []
    if hlv == '*':
        checked_vol_all = '*'
    else:
        if hlv.endswith("+"):
            hlv = hlv[:-1]
            plus_mark = 1
        for split_vol in hlv.split(";"):
            rtncd_vol, checked_split_vol = check_vol(split_vol)
            if rtncd_vol == 1:
                rtncd = 1
            checkd_split_vols.append(checked_split_vol)
        checked_vol_all = ';'.join(checkd_split_vols)
        if plus_mark:
            checked_vol_all = checked_vol_all + '+'
    return (rtncd, checked_vol_all)


def check_vol(vol):
    rtncd = 0
    switch = 0
    token = ""
    checked_vol = []
    rtncd = 0
    part_of_vols = vol.split(",")
    part_of_vols_size = len(part_of_vols) - 1

    for i, part_of_vol in enumerate(part_of_vols):
        number = ""
        # 4(4,3,5) のような形式に対応させる
        # 4(4
        if (re.match(r"^\d+\(", part_of_vol)) and not (part_of_vol.endswith(')')):
            if i != part_of_vols_size:
                token = token + part_of_vol + ','
                switch = 1
                continue
        if switch == 1:
            # 5)
            if (not re.match(r"^\d+\(", part_of_vol)) and part_of_vol.endswith(')'):
                part_of_vol = token + part_of_vol
                switch = 0
                token = ""
            # 3
            elif i == part_of_vols_size:
                part_of_vol = token
            else:
                token = token + part_of_vol + ','
                continue
        if re.match(r"^\d+$", part_of_vol):
            checked_vol.append(part_of_vol)
        elif re.match(r"^\d+\-\d+$", part_of_vol):
            checked_vol.append(part_of_vol)
        elif re.match(r"^\d+\(\)\-\d+\(\)$", part_of_vol):
            checked_vol.append(part_of_vol)
        elif re.match(r"^\d+\(.*\)$", part_of_vol):
            checked_number = []
            number = part_of_vol
            vol = re.search(r"^\d+", number).group()
            number = re.sub(r"^\d+\(", "", number)
            number = number[:-1]
            for part_of_number in number.split(","):
                if re.match(r"^\d+$", part_of_number):
                    checked_number.append(part_of_number)
                elif re.match(r"^\d+\-\d+$", part_of_number):
                    checked_number.append(part_of_number)
                elif part_of_number == "":
                    checked_number.append(part_of_number)
                else:
                    rtncd = 1
                    work = START_TAG + part_of_number + END_TAG
                    checked_number.append(work)
            work = vol + '(' + ','.join(checked_number) + ')'
            checked_vol.append(work)
        else:
            rtncd = 1
            work = START_TAG + part_of_vol + END_TAG
            checked_vol.append(work)
    result = ','.join(map(str, checked_vol))
    return (rtncd, result)


if __name__ == '__main__':
    # infile = open(sys.argv[1], "r", encoding="utf-8")
    infile = open("testinput.txt", "r", encoding="utf-8")
    for line in infile:
        line = line.rstrip("\n")
        code, checked = serials_hold_validator(line)
        print(code, checked)