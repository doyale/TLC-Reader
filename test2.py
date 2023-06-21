import cv2
import interactive
import util
import matplotlib.pyplot as plt
import copy
import numpy as np

image = cv2.imread("LS-2310V3C PE-EE 9-1.jpg", 1)
image = util.resize_image(image, 500)
cv2.circle(image, (100, 100), 6, (0, 0, 255), 2)
cv2.circle(image, (10, 100), 6, (0, 0, 255), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)