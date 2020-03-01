import pika

class Publisher:
    connection: pika.BlockingConnection
    channel: None

    def __init__(self):
        # Create a new instance of the Connection object
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Create a new channel with the next available channel number or pass in a channel number to use
        self.channel = self.connection.channel()
        # Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
        self.channel.queue_declare(queue='hello')

    def send(self):
        self.channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
        print("[x] Sent 'Hello World!'")

    def close(self):
        self.connection.close()


class Subscriber:
    connection: pika.BlockingConnection
    channel: None

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='hello')
        self.channel.basic_consume('hello', self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)


if __name__ == '__main__':
    subscriber = Subscriber()
    publisher = Publisher()
    publisher.send()