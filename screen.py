import numpy as np
import queue
import cv2

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
      cls._instance.buffer = queue.Queue()
      cls._instance.canvas = np.ones((height, width, 3),
        dtype=np.uint8) * np.array(bg_color, dtype=np.uint8)
    return cls._instance
  
  def show(self):
    cv2.imshow("Sparrow Screen", self.canvas)
    key = cv2.waitKey(1)
    if key == 27:
      cv2.destroyAllWindows()
      
    
  def clear(self):
    self.canvas[:] = self.bg_color
  
  def update(self):
    # while not self.buffer.empty():
    #   x, y, color = self.buffer.get()
    #   self.canvas[y, x] = color
    #   self.show()  # Refresh after each point
    self.chunks_update()
      
  def chunks_update(self, chunk_size=10):
    while not self.buffer.empty():
      chunk = []
      for _ in range(chunk_size):
        try:
          x, y = self.buffer.get_nowait()
          chunk.append((x, y))
        except queue.Empty:
          break
      x_coords = np.array([item[0] for item in chunk])
      y_coords = np.array([item[1] for item in chunk])
      self.canvas[y_coords, x_coords] = (0,0,0)
      # for x, y in chunk:
      #   self.canvas[y, x] = (0,0,0)
      self.show()
      
  def mainloop(self):
    # while True:
    #   if not self.buffer.empty():
    #     coord = self.buffer.get() #coord coming in screen coordinates
    #     if coord is None:
    #       break
    #     x,y = coord
    #     self.canvas[y,x] = self.colour#HACK doesn't use sparrows colour, and probably slow
    #     self.show()
    #   if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    self.chunks_update()