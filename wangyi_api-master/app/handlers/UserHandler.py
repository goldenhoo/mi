import uuid

from app.wtforms import UserForm, LoginUserForm
from app.models.Userold import User
from app.models.teach import WqUsers
from app.utils.message import to_dict_msg
from app.handlers.BaseHandler import BaseHandler
from config import JWT_SETTING
import jwt, sys, time, hashlib
from app.utils.login_require import login_require_async
import json
import requests


class RegisterHandler(BaseHandler):
    async def post(self):
        user_form = UserForm(self.request.arguments)
        if user_form.validate():
            # 验证用户是否存在
            try:
                username = user_form.username.data
                exist_user = await self.manager.get(User, username=username)
                if exist_user:
                    self.finish(to_dict_msg(code=500, msg='手机号已注册'))
            except:
                string = user_form.password.data
                sha1 = hashlib.sha1()
                sha1.update(string.encode('utf-8'))
                password = sha1.hexdigest()
                await self.manager.create(User, username=user_form.username.data, password=password)
                self.finish(to_dict_msg(code=200, msg='注册成功'))
        else:
            self.finish(to_dict_msg(code=500, msg='注册失败', **user_form.errors))


def get_user_info(js_code):
    req_params = {
        "appid": 'wxf6786fa2452fd1e3',  # 小程序的 ID
        "secret": 'e7ce5e9b7a6762471e20d7bc797c07bb',  # 小程序的 secret
        "js_code": js_code,
        "grant_type": 'authorization_code'
    }
    req_result = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                              params=req_params, timeout=3, verify=False)
    return req_result.json()


class LoginHandler(BaseHandler):
    async def post(self):


        req_data = json.loads(self.request.body)

        # js_code = req_data.get('js_code')
        js_code = req_data.get('code')

        # 这里是换取用户的信息

        user_info = get_user_info(js_code=js_code)
        openid = None

        try:
            openid = user_info['openid']
        except Exception:
            print("code error")
        if openid is None :
            self.finish(to_dict_msg(code=500, msg='code error'))

        session_key = user_info['session_key']
        user_uuid = str(uuid.uuid4())  # 暴露给小程序端的用户标示

        # 用来维护用户的登录态
        # User.save_user_session(
        #     user_uuid=user_uuid,
        #     openid=openid,
        #     session_key=session_key
        # )
        # 微信小程序不能设置cookie，把用户信息存在了 headers 中
        # self.set_header('Authorization', user_uuid)

        # 存储用户信息
        user = None
        # openid = "df"
        # user_uuid = "dfgfhhhd12"
        # session_key = "fdfgdg2"

        try:
            user = await self.manager.get(WqUsers, openid=openid)
        except Exception:
            print(" database error")
        if user is None:
            # 建立新用户
            user = await self.manager.create(WqUsers, openid=openid, uuid=user_uuid, session_key=session_key)
        else:
            # await self.manager.delete(user)
            user.uuid = user_uuid
            user.session_key = session_key
            await self.manager.update(user)
        # self.set_status(204)
        # payload = {
        #     'userid': user.id,
        #     'exp': int(time.time()) + 60 * 60 * 2
        #     # 86400 * 7
        # }
        # token = jwt.encode(payload, **JWT_SETTING)
        data = dict(openid=openid, uuid=user_uuid, session_key=session_key)
        self.finish(to_dict_msg(code=200, msg='登录成功', status=user.status, userid=user.id ,data=data))



class LoginUPHandler(BaseHandler):
    async def post(self):
        user_form = LoginUserForm(self.request.arguments)
        if user_form.validate():
            # 查数据
            try:
                string = user_form.password.data
                sha1 = hashlib.sha1()
                sha1.update(string.encode('utf-8'))
                password = sha1.hexdigest()
                #user = await self.manager.get(User, username=user_form.username.data, password=password)
                user = await self.manager.get(WqUsers, username=user_form.username.data, password=password)
                # user = await self.manager.get(WqUsers, id=7)

                # await self.manager.create(User, username="hoo", password=password)  //建立新用户

                payload = {
                    'username': user.username,
                    'exp': int(time.time()) + 60 * 60 * 3
                    # 86400 * 7
                }
                token = jwt.encode(payload, **JWT_SETTING)
                self.finish(to_dict_msg(code=200, msg='登录成功', token=token, username=user.username))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                self.finish(to_dict_msg(code=401, msg='用户名密码错误'))
        else:
            self.finish(to_dict_msg(code=401, msg='用户名密码不合法', **user_form.errors))


class GetUserHandler(BaseHandler):
    @login_require_async
    async def get(self):
        id = self._user_id
        try:
            # 有数据，将数据返回
            user = await self.manager.get(User, id=id)
            if user:
                self.finish(to_dict_msg(200, msg='查询用户数据成功', user=user.to_json()))
            else:
                self.finish(to_dict_msg(401, msg='非法用户'))
        except:
            self.finish(to_dict_msg(888, msg='数据库错误'))


class Test(BaseHandler):
    def get(self):
        token = self.request.headers.get('token')
        if token is not None:
            try:
                paylod = jwt.decode(token, JWT_SETTING['key'], [JWT_SETTING['algorithm']], options={'verify_exp': True},
                                    leeway=10)
                self.finish(to_dict_msg(200, msg=int(time.time()), data=paylod))
            except:
                self.finish(to_dict_msg(400, msg='token参数不合法或过期'))

        else:
            self.finish(to_dict_msg(403, msg='非法访问'))
