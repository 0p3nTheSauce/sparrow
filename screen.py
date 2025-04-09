import numpy as np
import queue
import cv2

#local
import polygon
class Screen:
  _instance = None 
  
  def __new__(cls, width=799, height=799, bg_color=(255, 255, 255), colour=(0,0,0)):
    if cls._instance is None:
      cls._instance = super(Screen, cls).__new__(cls)
      cls._instance.width = width
      cls._instance.height = height
      cls._instance.bg_color = bg_color
      cls._instance.colour = colour
      cls._instance.slowness=0
      # cls._instance.buffer = queue.Queue()
      cls._instance.point_buff = queue.Queue()
      cls._instance.poly_buff = queue.Queue()
      cls._instance.flock=False
      cls._instance.canvas = np.ones((height, width, 3),
        dtype=np.uint8) * np.array(bg_color, dtype=np.uint8)
    return cls._instance
  
  def show(self,wait=1):
    cv2.imshow("Sparrow Screen", self.canvas)
    key = cv2.waitKey(wait)
    if key == 27:
      cv2.destroyAllWindows()
      
  def flock_on(self):
    self.flock = True
  
  def flock_off(self):
    self.flock = False
  
  def clear(self):
    self.canvas[:] = self.bg_color
  
  def on_screen(self,new_coords):
    '''return True if the coordinates are on the screen'''
    x,y = new_coords    
    return 0 <= x < self.width and 0 <= y < self.height
  
  def seq_update(self):
    while True:
      if not self.buffer.empty():
        coord = self.buffer.get() #coord coming in screen coordinates
        if coord is None:
          break
        x,y,colour = coord
        if self.on_screen((x,y)):
          self.canvas[y,x] = colour
        self.show()
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
  def chunks_update(self, chunk_size=100):
    while True:
      chunk = []
      for _ in range(chunk_size):
        try:
          data = self.point_buff.get_nowait()
          x, y, colour = data          
          if self.on_screen((x,y)):
            chunk.append((x, y, colour))
        except queue.Empty:
          break
      try:
        poly = self.poly_buff.get_nowait()
        self.canvas = polygon.fill_poly(self.canvas, poly.edges,
                                        poly.colour)
      except queue.Empty:
        pass 
      if not chunk:
        break
      x_coords = np.array([item[0] for item in chunk])
      y_coords = np.array([item[1] for item in chunk])
      colours = np.array([item[2] for item in chunk])
      self.canvas[y_coords, x_coords] = colours
      # self.canvas[y_coords, x_coords] = (0,0,0)
      self.show()
      
  def mainloop(self):
    if self.flock:
      # self.seq_update()
      self.show(0)
    else: 
      self.chunks_update()
      self.show(0)
    