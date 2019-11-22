import math
import os
from collections import Counter

from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from joblib import dump


class RegressionMethods:
    def __init__(self):
        pass

    @staticmethod
    def pre_clustering(data):
        upc = [1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55,
               60]  # , 65, 70, 75, 80, 90, 100, 110, 150, 200,
        # 250, 300, 350, 400, 450, 500]
        result = []
        for u in upc:
            parsed_data = [[UPC, H, S, V] for UPC, H, S, V in data if UPC == u]
            cluster = KMeans(n_clusters=1)
            labels = cluster.fit_predict(parsed_data)
            label_counts = Counter(labels)
            # subset out most popular centroid
            dominant_color = cluster.cluster_centers_[label_counts.most_common(1)[0][0]]
            result.append(map(int, dominant_color))
        return result

    @staticmethod
    def multiple_lineal_regression(data):
        x = [[H, S, V] for UPC, H, S, V in data]
        y = [[UPC] for UPC, H, S, V in data]
        model = LinearRegression()
        model.fit(x, y)
        dump(model, '%s\models\multiple_lineal_regression.joblib'% os.getcwd())
        return model.coef_[0], model.intercept_[0]

    @staticmethod
    def polynomial_interpolation(data):
        for count, degree in enumerate([1, 2, 3, 4, 5]):
            model = make_pipeline(PolynomialFeatures(degree), Ridge())
            X = [[H, S, V] for UPC, H, S, V in data]
            y = [UPC for UPC, H, S, V in data]
            model.fit(X, y)
            dump(model, '%s\models\polynomial_regression_%d.joblib' % (os.getcwd(), degree))
            print model.predict([[62, 18, 48]])

    @staticmethod
    def euclidean_distance(centroids, data):
        least_distance = 1000000.0
        upc = 0
        for cent in centroids:
            distance = math.sqrt(
                math.pow(cent[1] - data[0], 2) + math.pow(cent[2] - data[1], 2) + math.pow(cent[3] - data[2], 2))
            if distance < least_distance:
                least_distance = distance
                upc = cent[0]
        return upc

    @staticmethod
    def knn_clustering(data):
        cluster = KMeans(n_clusters=32)
        labels = cluster.fit_predict(data)
        label_counts = Counter(labels)
        # subset out most popular centroid
        print label_counts
        dominant_color = cluster.cluster_centers_[label_counts.most_common(1)[0][0]]
