import peewee_async
from config import MYSQL_CONFIG


database = peewee_async.MySQLDatabase(**MYSQL_CONFIG)
manager = peewee_async.Manager(database)
