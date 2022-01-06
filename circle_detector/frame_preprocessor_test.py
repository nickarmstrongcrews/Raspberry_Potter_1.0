import cv2 as cv
import os
from os.path import isfile, join
import sys
from frame_preprocessor import FramePreprocessor

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

processor = FramePreprocessor()

i = 0
for frame in frames:
  i += 1
  print("Showing frame %d of %d; type 'q' to quit." %(i, len(frames)))

  frame_thresholded = processor.Threshold(frame)
  frame_accumulated = processor.Accumulate(frame_thresholded)
  assert len(frame_thresholded.shape) == 2
  assert len(frame_accumulated.shape) == 2

  print(frame.dtype)
  print(frame_thresholded.dtype)
  print(frame_accumulated.dtype)
  #assert (frame_thresholded.shape == frame.shape[0:2]).all()
  #assert (frame_thresholded.shape == frame_accumulated.shape).all()

  cv.imshow('frame', cv.hconcat([frame, cv.cvtColor(frame_thresholded, cv.COLOR_GRAY2BGR), cv.cvtColor(frame_accumulated, cv.COLOR_GRAY2BGR)]))
  #cv.imshow('frame', cv.hconcat([frame, cv.cvtColor(frame_thresholded, cv.COLOR_GRAY2BGR)]))
  k = cv.waitKey(0)
  if k == ord("q"):
    break


#assert len(circles) > 0
cv.destroyAllWindows()
