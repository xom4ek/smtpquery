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


async def connect(hostname, port, username, password, use_tls=False,*args,**kwargs):
    #Connect to smtp
    smtp = aiosmtplib.SMTP(hostname=hostname, port=port, use_tls=False)
    await smtp.connect()
    await smtp.auth_login(username=username, password=password)
    return smtp

    # send emails via creation connect
async def send(smtp,messages):
    result = []
    for task in create_tasks(messages, smtp.send_message):
        res = await task
        result.append(res)
    return result

async def main(cfg,messages):
    connect_task = asyncio.create_task(connect(**cfg.smtp))
    smtp = await connect_task
    send_task = asyncio.create_task(send(smtp,messages))
    response = await send_task
    print(response)
    # task2 = asyncio.create_task(send())

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
