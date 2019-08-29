import cv2
import imutils
import numpy as np
import math
from sklearn.cluster import KMeans
from collections import Counter

img = cv2.imread('test_case2.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Red color rangle  169, 100, 100 , 189, 255, 255
lower_range = np.array([89, 50, 50])
upper_range = np.array([140, 255, 255])

mask = cv2.inRange(hsv, lower_range, upper_range)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

# find contours in the mask and initialize the current
# (x, y) center of the ball
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
center = None
# only proceed if at least one contour was found
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
centers = []
radi = []
counter = 0

# iterate all existing contours
for c in cnts:
    # Limit the contours to the 2 biggest ones
    if counter >= 2:
        break

    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    centers.append(center)
    radi.append(radius)

    leftUp = ((int(x) - int(radius / math.sqrt(2))), int(y) - int(radius / math.sqrt(2)))
    rightBottom = (int(x) + int(radius / math.sqrt(2)), int(y) + int(radius / math.sqrt(2)))
    # draw the circle and centroid on the frame,
    # then update the list of tracked points
    # cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 255), 2)
    cv2.rectangle(img, leftUp, rightBottom, (0, 255, 255), 2)
    cv2.circle(img, center, 5, (0, 0, 255), -1)
    counter += 1

# Draw the circle in the central point between the center of each guide
centers = sorted(centers, key=lambda tup: tup[0])
centroidX = int((abs(centers[0][0] - centers[1][0]) / 2) + centers[0][0])
centroidY = int((abs(centers[0][1] - centers[1][1]) / 2) + centers[0][1])
centroidRadius = int((radi[0] + radi[1]) / 4)
# cv2.circle(img, (centroidX, centroidY), centroidRadius, (255, 0, 255), 2)

# calculate the crop coordinates to the color analysis area
cropXLeft = centroidX - centroidRadius
cropXRight = centroidX + centroidRadius
cropYUp = centroidY - centroidRadius
cropYDown = centroidY + centroidRadius

cv2.rectangle(img, (cropXLeft, cropYUp), (cropXRight, cropYDown), (255, 0, 255), 2)

cropArea = img[cropYUp:cropYDown, cropXLeft:cropXRight]
cv2.imshow('cropArea', cropArea)

# Cluster and assign labels to the pixels in the crop area
cropArea = cropArea.reshape((cropArea.shape[0] * cropArea.shape[1], 3))
cluster = KMeans(n_clusters=4)
labels = cluster.fit_predict(cropArea)

# count labels to find most popular
label_counts = Counter(labels)

# subset out most popular centroid
dominant_color = cluster.cluster_centers_[label_counts.most_common(1)[0][0]]
apparentColor = map(int, list(dominant_color))

# register the RGB values for the sample
font = cv2.FONT_HERSHEY_COMPLEX
cv2.putText(img, 'Sample RGB: (%d, %d, %d)' % (apparentColor[2], apparentColor[1], apparentColor[0]), (40, 40), font,
            1, (0, 0, 0), 2, cv2.LINE_AA)

# update the points queue

cv2.imshow('image', img)
cv2.imshow('mask', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
