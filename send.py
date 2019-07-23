#!/usr/bin/env python
import pika
import logging
import aiosmtpwrapper
import time
from classes import cfg

logging.basicConfig(filename="sample.log", level=logging.DEBUG)

connection = pika.BlockingConnection(pika.ConnectionParameters(
               cfg.rabbit['host'],cfg.rabbit['port'])
channel = connection.channel()
channel.queue_declare(queue='tasks',durable=True)

import sys



while True:
    time.sleep(10)
    message = '{ "body":"Сейчас %s  <br>Удивительно!", "to":"%s", "subject":"Тестовая тема"}' % (time.ctime(),cfg.smtp['username'])
    channel.basic_publish(exchange='',
                        routing_key='tasks',
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode=2
                        ))
    print (" [x] Sent %r" % (message,))

connection.close()