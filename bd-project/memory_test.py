#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:03:29 2019

@author: masudulhasanmasudb
"""

#!/usr/bin/env python

import sys
import time

if len(sys.argv) != 2:
    print ("usage: fillmem <number-of-megabytes>")
    sys.exit()

count = int(sys.argv[1])

megabyte = (0,) * (1024 * 1024 / 8)
print(megabyte)
data = megabyte * count

while True:
    time.sleep(1)