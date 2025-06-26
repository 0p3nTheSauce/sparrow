import queue
import numpy as np

class Screen():
  def __init__(self, name='sky', width=2000
    , height=2000, bg_color=(255, 255, 255)
    , point_buff=None, poly_buff=None
    , flock=None, canvas=None, speed = 100
    , slowness = 1, flocking = False):
    self.name = name
    self.width = width
    self.height = height
    self.bg_color = bg_color
    if point_buff is None:
      self.point_buff = queue.Queue()
    else:
      self.point_buff = point_buff
    if poly_buff is None:
      self.poly_buff = queue.Queue()
    else:
      self.poly_buff = poly_buff
    if flock is None:
      self.flock = queue.Queue()
    else:
      self.flock = flock
    if canvas is None:
      self.canvas = np.ones((height, width, 3),
        dtype=np.uint8) * np.array(bg_color, dtype=np.uint8)
    else:
      self.canvas = canvas
    self.speed = speed
    self.slowness = slowness
    self.flocking = flocking
    