import roll
import re

msg = '色子'
res = roll.dice()
match = re.match(r'^(色子|骰子)$', msg)

if match: print(res)