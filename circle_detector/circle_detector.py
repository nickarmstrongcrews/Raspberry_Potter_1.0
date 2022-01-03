import cv2 as cv
import numpy as np

class CircleDetector:
  def __init__(self):
    pass

  def DetectCircles(self, distilled_image):
    circles = cv.HoughCircles(distilled_image,cv.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)
    return circles

  def CirclePoints(self, img, circle):
    x_c, y_c, radius = circle[0:3]
    th = np.arange(0, 2*np.pi, 0.1)
    x = x_c + radius * np.cos(th)
    y = y_c + radius * np.sin(th)
    height = img.shape[0]
    width = img.shape[1]
    x = np.clip(x, 0, height-1)
    y = np.clip(y, 0, width-1)
    return list(zip(np.uint16(np.around(x)), np.uint16(np.around(y))))

  def CircleScore(self, distilled_image, circle):
    if len(circle) == 4:
      return circle[3]
    score = 0.0
    circle_points = self.CirclePoints(distilled_image, circle)
    n = len(circle_points)
    for (x, y) in circle_points:
      score += distilled_image[x, y]
      #score += distilled_image[y, x] / n
    return score

  def SelectDominantCircle(self, distilled_image, circles):
    best_score = None
    best_circle = None
    for circle in circles[0,:]:
      score = self.CircleScore(distilled_image, circle)
      if not np.any(best_score) or score > best_score:
        best_score = score
        best_circle = circle
    return best_circle

  def DrawCircle(self, distilled_image, circle):
    #out_img = cv.cvtColor(distilled_image, cv.COLOR_GRAY2BGR)
    out_img = distilled_image.copy()
    i = np.uint16(np.around(circle))
    # draw the outer circle
    cv.circle(out_img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(out_img,(i[0],i[1]),2,(0,0,255),3)
    return out_img

  def DrawCircles(self, distilled_image, circles):
    #out_img = cv.cvtColor(distilled_image, cv.COLOR_GRAY2BGR)
    out_img = distilled_image.copy()
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv.circle(out_img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv.circle(out_img,(i[0],i[1]),2,(0,0,255),3)
        # draw the individual points in the circle
        for (x, y) in self.CirclePoints(out_img, i):
            cv.circle(out_img, (x,y), radius=0, color=(255, 0, 0), thickness=-1)

    return out_img
