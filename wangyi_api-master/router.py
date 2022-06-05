from app.handlers import UserHandler
from tornado.web import RedirectHandler
from app.handlers.MysqlHandler import MysqlHandler
from app.handlers.RedisHandler import RedisHandler
from app.handlers.HttpHandler import HttpHandler
from app.handlers.FileHandler import FileHandler
from app.handlers.MessageHandler import PhoneBingHandler, PhoneSMSHandler
from app.handlers.ChildPhoneHandler import ChildPhoneHandler


handlers = [
    (r'/', RedirectHandler, dict(url="https://mini.minjiaotou.com")),
    ('/api/user/get/?', UserHandler.GetUserHandler),
    ('/api/user/login/?', UserHandler.LoginHandler),
    ('/api/user/loginup/?', UserHandler.LoginUPHandler),
    ('/api/user/register/?', UserHandler.RegisterHandler),
    ('/api/user/test/?', UserHandler.Test),
    (r'/api/mysql', MysqlHandler),
    (r'/api/redis', RedisHandler),
    (r'/api/request', HttpHandler),
    (r'/api/file', FileHandler),
    (r'/api/phone/bing', PhoneBingHandler),
    (r'/api/phone/sms', PhoneSMSHandler),
    (r'/api/child/more', ChildPhoneHandler),
]