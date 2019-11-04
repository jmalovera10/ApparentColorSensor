from scripts.color_detector import ColorDetector
from dotenv import load_dotenv
import os
import mysql.connector
import pika

load_dotenv('.env')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=os.getenv("QUEUE_NAME"),durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue=os.getenv("QUEUE_NAME"), on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
