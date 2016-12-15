import re
s = "done 0x00 Running -14.471272dB"
m = re.search(r'-(\d+)\.(\d+)', s)
print m.group(0)