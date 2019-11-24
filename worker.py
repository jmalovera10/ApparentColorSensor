import datetime
import json
import os
import time

import mysql.connector
import pika
from dotenv import load_dotenv
from joblib import load

from scripts.color_detector import ColorDetector

load_dotenv('.env')
model = load('./models/polynomial_regression_1.joblib')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=os.getenv("QUEUE_NAME"), durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    image_meta_data = json.loads(body)
    process_image(image_meta_data)


def store_result(result, meta_data):
    # Connect to the database
    measurements_db = mysql.connector.connect(
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        database=os.getenv("MYSQL_DATABASE")
    )
    db_cursor = measurements_db.cursor(prepared=True)
    # Calculate the timestamp from string date
    timestamp = time.mktime(datetime.datetime.strptime(meta_data['exif']['DateTime'], "%Y:%m:%d %H:%M:%S").timetuple())
    db_cursor.execute(
        'INSERT INTO MEASUREMENTS(ID_USER, ID_SENSOR, VALUE_MEASURED, UNITS, MEASUREMENT_TIME, LATITUDE, LONGITUDE) '
        'VALUES (?,?,?,?,?,?,?)', [meta_data['ID_USER'], meta_data['ID_SENSOR'], result, 'UPC', timestamp,
                                   meta_data['LATITUDE'], meta_data['LONGITUDE']])
    measurements_db.commit()
    print db_cursor.lastrowid


def process_image(meta_data):
    try:
        color_detector = ColorDetector(meta_data['imagePath'])
        color = color_detector.process_image(False)
        color = map(int, color)
        result = model.predict([color])
        print 'RESULT: ', result[0], ' UPC'
        store_result(result[0], meta_data)

    except AttributeError as e:
        print 'Error processing image:'
        print e
    except KeyError as e:
        print 'ATTRIBUTE NOT FOUND'
        print e


channel.basic_consume(queue=os.getenv("QUEUE_NAME"), on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
