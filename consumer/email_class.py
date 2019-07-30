from smtplib import SMTP as SMTPlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import logging

class Email(MIMEMultipart):
    def __init__(self,to,From,body,subject,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self['Subject'] = subject
        self['From'] =  From
        self['To'] =  to
        self.attach(MIMEText(body,'html'))
        LOGGER.debug('BODY %s' % body)
class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

def Get_config(config):
    import yaml
    with open(config) as f:
        return Struct(**yaml.safe_load(f))

cfg=Get_config('config.yml')
LOGGER = logging.getLogger(__name__)


class SMTP():
    def __init__(self,hostname,port,username,password,try_max=5,*args,**kwargs):
        self.username=username
        self.password=password
        self.hostname=hostname
        self.port= port
        self.password = password
        self.try_cnt=0
        self.try_max=try_max
        self.try_delay=0



    def maybe_reconnect(self,conn):
        try:
            self.reconnect = conn.noop()[0]
        except:
            self.reconnect = -1
        return True if self.reconnect == 250 else False


    def get_delay(self):
            if self.try_cnt == 1:
                self.try_delay = 1
            else:
                self.try_delay += 1
            if self.try_delay > 30:
                self.try_delay = 30
            return self.try_delay

    def create_conn(self):
        LOGGER.info('Connecting to %s' % self.hostname)
        self.conn = SMTPlib()
        try:
            self.conn.connect(self.hostname,self.port)
            self.conn.login(self.username,self.password)
        except Exception:
            self.try_cnt=self.try_cnt+1
            LOGGER.info('Try_cnt %s' % self.try_cnt)
            try_delay = self.get_delay()
            LOGGER.info('Try_delay %s' % try_delay)
            time.sleep(try_delay)
            if self.try_cnt < self.try_max:
                self.create_conn()
            else:
                LOGGER.info('Exception here')
                return Exception
        return self.conn

    def send_email(self,msg):
        self.try_cnt=0
        LOGGER.info('start send message')
        if not self.maybe_reconnect(self.conn):
            LOGGER.info('Reconnect')
            self.conn = self.create_conn()
        try:
            LOGGER.info('Just send')
            result = self.conn.send_message(msg)
            return self,result
        except Exception as e:
            return self,e


if __name__ == "__main__":
    LOG_FORMAT = ("{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}")
    LOGGER = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    smtp=SMTP(**cfg.smtp)
    smtp.create_conn()
    smtp,result = smtp.send_email(Email(to='Aleksey.a.lazarev@rt.ru',From='bonus@cbm.rt.ru',body='privet',subject='test tema'))
    LOGGER.info(result)
    time.sleep(1)
    smtp,result = smtp.send_email(Email(to='Aleksey.a.lazarev@rt.ru',From='bonus@cbm.rt.ru',body='privet2',subject='test tema'))
    LOGGER.info(result)
