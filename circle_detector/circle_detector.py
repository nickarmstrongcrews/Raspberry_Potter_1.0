import cv2 as cv
import numpy as np

class CircleDetector:
  def __init__(self):
    pass

  def DetectCircles(self, distilled_image, min_radius=20, max_radius=150):
    '''Hough circle detection. See openCV docs.'''
    circles = cv.HoughCircles(distilled_image,cv.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=min_radius,maxRadius=max_radius)
    return circles

  def CirclePoints(self, height, width, circle):
    '''Return a list of all the pixel coords comprising the circle (ignoring pixel contents; the circle is complete)'''
    x_c, y_c, radius = circle[0:3]
    th = np.arange(0, 2*np.pi, 0.1)
    x = x_c + radius * np.cos(th)
    y = y_c + radius * np.sin(th)
    x = np.clip(x, 0, width-1)
    y = np.clip(y, 0, height-1)
    return list(zip(np.uint16(np.around(x)), np.uint16(np.around(y))))

  def CircleInliers(self, distilled_image, circle):
    '''Return a list of pixel coords that have high enough values are close enough to the circle.'''
    assert len(distilled_image.shape) == 2
    DIST_THRESHOLD = 10 # in pixels
    GRAY_PIXEL_THRESHOLD = 150
    x_c, y_c, radius = np.array(circle[0:3], dtype=np.float)
    height, width = distilled_image.shape[0:2]
    inliers = []
    # iterate over all pixels in the image patch containing the circle
    for x in np.uint16(np.arange(np.floor(x_c-radius-DIST_THRESHOLD), np.ceil(x_c+radius+DIST_THRESHOLD))):
      if x < 0 or x >= width:
        continue
      for y in np.uint16(np.arange(np.floor(y_c-radius-DIST_THRESHOLD), np.ceil(y_c+radius+DIST_THRESHOLD))):
        if y < 0 or y >= height:
          continue
        # do we need to do edge detection first?
        if distilled_image[y, x] < GRAY_PIXEL_THRESHOLD:
          continue
        sq_dist = np.abs((float(x)-x_c)**2 + (float(y)-y_c)**2 - radius**2)
        if sq_dist < DIST_THRESHOLD**2:
          inliers += [(x, y)]
    return inliers

  def _angular_distance(self, th1, th2, wrap_interval=2*np.pi):
    '''Return the angular distance between th1 and th2 (which must be within 2*pi of each other); output is in [0, pi].'''
    a, b = min(th1, th2), max(th1, th2)
    return np.min((abs(b-a), abs(b-a-wrap_interval)))

  def InliersArcLength(self, circle, inliers):
    '''Considering the inliers in polar coords, returns the arc length in radians.'''
    x_c, y_c, radius = circle[0:3]
    arc_length = 0.0
    last_th = None
    # note: assumes inliers are in order
    for (x, y) in inliers:
      th = np.arctan2(y-y_c, x-x_c)
      dth = self._angular_distance(last_th-th) if last_th else 0
      last_th = th
      # integrate up to avoid wraparound issues
      arc_length += dth
    return arc_length

  def CircleScore(self, distilled_image, circle):
    if len(circle) == 4:
      return circle[3]
    score = 0.0
    circle_points = self.CirclePoints(distilled_image.shape[0], distilled_image.shape[1], circle)
    n = len(circle_points)
    # sum the pixel values lying on the circle
    # TODO: replace with inlier count or similar
    for (x, y) in circle_points:
      #score += distilled_image[x, y]
      score += distilled_image[y, x]
      #score += distilled_image[y, x] / n
    return score

  def SelectDominantCircle(self, distilled_image, circles):
    '''Returns the circle with the best score.'''
    best_score = None
    best_circle = None
    for circle in circles[0,:]:
      score = self.CircleScore(distilled_image, circle)
      if not np.any(best_score) or score > best_score:
        best_score = score
        best_circle = circle
    return best_circle

  def DrawCircle(self, gray_image, distilled_image, circle):
    #out_img = cv.cvtColor(distilled_image, cv.COLOR_GRAY2BGR)
    out_img = distilled_image.copy()
    i = np.uint16(np.around(circle))
    # draw the outer circle
    cv.circle(out_img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(out_img,(i[0],i[1]),2,(0,0,255),3)
    # draw the inliers
    for (x, y) in self.CircleInliers(gray_image, i):
    #for (x, y) in self.CirclePoints(out_img.shape[0], out_img.shape[1], i): # draw the individual points in the circle
      cv.circle(out_img, (x,y), radius=2, color=(255, 0, 0), thickness=-1)
    return out_img

  def DrawCircles(self, gray_image, distilled_image, circles):
    #out_img = cv.cvtColor(distilled_image, cv.COLOR_GRAY2BGR)
    out_img = distilled_image.copy()
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
      # draw the outer circle
      cv.circle(out_img,(i[0],i[1]),i[2],(0,255,0),2)
      # draw the center of the circle
      cv.circle(out_img,(i[0],i[1]),2,(0,0,255),3)
      # draw the inliers
      #for (x, y) in self.CircleInliers(gray_image, i):
      #for (x, y) in self.CirclePoints(out_img.shape[0], out_img.shape[1], i): # draw the individual points in the circle
      #  cv.circle(out_img, (x,y), radius=2, color=(255, 0, 0), thickness=-1)
    return out_img
