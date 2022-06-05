import json
import base64
from typing import Optional, Awaitable
from tornado import httputil
from tornado.web import RequestHandler
from app import manager
from app.utils.response_format import resp_json
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class Any:
    pass


class BaseHandler(RequestHandler):
    def __init__(
            self,
            application: "Application",
            request: httputil.HTTPServerRequest,
            **kwargs: Any
    ):
        super().__init__(application, request, **kwargs)
        self.manager = manager

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self) -> None:
        pass

    def set_default_headers(self) -> None:
        # 处理跨域请求
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')

    def write_error(self, status_code, **kwargs):
        """异常捕获"""
        message = str(kwargs["exc_info"])
        result = resp_json(code=status_code, error={"msg": message})
        self.write(result)

    def save_image(self, image_base64, image_path):
        """将文件保存"""
        with open(image_path, 'wb') as f:
            f.write(base64.b64decode(bytes(image_base64, encoding='utf-8')))

    def read_image(self, image_path):
        """获取文件base64"""
        with open(image_path, 'rb') as f:
            image_str = str(base64.b64encode(f.read()), encoding='utf-8')
        return image_str

    async def query_data(self, sql_params):
        """
        异步执行sql查询语句
        """
        result = []
        with (await self.application.mysql_db) as conn:
            cur = await conn.cursor()
            for sql, params in sql_params:
                await cur.execute(sql, params)
                r = await cur.fetchall()
                result.append(r)
            await cur.close()
            conn.close()
        return result

    async def alter_data(self, sql_params):
        """
        异步执行sql插入删除修改语句
        """
        with (await self.application.mysql_db) as conn:
            cur = await conn.cursor()
            try:
                for sql, params in sql_params:
                    await cur.execute(sql, params)
                await conn.commit()
                await cur.close()
                conn.close()
                return
            except:
                await conn.rollback()
                conn.close()
                raise Exception("数据库操作失败")

    async def query_data_one(self, sql, params=[]):
        """
        异步执行sql查询语句
        """
        with (await self.application.mysql_db) as conn:
            cur = await conn.cursor()
            await cur.execute(sql, params)
            result = await cur.fetchall()
            await cur.close()
            conn.close()
        return result

    async def alter_data_one(self, sql, params=[]):
        """
        异步执行sql插入删除修改语句
        """
        with (await self.application.mysql_db) as conn:
            cur = await conn.cursor()
            try:
                await cur.execute(sql, params)
                await conn.commit()
                await cur.close()
                conn.close()
                return
            except:
                await conn.rollback()
                conn.close()
                raise Exception("数据库操作失败")

    async def requests_http(self, url, method, data):
        """向第三方发送post请求"""
        http = AsyncHTTPClient()
        # 请求头设置
        headers = {
            "Content-Type": "multipart/form-data"
        }
        hr = HTTPRequest(
            url=url,
            method=method,
            headers=headers,  # 请求头指定参数类型,json格式提交
            body=json.dumps(data) if data else None  # 请求参数
        )
        resp = await http.fetch(hr)
        return json.loads(resp.body.decode())
