from dotenv import load_dotenv
import os
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

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

    # Retrieve calculated data from all UPC measurements
    query = 'SELECT UPC, ROUND(AVG(H)) AS H_AVG, ROUND(AVG(S)) AS S_AVG, ROUND(AVG(V)) AS V_AVG, ' \
            'AVG(H*H)-AVG(H)*AVG(H) AS H_VAR, AVG(S*S)-AVG(S)*AVG(S) AS S_VAR, AVG(V*V)-AVG(V)*AVG(V) AS V_VAR, ' \
            'SQRT(AVG(H*H)-AVG(H)*AVG(H)) AS H_DEV, SQRT(AVG(S*S)-AVG(S)*AVG(S)) AS S_DEV, SQRT(AVG(V*V)-AVG(V)*AVG(V)) AS V_DEV FROM CALIBRATION GROUP BY UPC'
    db_cursor.execute(query)

    # Gets all results for each UPC including AVG, VAR and STD DEV
    results = db_cursor.fetchall()
    # for res in results:

