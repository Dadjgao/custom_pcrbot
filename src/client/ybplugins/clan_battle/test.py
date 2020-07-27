import re
cmd = "下树"

match = re.match(r'^取消(?:预约)?([1-5]|挂树)$', cmd) or re.match(r'^下([0]|树)$', cmd)

b = match.group(1)

print(cmd, b)

# if b == '挂树' or '树':
#     boss_num = 0
#     event = b