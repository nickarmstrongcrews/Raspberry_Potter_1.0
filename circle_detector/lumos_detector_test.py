import cv2 as cv
import numpy as np
import os
from os.path import isfile, join
import sys
from lumos_detector import LumosDetector

TEST_FRAME_PATH = '../data/visible_wand_office/circle1/'
#TEST_IMAGE_PATH = '../data/perfect_circle.jpg'

files = [f for f in os.listdir(TEST_FRAME_PATH) if isfile(join(TEST_FRAME_PATH, f))]
files.sort()

if len(files) == 0:
  sys.exit("Could not read the image path.")

frames = []
for i in range(len(files)):
    filename=join(TEST_FRAME_PATH, files[i])
    #reading each files
    img = cv.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    print("%s: %d x %d x %d" %(filename, height, width, layers))
    #inserting the frames into an image array
    frames.append(img)

if len(frames) == 0:
  sys.exit("No frames in the image path")

detector = LumosDetector()

i = 0
for frame in frames:
  i += 1
  print("Showing frame %d of %d; type 'q' to quit." %(i, len(frames)))

  dominant_circle = detector.AddFrameAndDetect(frame)

  circles = detector.circle_detector.DetectCircles(detector.processor.accumulated_frame)
  img_circles = frame
  if np.any(circles):
    img_circles = detector.circle_detector.DrawCircles(detector.processor.accumulated_frame, frame, circles)

  img_circle = frame
  if np.any(dominant_circle):
    img_circle = detector.circle_detector.DrawCircle(detector.processor.accumulated_frame, frame, dominant_circle)

  #cv.imshow('frame', cv.hconcat([frame, cv.cvtColor(detector.processor.accumulated_frame, cv.COLOR_GRAY2BGR), cv.cvtColor(img_circle, cv.COLOR_GRAY2BGR)]))
  cv.imshow('frame', cv.vconcat([frame, cv.cvtColor(detector.processor.accumulated_frame, cv.COLOR_GRAY2BGR), img_circle]))
  #cv.imshow('frame', cv.vconcat([frame, cv.cvtColor(detector.processor.accumulated_frame, cv.COLOR_GRAY2BGR), img_circles]))
  k = cv.waitKey(0)
  if k == ord("q"):
    break


#assert len(circles) > 0
cv.destroyAllWindows()
