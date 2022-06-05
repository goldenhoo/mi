from peewee import *
from app import database
from datetime import datetime


class BaseModel(Model):
    # create_time = DateTimeField(default=datetime.now, verbose_name='创建时间')

    def to_json(self) -> dict:
        r = self.__data__
        # r['create_time'] = str(r['create_time'])
        r['password'] = '******'
        return r

    class Meta:
        database = database




