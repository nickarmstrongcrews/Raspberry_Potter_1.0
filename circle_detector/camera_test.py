import cv2

# this is /dev/videoX; you can query these with `for x in $(seq 0 10) ; do echo $x: ; v4l2-ctl -d /dev/video$x --list-formats ; done` and pick the one with the most formats listed

WEBCAM_INDEX = 0 # Nick's laptop

# define a video capture object
vid = cv2.VideoCapture(WEBCAM_INDEX)

print("FPS:", vid.get(cv2.CAP_PROP_FPS))
print("%d x %d" %(vid.get(cv2.CAP_PROP_FRAME_HEIGHT), vid.get(cv2.CAP_PROP_FRAME_WIDTH)))
vid.set(cv2.CAP_PROP_FPS, 10)

while(True):
    # camera option flags defined at https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html#ggaeb8dd9c89c10a5c63c139bf7c4f5704da7c2fa550ba270713fca1405397b90ae0
    # maybe these take a while to take effect?
    print("FPS:", vid.get(cv2.CAP_PROP_FPS))
    print("%d x %d" %(vid.get(cv2.CAP_PROP_FRAME_HEIGHT), vid.get(cv2.CAP_PROP_FRAME_WIDTH)))


    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    # Display the resulting frame
    cv2.imshow('frame', frame)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
