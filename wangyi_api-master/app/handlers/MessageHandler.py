import re
import uuid

from app.models.bingPhone import WqBingPhone
from app.models.teach import WqUsers
from app.utils.message import to_dict_msg
from app.handlers.BaseHandler import BaseHandler
from config import JWT_SETTING
import jwt, sys, time, hashlib
from app.utils.login_require import login_require_async
import json
import requests
import random


class PhoneSMSHandler(BaseHandler):
    async def post(self):
        req_data = json.loads(self.request.body)
        phone = req_data.get('phone')
        userid = req_data.get('userid')
        ret = re.match(r"^1[35678]\d{9}$", phone)
        if ret:
            print("匹配成功")
        else:
            print("匹配失败")
            self.finish(to_dict_msg(code=500, msg='手机号错误'))
            return

        # 用randint()
        code = ''
        for i in range(6):
            n = random.randint(0, 9)
            code += str(n)
        # print(code)
        wq_bing_phone = None
        try:
            wq_bing_phone = await self.manager.get(WqBingPhone, phone=phone)
            wq_bing_phone.status = 1
            wq_bing_phone.userid = userid
            wq_bing_phone.sms_code = code
            await self.manager.update(wq_bing_phone)

        except Exception:
            print("no record")

        if wq_bing_phone is None:
            wq_bing_phone = await self.manager.create(WqBingPhone, phone=phone, sms_code=code,
                                                      userid=userid, status=1, type=1)
        # sendsms(phone,code)
        self.finish(to_dict_msg(code=200, msg='短信发送成功'))


class PhoneBingHandler(BaseHandler):
    async def post(self):
        req_data = json.loads(self.request.body)
        phone = req_data.get('phone')
        sms_code = req_data.get('sms_code')
        try:
           wq_bing_phone = await self.manager.get(WqBingPhone, phone=phone)
        except Exception:
            print(Exception.with_traceback())
            return
        if wq_bing_phone:
            if wq_bing_phone.sms_code == sms_code and wq_bing_phone.status == 1:
                try:
                    user = await self.manager.get(WqUsers, id=wq_bing_phone.userid)
                    user.phone = phone
                    await self.manager.update(user)
                    wq_bing_phone.status = 0
                    await self.manager.update(wq_bing_phone)
                except Exception:
                    print(" database error")
            else:
                self.finish(to_dict_msg(code=500, msg='数据错误'))
        self.finish(to_dict_msg(code=200, msg='绑定成功'))

