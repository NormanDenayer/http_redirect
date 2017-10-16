import logging
import asyncio

from aiohttp import web
from . import app
from .processing import alert, SmtpConfig

logger = logging.getLogger('http_redirect.views')
logger_contact = logger.getChild('contact')


async def index(request):
    return web.Response(text='Hello!')

async def check(request):
    raise web.HTTPFound('http://www.google.com')  # HTTPFound == 302


async def campain_redirect(request):
    campain_id = request.match_info.get('campain_id', None)
    if campain_id is None:
        logger.info('campain_redirect called without campain_id')
        raise web.HTTPNotFound()

    campain_cfg = app['campains'].get(campain_id, None)
    if campain_cfg is None:
        logger.warning(f'campain_id .{campain_id}. unknown')
        raise web.HTTPNotFound()

    # get the email provided
    email = request.query.get('email', None)

    if email is None:
        logger.warning(f'email not provided: {request.query}')
    else:
        # start a task but not waiting for it.
        logger_contact.info(f'trying to contact {campain_cfg["address"]} on behalf of {email}')
        config = app['config']['EMAIL_SMTP']
        smtp = SmtpConfig(hostname=config['hostname'], port=config.get('port', 25),
                          username=config.get('username', ''), password=config.get('password', ''))
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(alert(smtp, campain_cfg, email), loop=loop)

    raise web.HTTPFound(campain_cfg['redirect_url']) # HTTPFound == 302
