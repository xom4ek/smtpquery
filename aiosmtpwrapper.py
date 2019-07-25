import asyncio
import aiosmtplib
import logging
logging.basicConfig(filename="aios.log", level=logging.DEBUG, filemode='w')

class SMTPError(Exception):
    pass


class SMTP:

    def __init__(self, hostname, port, username, password, use_tls=True):
        self.loop = asyncio.get_event_loop()
        try:
            self.smtp = aiosmtplib.SMTP(hostname=hostname, port=port, loop=self.loop , use_tls=use_tls)
            self.loop.run_until_complete(self.smtp.connect())
            self.loop.run_until_complete(self.smtp._ehlo_or_helo_if_needed())
            self.loop.run_until_complete(self.smtp.auth_login(username=username, password=password))
        except Exception as e:
            print(e.__str__())

    def send(self, messages: list):
        self.tasks=[]
        for message in messages:
            self.tasks.append(self.loop.create_task(self.smtp.send_message(message)))
            try:
                result = self.loop.run_until_complete(self.tasks)
                print('message send')
            except (aiosmtplib.SMTPRecipientsRefused) as e:
                print(e.__str__())
            except (TypeError):
                print(e.__str__())
            except Exception as e:
                print(e.__str__())
        return result
            
    def __del__(self):
        try:
            self.loop.run_until_complete(self.smtp.quit())
        except Exception as e:
            print(e.__str__())


if __name__ == "__main__":
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import time
    from classes import cfg, Email
    messages=[]
    for i in range(0,5):
        body = '<p><br>Privet Тут и русский есть?Б<br>ya uje %sый<br>%s</p>' % (i,time.ctime())
        message = Email(to=cfg.smtp['username'],From=cfg.smtp['username'],body=body,subject="Test from aiosmtp %s" % i)
        messages.append(message)
    print(messages)
    test = SMTP(cfg.smtp['host'],cfg.smtp['port'],cfg.smtp['username'],cfg.smtp['password'],use_tls=True).send(messages)
    print(test)
