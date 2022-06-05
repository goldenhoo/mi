from functools import wraps
from config import JWT_SETTING
import jwt
from app.models import User
from app.utils.message import to_dict_msg
"""
functools模块用于高阶函数，即参数或返回值为其他函数的函数，此模块的功能适用于所有可调用对象
@wraps装饰器：任何时候定义装饰器，都应使用wraps，可以保留装饰的函数的元信息：比如名字，文档字符串，注解和参数签名

因为使用装饰器, 原函数(即被装饰函数)的地址指向了装饰器所定义的内部inner函数
可以借助functools.warps函数, 避免属性篡改问题
verify_exp 校验过期时间
leeway 延后
"""


def login_require_async(func):
    @wraps(func)
    async def wrapper(self, *arg, **kwargs):
        # 验证用户是否登录
        token = self.request.headers.get('token')
        if token is not None:
            try:
                paylod = jwt.decode(token, JWT_SETTING['key'], [JWT_SETTING['algorithm']], options={'verify_exp': True},
                                    leeway=10)
                username = paylod.get('username')
                # 有数据，将数据返回
                try:
                    user = await self.manager.get(User, username=username)
                    self._user_name = user.username
                    self._user_id = user.id
                    try:
                        await func(self, *arg, **kwargs)
                    except:
                        self.finish(to_dict_msg(500, msg='服务器内部错误'))
                except:
                    self.finish(to_dict_msg(401, msg='用户不存在'))
            except:
                self.finish(to_dict_msg(400, msg='token参数不合法或已过期'))

        else:
            self.finish(to_dict_msg(403, msg='非法访问'))

    return wrapper
