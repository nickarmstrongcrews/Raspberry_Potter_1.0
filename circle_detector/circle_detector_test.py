import cv2 as cv
import sys
from circle_detector import CircleDetector

TEST_IMAGE_PATH = '../data/circle4.png'
#TEST_IMAGE_PATH = '../data/perfect_circle.jpg'

img = cv.imread(TEST_IMAGE_PATH)
if img is None:
    sys.exit("Could not read the image.")


img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#img_gray = 255-cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)
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
circles = detector.DetectCircles(img_gray)
assert len(circles) > 0
img_circles = detector.DrawCircles(img, circles)


cv.imshow('image_circles', img_circles)
k = cv.waitKey(0)


dominant_circle = detector.SelectDominantCircle(img_gray, circles)
img_circle = detector.DrawCircle(img, dominant_circle)

cv.imshow('image_circle', img_circle)
k = cv.waitKey(0)

#if k == ord("q"):
#    cv.imwrite("starry_night.png", img)
cv.destroyAllWindows()
