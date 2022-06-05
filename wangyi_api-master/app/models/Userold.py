from peewee import *
from app import database
from datetime import datetime
from app.models.BaseModel import BaseModel

#
# class BaseModel(Model):
#     create_time = DateTimeField(default=datetime.now, verbose_name='创建时间')
#
#     def to_json(self) -> dict:
#         r = self.__data__
#         r['create_time'] = str(r['create_time'])
#         r['password'] = '******'
#         return r
#
#     class Meta:
#         database = database


class User(BaseModel):
    username = FixedCharField(max_length=11, verbose_name='账号')
    password = CharField(max_length=40, verbose_name='密码')

    class Meta:
        table_name = 'wq_users'