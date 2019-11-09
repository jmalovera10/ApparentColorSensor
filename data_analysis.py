# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os
import mysql.connector
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys
from getopt import getopt
from sklearn.linear_model import LinearRegression


def average_characterization(data):
    print 'AVERAGE_CHARACTERIZATION'
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter([UPC for UPC, H, S, V in data], [H for UPC, H, S, V in data], [S for UPC, H, S, V in data], zdir='z',
               label='CARACTERIZACION PROTOTIPO 1')
    ax.set_xlabel('UPC')
    ax.set_ylabel('HUE')
    ax.set_zlabel('SATURATION')
    ax.legend()

    plt.show()


def multiple_regression(data):
    x = [[H, S] for UPC, H, S, V in data]
    y = [[UPC] for UPC, H, S, V in data]
    model = LinearRegression()
    model.fit(x, y)
    print('H, S, V Coefficients: ', model.coef_)
    print('Intercept: ', model.intercept_)


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
    '''
    query = 'SELECT UPC, ROUND(AVG(H)) AS H_AVG, ROUND(AVG(S)) AS S_AVG, ROUND(AVG(V)) AS V_AVG, ' \
            'AVG(H*H)-AVG(H)*AVG(H) AS H_VAR, AVG(S*S)-AVG(S)*AVG(S) AS S_VAR, AVG(V*V)-AVG(V)*AVG(V) AS V_VAR, ' \
            'SQRT(AVG(H*H)-AVG(H)*AVG(H)) AS H_DEV, SQRT(AVG(S*S)-AVG(S)*AVG(S)) AS S_DEV, SQRT(AVG(V*V)-AVG(V)*AVG(V)) AS V_DEV FROM CALIBRATION GROUP BY UPC'
    db_cursor.execute(query)
    '''
    query = 'SELECT UPC, H, S, V FROM CALIBRATION'
    db_cursor.execute(query)
    # Gets all results for each UPC including AVG, VAR and STD DEV
    results = db_cursor.fetchall()
    data = []

    for res in results:
        # Append tuple with (UPC, H, S, V)
        data.append((int(res[0]), int(res[1]), int(res[2]), int(res[3])))

    arguments, values = getopt(sys.argv[1:], 'm', ['method'])
    for i in range(len(arguments)):
        if arguments[i][0] in ('-m', '--method'):
            if values[i] == 'AVERAGE':
                average_characterization(data)
            elif values[i] == 'MULTIPLE_REGRESSION':
                multiple_regression(data)
