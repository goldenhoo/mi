import json
import tornado.web
from typing import Optional, Awaitable
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class HttpHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def get(self):
        """向第三方发送get请求"""
        http = AsyncHTTPClient()
        hr = HTTPRequest("http://127.0.0.1:8888/")
        resp = await http.fetch(hr)
        self.write(resp.body.decode())

    async def post(self):
        """向第三方发送post请求"""
        http = AsyncHTTPClient()
        hr = HTTPRequest(
            url="http://127.0.0.1:8888/api/user/login",
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            body=json.dumps({"username": "18850221201", "password": '123456'})
        )
        resp = await http.fetch(hr)
        self.write(resp.body.decode())