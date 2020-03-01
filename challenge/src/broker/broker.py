#!/usr/bin/env python3

import pika
from typing import Dict
import json
import pandas as pd

_TIMESTAMP_FORMAT = '%d.%m.%Y %H:%M:%S'


class Publisher:
    """ Used by HHSim to publish simulated control and meter data."""

    connection: pika.BlockingConnection
    channel: pika.BlockingConnection.channel

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='tmhchallenge')

    def send_data(self, timestamp: pd.Timestamp, power):
        msg = json.dumps({'topic': 'data',
                          'payload': {'timestamp': timestamp.strftime(_TIMESTAMP_FORMAT),
                                      'power': power}})
        self.channel.basic_publish(exchange='', routing_key='tmhchallenge', body=msg)
        print(f"[x] Sent '{msg}'")

    def send_ctrl(self, ctrl_str):
        msg = json.dumps({'topic': 'ctrl', 'payload': ctrl_str})
        self.channel.basic_publish(exchange='', routing_key='tmhchallenge', body=msg)
        print(f"[x] Sent '{msg}'")

    def close(self):
        self.connection.close()


class Subscriber:
    """ Used by PVSim to listen for incoming control or meter data.
        When a new data package arrives, the corresponding callback of PVSim is executed."""
    connection: pika.BlockingConnection
    channel: pika.BlockingConnection.channel
    callbacks: Dict

    def __init__(self, callback_ctrl, callback_data):
        self.callbacks = {'ctrl': callback_ctrl,
                          'data': callback_data}

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='tmhchallenge')
        self.channel.basic_consume(queue='tmhchallenge', on_message_callback=self.callback, auto_ack=True)

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        msg = json.loads(body)
        if msg['topic'] == 'data':
            self.callbacks['data'](pd.Timestamp(msg['payload']['timestamp']), msg['payload']['power'])
        elif msg['topic'] == 'ctrl':
            self.callbacks['ctrl'](msg['payload'])

    def close(self):
        self.channel.stop_consuming()
        self.connection.close()


def _test_subscriber_callback(*args):
    print(args)


if __name__ == '__main__':
    publisher = Publisher()
    subscriber = Subscriber(_test_subscriber_callback, _test_subscriber_callback)
    publisher.send_data(pd.Timestamp('2019-06-29 12:00:00'), 1.23)
    publisher.send_ctrl("Test")
    publisher.close()
    subscriber.run()
    subscriber.close()
