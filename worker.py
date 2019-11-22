from scripts.color_detector import ColorDetector
from dotenv import load_dotenv
import os
import mysql.connector
import pika
import json
from joblib import load

load_dotenv('.env')
model = load('./models/polynomial_regression_1.joblib')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=os.getenv("QUEUE_NAME"), durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    image_meta_data = json.loads(body)
    process_image(image_meta_data)


def process_image(meta_data):
    color_detector = ColorDetector(meta_data['imagePath'])
    color = color_detector.process_image(False)
    result = model.predict(color)
    print result


channel.basic_consume(queue=os.getenv("QUEUE_NAME"), on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
