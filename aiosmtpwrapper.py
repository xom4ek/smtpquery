import asyncio
import time
import aiosmtplib
from message import cfg, Email

def create_tasks(trs: list,fun):
    tasks=[]
    for tr in trs:
        tasks.append(asyncio.create_task(fun(tr)))
    return tasks

def tic():
    return '%1.1f' % (time.time() - start)

def parts(a, n):
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

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
        res = await self.smtp.connect(timeout=10)
        print(res)
        res = await self.smtp._ehlo_or_helo_if_needed()
        print(res)
        res = await self.smtp.auth_login(username=self.username, password=self.password)
        print(res)
        

        # send emails via creation connect
    async def sending(self,messages):
        result = []
        for task in create_tasks(messages, self.smtp.send_message):
            res = await task
            result.append(res)
            if len(result) < 1:
                result =  Exception
        return result

    def __del__(self):
        pass
        #self.smtp.close()


async def smtpConnect(cfg,messages):
    smtp=SMTP(**cfg.smtp)
    connect_task = asyncio.create_task(smtp.connect())
    await connect_task
    send_task = asyncio.create_task(smtp.sending(messages))
    response = await send_task
    print(response)

async def main(cfg,messages,threads=3):
    threadTasks=[]
    messagesParts=parts(messages,threads)
    for i in range(0,threads):
        threadTasks.append(asyncio.create_task(smtpConnect(cfg,messagesParts[i])))
    for threadTask in threadTasks:
        await threadTask

if __name__ == "__main__":
    messages = []
    for i in range(0,25):
            body = '<p><br>Privet Тут и русский есть?Б<br>ya uje %sый<br>%s</p>' % (
                i, time.ctime())
            message = Email(**cfg.send, body=body,
                            subject="Test from aiosmtp %s" % i)
            messages.append(message)
    start = time.time()
    asyncio.run(main(cfg,messages,5))
#print(tic())
#print(200/float(tic()))

#Email1 = Email(**cfg.send, body=body, subject="Test from aiosmtp %s" % 1)