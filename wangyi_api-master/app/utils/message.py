code_msg = {
    200: '成功',
    500: '服务器内部错误'
}


def to_dict_msg(code=200, data=None, msg=None, **kwargs):
    return {
        "code": code,
        "data": data,
        "msg": msg if msg else code_msg.get(code),
        **kwargs
    }
