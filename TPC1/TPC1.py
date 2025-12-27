''' ^1*(0|01)*$ '''

import re

pattern = re.compile(r'^1*(0|01)*$')

tests = [
    "1111111",
    "000001",
    "1111010101000",
    "111010110111",
    "011",
    "00000001100000000"
    "0010101010101",
    "10",
    "1100",
    "1011",
    "0001",
    "0100",
]

for s in tests:
    if pattern.fullmatch(s):
        print(f"{s} OK")
    else:
        print(f"{s} FAIL")
