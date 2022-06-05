import re
import uuid

from app.models.childPhone import WqChildPhone
from app.models.teach import WqUsers
from app.utils.message import to_dict_msg
from app.handlers.BaseHandler import BaseHandler
from config import JWT_SETTING
import jwt, sys, time, hashlib
from app.utils.login_require import login_require_async
import json
import requests
import random


class ChildPhoneHandler(BaseHandler):
    async def post(self):
        req_data = json.loads(self.request.body)
        phones = req_data.get('phones')

        for phone in phones:
            userid = req_data.get('userid')
            ret = re.match(r"^1[35678]\d{9}$", phone)
            if ret:
                print("匹配成功")
            else:
                continue

            wq_child_phone = None
            try:
                wq_child_phone = await self.manager.get(WqChildPhone, phone=phone, userid=userid)
                wq_child_phone.status = 1
                await self.manager.update(wq_child_phone)

            except Exception:
                print("no record")

            if wq_child_phone is None:
                wq_bing_phone = await self.manager.create(WqChildPhone, phone=phone, userid=userid)


        self.finish(to_dict_msg(code=200, msg='更多孩子手机增加成功'))


