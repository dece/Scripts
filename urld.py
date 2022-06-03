#!/usr/bin/env python3
# Delicate URL decoding of whatever string is passed as argument.

import sys
import urllib.parse


print(urllib.parse.unquote(sys.argv[1]))
