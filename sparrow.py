#sparrows is a play on turtle graphics
#sparrows is a python library that allows you to draw shapes and images on the screen
#sparrow will be faster than slow turtle, and will be able to 'flock together' in parrallel

import cv2 
import numpy as np
import queue
import threading
import time
import random
import lines #local import

#Global variables for Sparrow
HOME = (0,0)

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
    while not self.buffer.empty():
      x, y, color = self.buffer.get()
      self.canvas[y, x] = color
      self.show()  # Refresh after each point
      
  def mainloop(self):
    while True:
      if not self.buffer.empty():
        coord = self.buffer.get() #coord coming in screen coordinates
        if coord is None:
          break
        x,y = coord
        self.canvas[y,x] = self.colour#HACK doesn't use sparrows colour, and probably slow
        self.show()
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
    
def run_parallel(task, sparrow, *args):
  '''run tasks in parallel'''
  thread = threading.Thread(target=task, args=(sparrow, *args))
  thread.start()
  return thread

def update_screen(screen):
  """Continuously updates and displays the screen while threads are active."""
  while any(thread.is_alive() for thread in threading.enumerate() if thread != threading.main_thread()):
    screen.update()
    screen.show()
    time.sleep(0.01)  # More frequent updates

  # Final update and display
  screen.update()
  screen.show()
  cv2.waitKey(0)
  cv2.destroyAllWindows()

class Sparrow():
  def __init__(self):
    self.screen = Screen()
    self.slowness = 1
    self.x, self.y = 0,0
    self.color = (0,0,0)
    self.size = 1
    self.image = 'v^o>'
    self.angle = 0
    self.pen = True
    self.priority = 0 #0 is the highest, 1 is the next highest, etc.
    
  def clear(self):
    self.screen.clear()
    self.screen.show()
    
  def goto(self, x, y, penup=False, drawline=False):
    if not penup and self.pen:
      if drawline:
        self.drawline(x, y)
      else:
        self.__drawline_points(x, y)
    self.x, self.y = x, y
    # self.screen.show()
  
  def drawline(self, *args):
    curr_x, curr_y = cartesian_2_screen((self.x, self.y))
    if len(args) == 1:
      distance = args[0]
      # new_x, new_y = new_coordinate((self.x, self.y), self.angle, distance)
      new_x, new_y = cartesian_2_screen(self.__new_coordinate(distance))
    elif len(args) == 2:
      new_x, new_y = cartesian_2_screen(args)
      self.x, self.y = args
    else:
      raise ValueError('Invalid number of arguments')
    
    if self.slowness == 0:  
      self.screen.canvas = lines.bresenham_line((curr_x, curr_y), (new_x, new_y),
        self.screen.canvas, self.color)
      self.screen.show()
    else:
      self.screen.canvas = lines.bresenham_slowness((curr_x, curr_y), (new_x, new_y),
        self.screen.canvas, self.color, self.slowness)
    # self.x = new_x
    # self.y = new_y
    
    
  def __drawline_points(self, *args):
    '''used for parallel writing'''
    curr_x, curr_y = cartesian_2_screen((self.x, self.y))
    if len(args) == 1:
      distance = args[0]
      new_x, new_y = cartesian_2_screen(self.__new_coordinate(distance))
    elif len(args) == 2:
      new_x, new_y = cartesian_2_screen(args)
      self.x, self.y = args
    else:
      raise ValueError('Invalid number of arguments')
    
    point_generator = lines.bresenham_points((curr_x, curr_y), (new_x, new_y))
    for point in point_generator:
        self.screen.buffer.put((point[0], point[1]))
        time.sleep(0.001)  # Critical: Allows threads to interleave
    
  
  def __new_coordinate(self, distance):
    '''return the new coordinate after moving distance in the angle direction'''
    new_x = self.x + distance * np.cos(self.angle)
    new_y = self.y + distance * np.sin(self.angle)
    self.x = new_x
    self.y = new_y
    return (new_x, new_y)
    
  def forward(self, distance):
    '''move the sparrow forward by distance'''
    self.__drawline_points(distance)
  
  def backward(self, distance):
    '''move the sparrow backward by distance'''
    self.__drawline_points(-distance)
  
  def left(self, angle):
    '''turn the sparrow left by angle'''
    self.angle += angle
  
  def right(self, angle):
    '''turn the sparrow right by angle'''
    self.angle -= angle
  
  def penup(self):
    '''stop drawing'''
    self.pen = False
    
  def pendown(self):
    '''start drawing'''
    self.pen = True
  
  def set_color(self, color):
    '''set the color of the sparrow'''
    self.color = color
  
  def set_size(self, size):
    '''set the size of the sparrow'''
    self.size = size
    
  def set_image(self, image):
    '''set the image of the sparrow'''
    self.image = image
    
  def set_angle(self, angle):
    '''set the angle of the sparrow'''
    self.angle = angle
  
  def set_position(self, x, y):
    '''set the position of the sparrow'''
    self.x = x
    self.y = y
    
  def set_slowness(self, slowness):
    '''set the slowness of the sparrow'''
    self.slowness = slowness 

def small_circle(coord,screen,colour=(0,0,0)):
  '''draw a small circle at x,y on the screen'''
  x,y=coord
  x,y = cartesian_2_screen(x,y)
  cv2.circle(screen, (x,y), 10, colour, -1)
  return screen
  
