#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

program = []

# if len(sys.argv) != 2:
#     print(f"using {sys.argv[0]} requires a file")
# try:
#     with open(sys.argv[1]) as f:
#         for line in f:
#             # split line before and after comment symbol
#             comment_split = line.split("#")

#             # extract our number
#             num = comment_split[0].strip() # trim whitespace

#             if num == '':
#                 continue # ignore blank lines

#             # convert our binary string to a number
#             val = int(num, 2)

#             # print the val in bin and dec
#             # print(f"{val:08b}: {val:d}")
#             program.append(val)

# except FileNotFoundError:
#     print(f"{sys.argv[0]}: {sys.argv[1]} not found")
#     sys.exit(2)

# print(program)

cpu.load(program)
cpu.run()