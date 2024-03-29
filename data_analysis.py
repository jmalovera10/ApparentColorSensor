# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os
import mysql.connector
import sys
from getopt import getopt
import colorsys
from scripts.regression_methods import RegressionMethods
from scripts import plotter


if __name__ == '__main__':
    # Load environment variables
    load_dotenv('.env')

    # Load script arguments
    arguments, values = getopt(sys.argv[1:], 'm:c:pg', ['method', 'colorspace', 'precluster', 'graph'])
    method = None
    colorspace = None
    precluster = False
    graph = False
    for command, value in arguments:
        if command in ('-m', '--method'):
            method = value
        elif command in ('-c', '--colorspace'):
            colorspace = value
        elif command in ('-p', '--precluster'):
            precluster = True
        elif command in ('-g', '--graph'):
            graph = True

    # Connect to the database
    measurements_db = mysql.connector.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE")
    )
    db_cursor = measurements_db.cursor(buffered=True)
    # Retrieve calibration data
    query = 'SELECT UPC, H, S, V FROM CALIBRATION'
    db_cursor.execute(query)
    # Gets all results for each UPC including AVG, VAR and STD DEV
    results = db_cursor.fetchall()
    data = []
    H = None
    S = None
    V = None

    for res in results:
        # Append tuple with (UPC, H, S, V)
        H = int(res[1])
        S = int(res[2])
        V = int(res[3])
        if colorspace == 'RGB':
            transform = colorsys.hsv_to_rgb(float(H) / 360.0, float(S) / 100.0, float(V) / 100.0)
            H = int(transform[0] * 255)
            S = int(transform[1] * 255)
            V = int(transform[2] * 255)
        elif colorspace == 'HSL':
            RGB = colorsys.hsv_to_rgb(float(H) / 360.0, float(S) / 100.0, float(V) / 100.0)
            transform = colorsys.rgb_to_hls(RGB[0], RGB[1], RGB[2])
            H = int(transform[0] * 360)
            S = int(transform[2] * 100)
            V = int(transform[1] * 100)
        data.append((int(res[0]), H, S, V))

    # If pre-cluster flag is activated, the centroids of UPC values are calculated
    reg_methods = RegressionMethods()

    if precluster:
        data = reg_methods.pre_clustering(data)

    # Build the object that contains all the regression methods

    if method == 'MULTIPLE_REGRESSION':
        model = reg_methods.multiple_lineal_regression(data)
        print model
        if graph:
            plotter.normal_data_plotting(data, None)
    elif method == 'POLYNOMIAL_INTERPOL':
        model = reg_methods.polynomial_interpolation(data)
        print model
        if graph:
            plotter.normal_data_plotting(data)
    elif method == 'EUCLIDEAN_DISTANCE':
        result = reg_methods.euclidean_distance(data, [80, 24, 52])
        print 'VALOR_MUESTRA: ', result
        if graph:
            plotter.cylindrical_data_plotting(data)
