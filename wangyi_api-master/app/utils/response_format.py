import json
from datetime import date, datetime


# 响应状态码
class RET:
    OK = 0
    PARAMERR = 4000
    PARAMNUll = 4001
    USERERR = 4002
    FILEERR = 4003
    USERENOEXIST = 4004
    USERDELETE = 4005
    USERSTOP = 4006
    PASSWDERR = 4007
    NOAUTH = 4008
    AUTHFAILURE = 4009
    DATAINSERTERR = 5001
    DATADELETEERR = 5002
    DATAUPDATEERR = 5003
    DATASELECTERR = 5004
    NODATA = 5005
    DATAEXIST = 5006
    DBERR = 5007
    IOERR = 5008
    REQUESTERR = 5009
    UNKOWNERR = 5100


# 提示错误信息
error_map = {
    RET.OK: u"成功",
    RET.PARAMERR: u"参数错误",
    RET.PARAMNUll: u"缺少参数",
    RET.USERERR: u"用户登录失效",
    RET.FILEERR: u"文件格式错误",
    RET.USERENOEXIST: u"账户不存在",
    RET.USERDELETE: u"账户已注销",
    RET.USERSTOP: u"账户已停用",
    RET.PASSWDERR: u"验证失败",
    RET.NOAUTH: u"没有权限",
    RET.AUTHFAILURE: u"授权过期",
    RET.DATAINSERTERR: u"数据插入错误",
    RET.DATADELETEERR: u"数据删除错误",
    RET.DATAUPDATEERR: u"数据修改错误",
    RET.DATASELECTERR: u"数据查询错误",
    RET.NODATA: u"无数据",
    RET.DATAEXIST: u"用户已存在",
    RET.DBERR: u"数据库错误",
    RET.IOERR: u"文件读写错误",
    RET.REQUESTERR: u"请求失败",
    RET.UNKOWNERR: u"未知错误",
}


# 统一返回json格式
def resp_json(**kwargs):
    """响应格式"""
    if "data" not in kwargs:
        kwargs["data"] = ""
    if "code" not in kwargs:
        kwargs["code"] = RET.OK
        kwargs["message"] = ""
    else:
        if kwargs["code"] != RET.OK and "message" not in kwargs:
            kwargs["message"] = error_map[kwargs["code"]]

    return json.dumps(kwargs, cls=DateEncoder)


class DateEncoder(json.JSONEncoder):
    """解决json不能序列化时间问题"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)