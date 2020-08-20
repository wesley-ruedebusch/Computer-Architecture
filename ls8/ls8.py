#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# get our file name from sys
if len(sys.argv) != 2:
    print("Usage: ls8.py <path/filename>")
    sys.exit(2)
file = sys.argv[1]

cpu.load(file)
cpu.run()