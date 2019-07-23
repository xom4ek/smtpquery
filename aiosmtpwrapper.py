import asyncio
import aiosmtplib
import logging
logging.basicConfig(filename="aios.log", level=logging.DEBUG, filemode='w')

class SMTPError(Exception):
    pass


class SMTP:

    def __init__(self, hostname, port, username, password, use_tls=False):
        try:
            self.loop = asyncio.get_event_loop()
            self.smtp = aiosmtplib.SMTP(hostname=hostname, port=port, loop=self.loop , use_tls=use_tls)
            self.loop.run_until_complete(self.smtp.connect())
            self.loop.run_until_complete(self.smtp._ehlo_or_helo_if_needed())
            self.loop.run_until_complete(self.smtp.auth_login(username=username, password=password))
        except Exception as e:
            print(e.__str__())

    def send(self, messages: list):
        for message in messages:
            try:
                result = self.loop.run_until_complete(self.smtp.send_message(message))

            except (aiosmtplib.SMTPRecipientsRefused) as e:
                print(e.__str__())
            except (TypeError):
                pass
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
    from classes import cfg
    message = MIMEMultipart()
    message['Subject'] = 'Testivuu privet'
    message['From'] =  cfg.smtp['username']
    message['To'] = cfg.smtp['username']
    msghtml = MIMEText('<p><b>Privet!!<br>%s</p>' % time.ctime(), 'html')
    message.attach(msghtml)
    print(SMTP(cfg.smtp['host'],cfg.smtp['port'],cfg.smtp['username'],cfg.smtp['password'],True).send([message,]))
