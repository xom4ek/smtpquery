#!/usr/bin/env python
import pika
import uuid
import logging
queue = 'test'


LOGGER = logging.getLogger(__name__)
class EmailRpcClient(object):
    def __init__(self,url,queue):
        self.url=url
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.URLParameters(url=self.url))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def sendEmail(self, text,to,subject):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body='{ "body":"%s", "to":"%s","From":"bonus@cbm.rt.ru", "subject":"%s"}' % (text,to,subject)
            )
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)

    def sendTemplate(self,*args,**kwargs):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(dict(**kwargs))
            )
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)



if __name__ == "__main__":
    LOG_FORMAT = ("{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}")
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    LOGGER.info('Start sending')
    email_rpc = EmailRpcClient("""amqp://guest:guest@localhost:5672/%2f""",'test')
    LOGGER.info(email_rpc.sendTemplate(text=str('<p>Privet from RabbitMQ</p>'),to='xom4ek-1994@yande.ru'),subject='Привет тема',template='./templates/template.html.j2')
