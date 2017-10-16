import aiosmtplib
import logging

from email.mime.text import MIMEText
from collections import namedtuple

logger = logging.getLogger('http_redirect.processing.alert')
SmtpConfig = namedtuple('SmtpConfig', ('hostname', 'username', 'password', 'port'))


async def alert(email_config:SmtpConfig, campain:dict, email:str):
    try:
        smtp = aiosmtplib.SMTP(hostname=email_config.hostname, port=int(email_config.port))
        await smtp.connect()
        if email_config.username:
            await smtp.login(username=email_config.username, password=email_config.password)
        message = MIMEText(f'{email} wants to be recontacted')
        message['From'] = campain['from_address']
        message['To'] = campain['address']
        message['Subject'] = campain['subject']

        await smtp.send_message(message)
    except:
        logger.exception('not able to send the mail')
