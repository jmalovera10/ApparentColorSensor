from scripts.color_detector import ColorDetector
from dotenv import load_dotenv
import os
import mysql.connector

if __name__ == '__main__':
    # Load environment variables
    load_dotenv('.env')
    # Connect to the database
    measurements_db = mysql.connector.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE")
    )
    db_cursor = measurements_db.cursor(prepared=True)
    color_detector = ColorDetector('')
    # Current UPC available samples
    upc = [1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 90, 100, 110, 150, 200, 250]
    for ref in upc:
        for sample in range(1, 5):
            # Iterate through the samples and store the results in the database
            color_detector.set_image_path('samples/UPC_%d_SAMPLE_%d.JPG' % (ref, sample))
            (h, s, v) = color_detector.process_image(debug_image=False)
            db_cursor.execute('INSERT INTO CALIBRATION(UPC,SAMPLE,H,S,V) VALUES (?,?,?,?,?)', [ref, sample, h, s, v])
            measurements_db.commit()
            print 'FINISHED: UPC %d, SAMPLE %d' % (ref, sample)
    db_cursor.close()
    measurements_db.close()
