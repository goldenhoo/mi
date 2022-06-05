from typing import Optional, Awaitable

import aiomysql
import asyncio_redis
import tornado.locks
import tornado.gen
import tornado.web
from tornado import httputil
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from config import SETTINGS, REDIS_CONFIG, MYSQL_CONFIG, LOG_CONFIG, PORT
from router import handlers
from logging.config import dictConfig


async def __redis_init():
    return await asyncio_redis.Pool.create(
        host=REDIS_CONFIG["host"],
        port=REDIS_CONFIG["port"],
        db=REDIS_CONFIG["db"],
        password=REDIS_CONFIG["password"],
        poolsize=REDIS_CONFIG["poolsize"]
    )


async def __mysql_init():
    return await aiomysql.create_pool(
        host=MYSQL_CONFIG["host"],
        port=MYSQL_CONFIG["port"],
        minsize=MYSQL_CONFIG["minsize"],
        maxsize=MYSQL_CONFIG["maxsize"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        db=MYSQL_CONFIG["database"],
        cursorclass=aiomysql.cursors.DictCursor
    )


class Application(tornado.web.Application):
    # def __init__(self, mysql_db, redis_db):
    def __init__(self, mysql_db):
        # 配置日志
        dictConfig(LOG_CONFIG)

        # 数据库初始化配置
        self.mysql_db = mysql_db
        # self.redis_db = redis_db

        # 继承父类
        super(Application, self).__init__(handlers, **SETTINGS)


async def start_app():
    # redis_db = await __redis_init()
    mysql_db = await __mysql_init()
    # app = Application(mysql_db, redis_db)
    app = Application(mysql_db)
    # 单进程模式
    app.listen(PORT)

    # 多进程模式
    """
    http_server = HTTPServer(app)
    http_server.listen(PORT)
    http_server.start(0)
    """
    shutdown_event = tornado.locks.Event()
    await shutdown_event.wait()


if __name__ == '__main__':
    IOLoop.current().run_sync(start_app)
