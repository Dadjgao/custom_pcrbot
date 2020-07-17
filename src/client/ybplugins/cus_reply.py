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


class Cus_reply:
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

    async def execute_async(self, ctx: Dict[str, Any]) -> Union[None, bool, str]:

        MsgType = ctx['message_type']
        msg = ctx['raw_message']
        if MsgType == "group":
            GID = ctx['group_id']
            Role = ctx['sender']['role']

        reply = None

        # 设置回复文本
        if (re.match(r'^(镜华)?([Xx]cw)?[\S]?$', msg)):
            reply = ['变态！叫我干嘛！爬爬爬', 
                     '呐，你叫我是想干什么呢？', 
                     '镜华累了，镜华不想说话。',
                     ][random.randint(0,2)]
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
