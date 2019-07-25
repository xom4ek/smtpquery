import asyncio
import time
import aiosmtplib
from classes import cfg, Email

def create_tasks(trs: list,fun):
    tasks=[]
    tasks=[]
    for tr in trs:
        tasks.append(asyncio.create_task(fun(tr)))
    return tasks

def tic():
    return '%1.1f' % (time.time() - start)

async def test(*args,**kwargs):
    print('test started work: {}'.format(tic()))
    res = await asyncio.sleep(1, result='test')
    print('test end work: {}'.format(tic()))
    return res

class SMTP:
    def __init__(self, hostname, port, username, password, use_tls = False):
        self.hostname=hostname
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.smtp = aiosmtplib.SMTP(
            hostname=self.hostname, port=self.port, use_tls=self.use_tls)

    async def connect(self):
        #Connect to smtp
        await self.smtp.connect()
        await self.smtp.auth_login(username=self.username, password=self.password)

        # send emails via creation connect
    async def sending(self,messages):
        result = []
        for task in create_tasks(messages, self.smtp.send_message):
            res = await task
            result.append(res)
        return result

async def main(cfg,messages):
    smtp=SMTP(**cfg.smtp)
    connect_task = asyncio.create_task(smtp.connect())
    await connect_task
    send_task = asyncio.create_task(smtp.sending(messages))
    response = await send_task
    print(response)

messages = []
for i in range(0, 5):
        body = '<p><br>Privet Тут и русский есть?Б<br>ya uje %sый<br>%s</p>' % (
            i, time.ctime())
        message = Email(**cfg.send, body=body,
                        subject="Test from aiosmtp %s" % i)
        messages.append(message)
start = time.time()
asyncio.run(main(cfg,messages))
#print(tic())
#print(200/float(tic()))

#Email1 = Email(**cfg.send, body=body, subject="Test from aiosmtp %s" % 1)
