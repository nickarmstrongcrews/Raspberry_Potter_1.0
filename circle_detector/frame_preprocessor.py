import cv2 as cv
import numpy as np

class FramePreprocessor:
  def __init__(self):
    self.accumulated_frame = None
    self.num_frames = 0

  def Threshold(self, frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret,frame_binary = cv.threshold(frame_gray,250,255,cv.THRESH_BINARY)
    return frame_binary

  def Accumulate(self, frame):
    if not np.any(self.accumulated_frame):
      self.accumulated_frame = frame
    else:
      self.accumulated_frame += frame
      np.clip(self.accumulated_frame, 0, 255)
    self.num_frames += 1.0
    #return np.uint8(np.clip(np.around(self.accumulated_frame / self.num_frames), 0, 255))
    return np.uint8(np.clip(np.around(self.accumulated_frame), 0, 255))
