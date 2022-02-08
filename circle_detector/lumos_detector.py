import numpy as np
from circle_detector import CircleDetector
from frame_preprocessor import FramePreprocessor


class LumosDetector:
  '''Top-level detector. Thresholds frames, accumulates frames, detects dominant circle, checks if it is good enough.'''
  def __init__(self):
    self.circle_detector = CircleDetector()
    self.processor = FramePreprocessor()

  def AddFrameAndDetect(self, frame):
    '''Returns the circle if detected, else None.'''
    frame_thresholded = self.processor.Threshold(frame)
    accumulated_frame = self.processor.Accumulate(frame_thresholded)
    circles = self.circle_detector.DetectCircles(accumulated_frame)
    if np.any(circles):
      dominant_circle = self.circle_detector.SelectDominantCircle(accumulated_frame, circles)
      radius = dominant_circle[2]
      inliers = self.circle_detector.CircleInliers(accumulated_frame, dominant_circle)
      num_inliers = len(inliers)
      # TODO: use ArcLength instead
      #if num_inliers > 10 / radius:  # circumference of full circle is ~6.28*radius
      if self.circle_detector.InliersArcLength(dominant_circle, inliers) > 0.75*2*np.pi:
        return dominant_circle
    return None
