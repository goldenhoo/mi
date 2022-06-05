from typing import Optional, Awaitable
import tornado.web
from app.utils.response_format import resp_json


class MysqlHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def execute(self, sql, *args):
        """
        异步执行sql语句
        """
        with (await self.application.mysql_db) as conn:
            cur = await conn.cursor()
            await cur.execute(sql, args)
            result = await cur.fetchall()
            await cur.close()
            conn.close()
        return result

    async def get(self):
        """操作mysql"""
        data = await self.execute("select * from wq_users limit 10")
        result = resp_json(data=data)
        self.write(result)
        # self.write后调用self.finish(),意味服务与前端链接终结,但是服务可以继续做其他事情
        # 如果没有主动调用self.finish(), 当前函数get()执行完毕就会调用self.on_finish()
        self.finish()
        print("已经将数据返回给前端,我可以继续干别的事情")