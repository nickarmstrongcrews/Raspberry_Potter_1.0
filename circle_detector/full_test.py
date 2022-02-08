import cv2 as cv
import numpy as np
from playsound import playsound
from lumos_detector import LumosDetector

WEBCAM_INDEX = 0 # Nick's laptop; see camera_test.py if not working.

# define a video capture object
vid = cv.VideoCapture(WEBCAM_INDEX, cv.CAP_V4L2)

def decode_fourcc(v):
  v = int(v)
  return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

fourcc = decode_fourcc(vid.get(cv.CAP_PROP_FOURCC))
format = vid.get(cv.CAP_PROP_FORMAT)
mode = vid.get(cv.CAP_PROP_MODE)
print("codec: %s, rgb=%d, format=%s, mode=%s" %(fourcc, bool(vid.get(cv.CAP_PROP_CONVERT_RGB)), format, mode))

print("FPS:", vid.get(cv.CAP_PROP_FPS))
print("%d x %d" %(vid.get(cv.CAP_PROP_FRAME_HEIGHT), vid.get(cv.CAP_PROP_FRAME_WIDTH)))
vid.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
vid.set(cv.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv.CAP_PROP_FPS, 30)

detector = LumosDetector()

while(True):
    # camera option flags defined at https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html#ggaeb8dd9c89c10a5c63c139bf7c4f5704da7c2fa550ba270713fca1405397b90ae0
    # maybe these take a while to take effect?
    print("FPS:", vid.get(cv.CAP_PROP_FPS))
    print("%d x %d" %(vid.get(cv.CAP_PROP_FRAME_HEIGHT), vid.get(cv.CAP_PROP_FRAME_WIDTH)))

    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    #ret, frame = vid.retrieve()

    if not bool(vid.get(cv.CAP_PROP_CONVERT_RGB)):
      if fourcc == "MJPG":
        frame = cv.imdecode(frame, cv.IMREAD_GRAYSCALE)
      elif fourcc == "YUYV":
        frame = cv.cvtColor(frame, cv.COLOR_YUV2GRAY_YUYV)
      else:
        print("unsupported format")
        break

    dominant_circle = detector.AddFrameAndDetect(frame)

    circles = detector.circle_detector.DetectCircles(detector.processor.accumulated_frame)
    #img_circles = frame
    #if np.any(circles):
      #img_circles = detector.circle_detector.DrawCircles(detector.processor.accumulated_frame, detector.processor.accumulated_frame, circles)

    accumulated_frame_color = cv.cvtColor(detector.processor.accumulated_frame, cv.COLOR_GRAY2BGR)

    success = False
    img_circle = frame
    if np.any(dominant_circle):
      success = True
      img_circle = detector.circle_detector.DrawCircle(detector.processor.accumulated_frame, frame, dominant_circle)
      accumulated_frame_color = detector.circle_detector.DrawCircle(detector.processor.accumulated_frame, accumulated_frame_color, dominant_circle)
      #if cv.waitKey(0) & 0xFF == ord('q'):
      #  break

    # Display the resulting frame
    cv.imshow('frame', cv.vconcat([img_circle, accumulated_frame_color]))
    if success:
      playsound('../data/lumos.mp3')
      if cv.waitKey(0) & 0xFF == ord('q'):
        break

    #cv.imshow('frame', frame)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()
