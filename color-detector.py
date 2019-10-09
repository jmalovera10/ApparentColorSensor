from collections import Counter

import sys
import cv2
import imutils
import colorsys
import numpy as np
from sklearn.cluster import KMeans


def main():
    img_file = sys.argv[1]
    img = cv2.imread(img_file)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Red color rangle  169, 100, 100 , 189, 255, 255
    lower_range = np.array([169, 100, 75])
    upper_range = np.array([189, 255, 255])

    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # only proceed if at least one contour was found
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    centers = []
    counter = 0
    rotation = 0
    height = 0
    width = 0
    # iterate all existing contours
    for c in cnts:
        # Limit the contours to the 2 biggest ones
        if counter >= 2:
            break
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 4:
            # Add the contour that matches the reference shape
            min_rectangle = cv2.minAreaRect(c)
            center = min_rectangle[0]
            width += min_rectangle[1][0]
            height += min_rectangle[1][1]
            rotation += min_rectangle[2]

            centers.append(center)
            center = tuple(map(int, center))

            cv2.circle(img, center, 5, (0, 0, 255), -1)
            box = cv2.boxPoints(min_rectangle)
            box = np.int0(box)
            cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

            counter += 1

    width /= counter * 1.8
    height /= counter * 1.2
    rotation /= counter
    # Draw the circle in the central point between the center of each guide
    centers = sorted(centers, key=lambda tup: tup[0])
    centroidX = int((abs(centers[0][0] - centers[1][0]) / 2) + centers[0][0])
    centers = sorted(centers, key=lambda tup: tup[1])
    centroidY = int((abs(centers[0][1] - centers[1][1]) / 2) + centers[0][1])

    center_box = cv2.boxPoints(((centroidX, centroidY), (width, height), rotation))
    center_box = np.int0(center_box)

    (img_h, img_w) = img.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((centroidX, centroidY), rotation, 1)
    cropArea = cv2.warpAffine(img, rotation_matrix, (img_w, img_h))
    cropArea = cv2.getRectSubPix(cropArea, (int(width), int(height)), (int(centroidX), int(centroidY)))

    # Draw the centroid contour in the original image
    cv2.drawContours(img, [center_box], 0, (0, 160, 255), 2)
    cv2.circle(img, (int(centroidX), int(centroidY)), 5, (255, 0, 255), -1)
    cv2.imshow('cropArea', cropArea)

    # Cluster and assign labels to the pixels in the crop area
    cropArea = cropArea.reshape((cropArea.shape[0] * cropArea.shape[1], 3))
    cluster = KMeans(n_clusters=10)
    labels = cluster.fit_predict(cropArea)

    # count labels to find most popular
    label_counts = Counter(labels)

    # subset out most popular centroid
    dominant_color = cluster.cluster_centers_[label_counts.most_common(1)[0][0]]
    apparentColor = map(int, list(dominant_color))
    apparentColor = colorsys.rgb_to_hsv(float(apparentColor[2]) / 255.0, float(apparentColor[1]) / 255.0,
                                        float(apparentColor[0]) / 255.0)
    print apparentColor
    # register the RGB values for the sample
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(img,
                'Sample HSV: (%d, %d, %d)' % (apparentColor[0] * 360, apparentColor[1] * 100, apparentColor[2] * 100),
                (40, 40),
                font,
                1, (0, 0, 0), 2, cv2.LINE_AA)

    # update the points queue

    cv2.imshow('image', img)
    cv2.imshow('mask', mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
