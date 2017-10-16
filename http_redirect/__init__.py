import configparser
from aiohttp import web
from collections import defaultdict

import asyncio
import pathlib
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(pathlib.Path('/') / 'var' / 'log' / 'http_redirect' / 'web.log'),
            'maxBytes': 1024 * 1024 * 60,  # 20 MB
            'backupCount': 10,
        },
        'contact_file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(pathlib.Path('/') / 'var' / 'log' / 'http_redirect' / 'contact.log'),
            'maxBytes': 1024 * 1024 * 60,  # 20 MB
            'backupCount': 40,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'http_redirect.views.contact': {
            'handlers': ['console', 'contact_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

def load_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    result = defaultdict(dict)
    for s in config.sections():
        for o in config.options(s):
            result[s][o] = config.get(s, o)
    return result


loop = asyncio.get_event_loop()
app = web.Application(loop=loop, debug=False)

# load the configuration
app['config'] = load_config(str(pathlib.Path('.') / 'config' / 'common.ini'))
app['campains'] = load_config(str(pathlib.Path('.') / 'config' / 'campains.ini'))

# setup the routes
from .views import index, check, campain_redirect

router = app.router
router.add_get('/', index)
router.add_get('/g', check)
router.add_get('/api/v1/c/{campain_id}/r', campain_redirect)

if __name__ == '__main__':
    # start the server
    web.run_app(app, host='0.0.0.0', port=8180)
