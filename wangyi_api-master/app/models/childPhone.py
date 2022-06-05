from peewee import *
from app.models.BaseModel import BaseModel


class UnknownField(object):
    def __init__(self, *_, **__): pass


class WqChildPhone(BaseModel):
    phone = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    userid = IntegerField(null=True, unique=True)

    class Meta:
        table_name = 'wq_child_phone'

