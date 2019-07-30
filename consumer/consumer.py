#!/usr/bin/env python
import pika
import logging
import time
import json
from email_class import cfg,Email,SMTPe,Struct
LOGGER = logging.getLogger(__name__)
from jinja2 import Template

class Consumer(object):
    def __init__(self,url,queue,try_max=15):
        self.url=url
        self.queue=queue
        self.try_cnt=0
        self.try_max=try_max
        self.smtp=SMTPe(**cfg.smtp)
        self.smtp.create_conn()


    def get_delay(self):
            if self.try_cnt == 1:
                self.try_delay = 1
            else:
                self.try_delay += 1
            if self.try_delay > 30:
                self.try_delay = 30
            return self.try_delay

    def create_conn(self):
        LOGGER.info('Connecting to %s' % self.url)
        try:
            self.rabconn = pika.BlockingConnection(pika.URLParameters(url=self.url))
            self.ch = self.rabconn.channel()
            LOGGER.info('Queue declare %s' % self.queue)
            self.ch.queue_declare(queue=self.queue)
            self.ch.basic_qos(prefetch_count=1)
            self.ch.basic_consume(queue=self.queue, on_message_callback=self.callback)
        except Exception as e:
            LOGGER.info('Exception rise %s' % e.__str__)
            self.try_cnt=self.try_cnt+1
            try_delay=self.get_delay()
            time.sleep(try_delay)
            if self.try_cnt < self.try_max:
                self.create_conn()
            else:
                LOGGER.error(e)
                raise Exception
        return self.ch,self.rabconn

    def callback(self,ch, method, props, body):
        LOGGER.info('Start callback at message')
        message = json.loads(body.decode("utf-8"))
        LOGGER.info('Message get %s' % message)

        # SEND EMAIL OFC
        try:
            self.smtp,self.result = self.smtp.send_email(Email(
            to=message['to'],
            From=message['From'],
            body=Template(message['body']).render(message),
            subject=message['subject']))
        except Exception as e:
            LOGGER.error(e)
            raise Exception
        # END SEND EMAIL OFC

        LOGGER.info('Success sending message')
        LOGGER.info('Result %s' % self.result)
        if self.result == {}:
            response = {
                message['to']:(250,'Success sending')
            }
        else:
            response = self.result
        LOGGER.info('Message send %s' % message)
        ch.basic_publish(exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id = props.correlation_id),
                body=json.dumps(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def reconnect(self):
        try:
            self.ch.start_consuming()
        except Exception:
            self.create_conn()
            self.reconnect()
        except KeyboardInterrupt:
            raise KeyboardInterrupt

    def main(self):
        self.consumer=Consumer(url=self.url,queue=self.queue)
        self.consumer.create_conn()
        self.consumer.reconnect()


if __name__ == "__main__":
    from pprint import pprint
    LOGGER = logging.getLogger(__name__)
    LOG_FORMAT = ("{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}")
    logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)
    conn=Consumer(url='amqp://guest:guest@localhost:5672/%2F',queue='test')
    conn.create_conn()
    conn.reconnect()