def small_triangle(coord,screen,colour=(0,0,0)):
  '''draw a small triangle at x,y on the screen'''
  x,y=coord
  x,y = cartesian_2_screen(x,y)
  points = np.array([[x,y-5], [x-5,y+5], [x+5,y+5]])
  cv2.fillPoly(screen, [points], colour)
  return screen

def tup_2_np(tup):
  '''convert a tuple to a numpy array'''
  return np.array(tup)

def directed_trianlge(coord,angle,screen,colour=(0,0,0),size=10):
  '''draw a small triangle at x,y on the screen'''
  def new_coordinate(coord, angle, distance):
    '''return the new coordinate after moving distance in the angle direction'''
    x,y = screen_2_cartesian(coord)
    new_x = x + distance * np.cos(angle)
    new_y = y + distance * np.sin(angle)
    return cartesian_2_screen((new_x, new_y))   
  x,y = coord
  '''
  a\\
  | \\
  |  c
  | //
  b//
  '''
  #a,b,c=[x,y-size], [x,y+size], [x+size,y]
  
  #rotate the triangle
  a_angle = angle + np.pi/2#90 degrees
  b_angle = angle - np.pi/2#90 degrees
  a = new_coordinate((x,y), a_angle, size)
  b = new_coordinate((x,y), b_angle, size)
  c = new_coordinate((x,y), angle, size)
  
  #convert cartesian to screen
  a = cartesian_2_screen(a)
  b = cartesian_2_screen(b)
  c = cartesian_2_screen(c)
  
  points = np.array([a,b,c],dtype=np.int32)
  
  cv2.fillPoly(screen, [points], colour)
  return screen

def cartesian_2_screen(coord):
  '''convert the cartesian coordinates to screen coordinates'''
  x,y = coord
  return (round(x+300), round(300-y))

def screen_2_cartesian(coord):
  '''convert the screen coordinates to cartesian coordinates'''
  x,y = coord
  return (x-300, 300-y)

def deg_2_rad(deg):
  '''convert degrees to radians'''
  return deg * np.pi / 180


def test_directed_triangle():
  blank = np.ones((600,600), np.int8)*255
  #spot = small_circle(300,300, blank)
  # cv2.imshow('blank', blank_)
  tri = directed_trianlge((0,0), deg_2_rad(30), blank)
  
  # cv2.imshow('spot', spot)  
  cv2.imshow('tri', tri)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def test_basic():
  wn = Screen()
  sparrow = Sparrow()
  sparrow.set_slowness(1)
  sparrow.forward(100)
  sparrow.left(deg_2_rad(90))
  sparrow.forward(100)
  sparrow.set_color((255,0,0))
  sparrow.goto(0,0)
  # sparrow.screen.show()
  wn.show()
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
def test_parallel():
  wn = Screen()
  rock = Sparrow()
  petronia = Sparrow()
  house = Sparrow()
  eurasian_tree = Sparrow()
  

  
  thread1 = run_parallel(rand_triangle, rock, 50)
  thread2 = run_parallel(rand_triangle, petronia, 30)
  thread3 = run_parallel(rand_triangle, house, 20)
  thread4 = run_parallel(rand_triangle, eurasian_tree, 10)
  
  wn.mainloop()
  
  thread1.join()
  thread2.join()
  thread3.join()
  thread4.join()

def better_triangle(sparrow, distance, pos=(0,0)):
  sparrow.goto(*pos, penup=True)
  sparrow.drawline(distance)
  sparrow.right(deg_2_rad(120))
  sparrow.drawline(distance)
  sparrow.goto(*pos,drawline=True) 

def triangle(sparrow, distance, pos):
  # sparrow.penup()
  # sparrow.goto(*pos)
  # sparrow.pendown()
  for _ in range(3):
    sparrow.drawline(distance)
    sparrow.right(deg_2_rad(120))

def test_big_triangle():
  wn = Screen()
  rock = Sparrow()
  # rock.goto(100,100, penup=True)
  # for i in range(3):
  #   rock.drawline(100)
  #   rock.right(deg_2_rad(120))
  # # for i in range(3):
  # #   rock.forward(100)
  # #   rock.right(deg_2_rad(120))
  # rock.goto(*HOME, penup=True)
  # for i in range(3):
  #   rock.forward(100)
  #   rock.right(deg_2_rad(120))
  # better_triangle(rock, 100)
  
  triangle(rock, 100, (100,100))
  
  wn.mainloop()
  
def rand_triangle(sparrow,distance):
  for _ in range(5):
    sparrow.penup()
    rand_x = random.randint(-200,200)
    rand_y = random.randint(-200,200)
    sparrow.goto(rand_x,rand_y)
    sparrow.pendown()
    for _ in range(3):
      sparrow.drawline(distance)
      sparrow.right(deg_2_rad(120))

def test_more_triangles():
  wn = Screen()
  rock = Sparrow()
  # rock.set_slowness(0)
  rand_triangle(rock, 100)
  wn.mainloop()
  
def main():
  #test_parallel()
  #test_big_triangle()
  test_more_triangles()
  

if __name__ == '__main__':
  main()
    