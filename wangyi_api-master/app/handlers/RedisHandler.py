from typing import Optional, Awaitable
from tornado.web import RequestHandler
from app.utils.response_format import resp_json


class RedisHandler(RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def get(self):
        """操作redis"""
        r = await self.application.redis_db.get("key")
        result = resp_json(data=r)
        self.write(result)