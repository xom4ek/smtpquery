#!/usr/bin/env python
import pika
import json
import logging
from aiosmtpwrapper import SMTP
from classes import Email,cfg,Struct

i = 1
connection = pika.BlockingConnection(pika.ConnectionParameters(
               cfg.rabbit['host'],cfg.rabbit['port']))
channel = connection.channel()
channel.queue_declare(queue='tasks',durable=True)
import time
from pprint import pprint

def callback(ch, method, properties, body):
    global i
    body=Struct(**json.loads(body.decode("utf-8")))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    i=i+1
    message=Email(to=body.to,
                    From=cfg.smtp['username'],
                    body=body.body,
                    subject=body.subject)
    print(SMTP(cfg.smtp['host'],cfg.smtp['port'],cfg.smtp['username'],cfg.smtp['password'],True).send([message,]))

channel.basic_consume(queue='tasks',
                      on_message_callback=callback)
channel.basic_qos(prefetch_count=1)
print('Start recives emails')
channel.start_consuming()