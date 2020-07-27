import roll
import re

res = roll.dice()
match = re.match(r'^(色子|骰子)$', msg)

if match: print(res)