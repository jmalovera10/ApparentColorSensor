from scripts.color_detector import ColorDetector
from dotenv import load_dotenv
import os
import mysql.connector
import pika
import json

load_dotenv('.env')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=os.getenv("QUEUE_NAME"), durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    image_meta_data = json.loads(body)
    process_image(image_meta_data)


def process_image(meta_data):
    color_detector = ColorDetector(meta_data['imagePath'])
    result = color_detector.process_image(False)
    print result


channel.basic_consume(queue=os.getenv("QUEUE_NAME"), on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
