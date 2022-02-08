import cv2 as cv
import numpy as np

class FramePreprocessor:
  '''Do stuff to frames in preparation for shape matching. Threshold to binary and squash frame sequence into single frame.'''
  def __init__(self):
    self.accumulated_frame = None
    self.num_frames = 0

  def Threshold(self, frame):
    '''Input color frame, output binary frame. Uses hard-coded threshold.'''
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret,frame_binary = cv.threshold(frame_gray,253,255,cv.THRESH_BINARY)
    return frame_binary

  def Accumulate(self, frame):
    '''Adds a frame into the accumulation.'''
    if not np.any(self.accumulated_frame):
      self.accumulated_frame = frame
    else:
      self.accumulated_frame += frame
      np.clip(self.accumulated_frame, 0, 255)
    self.num_frames += 1.0
    #return np.uint8(np.clip(np.around(self.accumulated_frame / self.num_frames), 0, 255))  # average
    return np.uint8(np.clip(np.around(self.accumulated_frame), 0, 255))  # sum
