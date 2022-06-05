from peewee import *
from app.models.BaseModel import BaseModel

# database = MySQLDatabase('teach', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '123456'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


# class BaseModel(Model):
#     class Meta:
#         database = database


class WqBingPhone(BaseModel):
    phone = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    sms_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    type = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    userid = IntegerField(null=True, unique=True)

    class Meta:
        table_name = 'wq_bing_phone'

