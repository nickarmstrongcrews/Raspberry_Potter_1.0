import cv2 as cv
import sys
import numpy as np
from circle_detector import CircleDetector

#TEST_IMAGE_PATH = '../data/circle4.png'
TEST_IMAGE_PATH = '../data/perfect_circle.jpg'

img = cv.imread(TEST_IMAGE_PATH)
if img is None:
  sys.exit("Could not read the image.")

# pad image to make it square to avoid height/width bug somewhere
#height, width = img.shape[0:2]
#if width > height:
#  img = cv.copyMakeBorder(img, 0, width-height, 0, 0, cv.BORDER_CONSTANT, None, value=0)
#elif height > width:
#  img = cv.copyMakeBorder(img, 0, 0, 0, height-width, cv.BORDER_CONSTANT, None, value=0)



img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#img_gray = 255-cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)
assert np.all(img.shape[0:2] == img_gray.shape[0:2])

#GaussianBlur( src_gray, src_gray, Size(9, 9), 2, 2 );
ret, img_binary = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY );

assert img.shape[2] == 3
cv.imshow('image', img)
k = cv.waitKey(0)

assert len(img_gray.shape) == 2
cv.imshow('image_gray', img_gray)
k = cv.waitKey(0)

cv.imshow('image_binary', img_binary)
k = cv.waitKey(0)

detector = CircleDetector()
circles = detector.DetectCircles(img_gray, 0, 0)
assert np.any(circles)
img_circles = detector.DrawCircles(img_gray, img, circles)


cv.imshow('image_circles', img_circles)
k = cv.waitKey(0)


dominant_circle = detector.SelectDominantCircle(img_gray, circles)
img_circle = detector.DrawCircle(img_gray, img, dominant_circle)

cv.imshow('image_circle', img_circle)
k = cv.waitKey(0)

#if k == ord("q"):
#    cv.imwrite("starry_night.png", img)
cv.destroyAllWindows()
