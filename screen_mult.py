from multiprocessing import Process, Queue
import numpy as np
import cv2
import queue

#local
import polygon

class Screen:
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
      self.point_buff = Queue()
    else:
      self.point_buff = point_buff
    if poly_buff is None:
      self.poly_buff = Queue()
    else:
      self.poly_buff = poly_buff
    if flock is None:
      self.flock = []
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
    
  def show(self, wait):
    cv2.imshow("Sparrow Screen", self.canvas)  
    key = cv2.waitKey(wait)
    if key == 27:
      cv2.destroyAllWindows()
      
  def start_flock(self):
    self.flocking = True
  
  def solo(self):
    self.flocking = False
  
  def clear(self):
    self.canvas[:] = self.bg_color
  
  def on_screen(self,new_coords):
    '''return True if the coordinates are on the screen'''
    x,y = new_coords    
    return 0 <= x < self.width and 0 <= y < self.height
  
     
  def polygon_update(self):
    try:
      poly = self.poly_buff.get_nowait()
      self.canvas = polygon.fill_poly(self.canvas, poly.edges,
                                      poly.colour, self.speed, self.slowness)
    except queue.Empty:
      return True
    return False
  
  def point_update(self):
    chunk = []
    finished = False
    for _ in range(self.speed):
      try:
        point = self.point_buff.get_nowait()
        x, y, colour = point
        if self.on_screen((x,y)):
          chunk.append((x,y,colour))
      except queue.Empty:
        finished = True
        break
    if len(chunk) != 0:
      x_coords = np.array([item[0] for item in chunk])
      y_coords = np.array([item[1] for item in chunk])
      colours = np.array([item[2] for item in chunk])
      self.canvas[y_coords, x_coords] = colours
    return finished
  
  
  def all_finished(self):
    return all(not sparr.is_alive() for sparr in self.flock)    
  
  def mainloop(self): 
    if self.flocking:
      while True:
        if self.point_update() and self.polygon_update() and self.all_finished():
          break
        else:
          self.show(self.slowness)
      self.show(0)
    else: 
      self.show(0)