import time
import asyncio
from classes import cfg,Email
import aiosmtplib
start = time.time()

def tic():
    return 'at %1.1f seconds' % (time.time() - start)

class SMTP():
    def __init__(self, hostname=cfg.smtp['host'], port=cfg.smtp['port'], username=cfg.smtp['username'], password=cfg.smtp['password'], use_tls=False):
        print('START here')
        self.ioloop = asyncio.get_event_loop()
        self.smtp = aiosmtplib.SMTP(hostname=hostname, port=port, loop=self.ioloop,use_tls=use_tls)
        response = self.ioloop.run_until_complete(self.smtp.connect())
        print(response)
        response = self.ioloop.run_until_complete(self.smtp._ehlo_or_helo_if_needed())
        print(response)
        response = self.ioloop.run_until_complete(self.smtp.auth_login(username=username, password=password))
        print(response)
        self.fin_con=time.time
    # Try send emails with tasks
    def send(self,messages):
        print('With tasks')
        self.tasks=[]
        for message in messages:
            self.tasks.append(self.ioloop.create_task(self.smtp.send_message(message)))
        results = self.ioloop.run_until_complete(asyncio.wait(self.tasks))
        return results

    # def send(self,messages):
    #     print('Without tasks')
    #     results=[]
    #     for message in messages:
    #         res = self.ioloop.run_until_complete(self.smtp.send_message(message))
    #         results.append(res)
    #     return results

    def __del__(self):
        response = self.ioloop.run_until_complete(self.smtp.quit())
        print('del',response)
        print(tic())
        print('Total time for sending:',self.fin_con-time.time())
        self.ioloop.close()
    print('END here')

if __name__ == "__main__":
    body="<p>Privet</p>"
    messages=[]
    for i in range(0,20):
        message = Email(to=cfg.smtp['username'],From=cfg.smtp['username'],body=body,subject="Test from aiosmtp {}".format(i) )
        messages.append(message)
    SMTP().send(messages)