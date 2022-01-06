import numpy as np
from circle_detector import CircleDetector
from frame_preprocessor import FramePreprocessor


class LumosDetector:
  def __init__(self):
    self.circle_detector = CircleDetector()
    self.processor = FramePreprocessor()
    pass

  def AddFrameAndDetect(self, frame):
    frame_thresholded = self.processor.Threshold(frame)
    accumulated_frame = self.processor.Accumulate(frame_thresholded)
    circles = self.circle_detector.DetectCircles(accumulated_frame)
    if np.any(circles):
      dominant_circle = self.circle_detector.SelectDominantCircle(accumulated_frame, circles)
      radius = dominant_circle[2]
      num_inliers = len(self.circle_detector.CircleInliers(accumulated_frame, dominant_circle))
      if num_inliers > 10 / radius:
        return dominant_circle
    return None
