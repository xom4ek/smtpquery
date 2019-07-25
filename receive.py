#!/usr/bin/env python
import pika
import json
import logging
import asyncio
from aiosmtpwrapper import SMTP
from message import Email,cfg,Struct

i = 1
smtp=SMTP(**cfg.smtp)
async def connectEstablish(cfg,smtp=smtp):
    connect_task = asyncio.create_task(smtp.connect())
    res = await connect_task
    print(res)
loop = asyncio.get_event_loop()
loop.run_until_complete(connectEstablish(cfg))

connection = pika.BlockingConnection(pika.ConnectionParameters(
               **cfg.rabbit))
channel = connection.channel()
channel.queue_declare('test',durable=True)

def callback(ch, method, properties, body,loop=loop,smtp=smtp):
    body=Struct(**json.loads(body.decode("utf-8")))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    message=Email(to=body.to,
                    From=cfg.smtp['username'],
                    body=body.body,
                    subject=body.subject)
    try:
        asyncio.gather()
        res = loop.run_until_complete(smtp.sending([message,]))
        print(res)
    except Exception as e:
        print(e.__str__())
        loop.run_until_complete(connectEstablish(cfg))
        res = loop.run_until_complete(smtp.sending([message,]))
        print(res)

channel.basic_consume(queue='tasks',
                      on_message_callback=callback)
channel.basic_qos(prefetch_count=1)




print('Start recives emails')
channel.start_consuming()