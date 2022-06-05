import os

base_path = os.path.abspath(os.path.dirname(__file__))
SETTINGS = {
    'static_path': os.path.join(base_path, 'application/static'),
    'static_url_prefix': '/static/',
    'debug': True,
}

JWT_SETTING = {
    'key': 'wangyi',
    'algorithm': 'HS256'
}

# [端口]
PORT = 8888
# PORT = 5000

# [数据库配置]
# mysql配置
MYSQL_CONFIG = {
    'database': 'teach',
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'minsize': 1,
    'maxsize': 4
}

# redis配置
REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': 6379,
    'password': "",
    'db': 0,
    'poolsize': 4
}

# [日志配置]
LOG_CONFIG = {
    # 版本号
    'version': 1,
    'disable_existing_loggers': False,
    # 定义格式化输出格式
    'formatters': {
        'simple': {
            'fmt': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    # 处理器,输出日志到文件以及位置
    'handlers': {
        # 控制台输出
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 日志文件输出
        'access': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': 'logs/access.log',
            'when': 'MIDNIGHT',
            'interval': 1,
            'backupCount': 180
        }
    },
    # 记录器,根据需求设置对应的日期对象
    'loggers': {
        # url请求信息输出
        'tornado.access': {
            'handlers': ['console', 'access'],
            'level': 'DEBUG'
        },
        'tornado.application': {
            'handlers': ['console', 'access'],
            'level': 'DEBUG'
        },
        'tornado.general': {
            'handlers': ['console', 'access'],
            'level': 'DEBUG'
        }
    }
}

# 文件上传目录
# UPLOADED_PHOTOS_DEST = '/static/upload'
UPLOADED_PHOTOS_DEST = os.path.join(os.path.dirname(__file__), "static/uploads")
UPLOADED_FILES_ALLOW = ['gif', 'jpg']