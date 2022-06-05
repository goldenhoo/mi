import tornado.web
from typing import Optional, Awaitable
import logging
import os
from config import UPLOADED_PHOTOS_DEST
import time
import random

class FileHandler(tornado.web.RequestHandler):

    # def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
    #     pass

    async def post(self):
        """文件上传"""
        # logging.warning('data=', self.request)
        token = self.request.headers.get('token')
        if 'file' in self.request.files:
            file_obj = self.request.files['file'][0]
        try:
            # file_metas = self.request.body.
            file_metas = self.request.files['file']
            if len(file_metas) > 0:
                for meta in file_metas:
                    filename = meta['filename']

                    extName = filename.split('.').pop()


                    # 文件夹不存在时 创建
                    file_url = '/photos/' + time.strftime("%Y%m%d%H%M%S", time.localtime()) +\
                               str(random.randint(0, 9999)) + '.' + extName
                    fdir = UPLOADED_PHOTOS_DEST + '/photos/'
                    # if not os.path.exists(UPLOADED_PHOTOS_DEST + '/photos/'):
                    #     os.mkdir(UPLOADED_PHOTOS_DEST + '/photos/')
                    # 写入文件
                    # fd = os.open(UPLOADED_PHOTOS_DEST + file_url, os.O_RDWR | os.O_CREAT)
                    # os.write(fd, body)
                    filepath = UPLOADED_PHOTOS_DEST + file_url
                    # filepath = "./static/uploads" + file_url

                    # filepath = "./" + filename
                    with open(filepath, 'wb') as up:
                        up.write(meta['body'])
                self.write('finished!')
            else:
                self.write('请上传文件!')
        except:
            self.write('参数有误!')

    async def get(self):
        """文件下载"""
        self.set_header('Content-Type', 'application/octet-stream')
        with open('./1.txt', 'rb') as f:
            while True:
                data = f.read(100)
                if not data:
                    break
                self.write(data)
        # 记得要finish
        self.finish()