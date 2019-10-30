from scripts.color_detector import ColorDetector
from dotenv import load_dotenv
import os
import mysql.connector

if __name__ == '__main__':
    load_dotenv()
    measurements_db = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        passwd=os.getenv("PASSWORD")
    )
    color_detector = ColorDetector('')
