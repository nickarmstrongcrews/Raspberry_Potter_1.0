import cv2 as cv
import os
import subprocess

SOUND_PATH = '../data/lumos.mp3'
IMAGE_PATH = '../data/lightburst.png'
FADE_SCRIPT = '../data/light.sh'
FADE_DURATION_MS = 2300
WINDOW_NAME = 'lightburst'

class SpellEffect:
  def __init__(self):
    self.img = cv.imread(IMAGE_PATH)
    if self.img is None:
      print("Could not read the image.")

  def PlaySound(self):
    subprocess.call('play %s &' % SOUND_PATH, shell=True)

  def ShowVisualEffect(self):
    cv.namedWindow(WINDOW_NAME, cv.WINDOW_NORMAL)
    cv.setWindowProperty(WINDOW_NAME, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN);
    cv.imshow(WINDOW_NAME, self.img);
    os.system('sh %s &' % FADE_SCRIPT)
    cv.waitKey(FADE_DURATION_MS)
    cv.destroyWindow(WINDOW_NAME)

  def Activate(self):
    self.PlaySound()
    if self.img is not None:
      self.ShowVisualEffect()
    else:
      print("No image to display.")
