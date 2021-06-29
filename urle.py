#!/usr/bin/env python3
# Brutal URL encoding of whatever string is passed as argument.

import binascii
import sys

s = sys.argv[1].encode()
h = binascii.hexlify(s).decode()
encoded = ""
for i in range(len(h) // 2):
    byte = h[i * 2 : i * 2 + 2]
    encoded += "%" + byte
print(encoded)
