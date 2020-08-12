'''
自定义功能：

在这里可以编写自定义的功能，
编写完毕后记得 git commit，

这个模块只是为了快速编写小功能，如果想编写完整插件可以使用：
https://github.com/richardchien/python-aiocqhttp
或者
https://github.com/richardchien/nonebot

关于PR：
如果基于此文件的PR，请在此目录下新建一个`.py`文件，并修改类名
然后在`yobot.py`中添加`import`（这一步可以交给仓库管理者做）
'''

import asyncio
import os
from typing import Any, Dict, Union
import random
import re

from aiocqhttp.api import Api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart

def dice():
    return random.randint(1, 6)


def russian_roll(in_roll_user_UID, msgs_after_begin, flag, UID=None, in_roll = 5):
    if UID == None: return None
    
    msg = ''

    if len(in_roll_user_UID) >= in_roll:  # 结束
        msg = '[CQ:at,qq={}] 你马没了'.format(in_roll_user_UID[random.randint(0, in_roll-1)])

        in_roll_user_UID.clear()
        msgs_after_begin = 0
        flag = 0
        
    
    elif msgs_after_begin >= 20:  # 消息数量超过结束
        msg = '[CQ:at,qq={}] 你马没了'.format(in_roll_user_UID[random.randint(0, len(in_roll_user_UID))])

        in_roll_user_UID.clear()
        msgs_after_begin = 0
        flag = 0
    
    else:
        in_roll_user_UID.append(UID)
        msg = '[CQ:at,qq={}] 你的马已经被塞到转盘里了'.format(UID)

    return msg


class Cus_reply:
    in_roll_user_UID = []
    buffed_msgs = 0
    flag = 0

    def __init__(self,
                 glo_setting: Dict[str, Any],
                 scheduler: AsyncIOScheduler,
                 app: Quart,
                 bot_api: Api,
                 *args, **kwargs):
        self.evn = glo_setting["verinfo"]["run-as"]
        self.path = glo_setting["dirname"]
        self.working_path = os.path.abspath(".")
        self.ver = glo_setting["verinfo"]
        self.setting = glo_setting
        self.api = bot_api


    def reset_status(self):
        self.flag = 0
        self.in_roll_user_UID.clear()
        self.buffed_msgs = 0


    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:

        MsgType = ctx['message_type']
        msg = ctx['raw_message']
        UID = ctx["sender"]["user_id"]
        if MsgType == "group":
            GID = ctx['group_id']
            Role = ctx['sender']['role']
        
        if self.buffed_msgs < 20: 
            self.buffed_msgs += 1
        else:
            self.buffed_msgs = 1

        reply = None
        # 设置回复文本
        if re.match(r'^镜华是谁[\S]?[\S]?', msg):
            reply = '[CQ:at,qq={}] 镜华是本群最可爱的{}~'.format(UID, 
                                                               ['机器人', '女仆'][random.randint(0,1)])
            
        elif re.match(r'^[\S]*斯哈斯哈[\S]*$', msg):
            reply = '[CQ:at,qq={}] 不许斯哈~'.format(UID)

        elif re.match(r'^(色子|骰子)$', msg):
            dice_res = dice()
            reply = '[CQ:at,qq={}] 本次投掷结果为{}'.format(UID, dice_res)

        # 俄罗斯转盘
        elif msg == '俄罗斯转盘' and self.flag == 0:
            self.reset_status()

            self.flag = 1  # 开始游戏
            reply = russian_roll(self.in_roll_user_UID, self.buffed_msgs, self.flag, UID)
        
        elif msg == '参加' and self.flag == 1:
            reply = russian_roll(self.in_roll_user_UID, self.buffed_msgs, self.flag, UID)

        else:
            return False

        # 统一回复
        if (reply is not None):
            await self.api.send_group_msg(
                group_id=GID,
                message=reply)

        else:
            return False

        # 返回布尔值：是否阻止后续插件（返回None视作False）
        return False
