#sparrows is a play on turtle graphics
#sparrows is a python library that allows you to draw shapes and images on the screen
#sparrow will be faster than slow turtle, and will be able to 'flock together' in parrallel

import cv2 
import numpy as np

class Screen:
  _instance = None 
  
  def __new__(cls, width=500, height=500, bg_color=(255, 255, 255)):
    if cls._instance is None:
      cls._instance = super(Screen, cls).__new__(cls)
      cls._instance.width = width
      cls._instance.height = height
      cls._instance.bg_color = bg_color
      cls._instance.canvas = np.ones((height, width, 3),
        dtype=np.uint8) * np.array(bg_color, dtype=np.uint8)
    return cls._instance
  
  def show(self):
    cv2.imshow("Sparrow Screen", self.canvas)
    cv2.waitKey(1)
    
  def clear(self):
    self.canvas[:] = self.bg_color
    
  # def update(self):
  #   cv2.imshow("Sparrow Screen", self.canvas)
  #   cv2.waitKey(1)
    


class Sparrow:
  def __init__(self):
    self.screen = Screen()
    self.speed = 0
    self.x, self.y = self.screen.width // 2, self.screen.height // 2
    self.color = (0,0,0)
    self.size = 1
    self.image = 'v^o>'
    self.angle = 0
    self.pen = True
    self.priority = 0 #0 is the highest, 1 is the next highest, etc.
    
  def clear(self):
    self.screen.clear()
    self.screen.show()
    
  def goto(self, x, y):
    x,y = cartesian_2_screen((x,y))
    if self.pen:
      cv2.line(self.screen.canvas, (self.x, self.y), (x, y),
        self.color, self.size)
    self.x, self.y = x, y
    self.screen.show()
    
  def forward(self, distance):
    '''move the sparrow forward by distance'''
    new_x, new_y = new_coordinate((self.x, self.y), self.angle, distance)
    if self.pen:
      cv2.line(self.screen.canvas, (self.x, self.y), (new_x, new_y),
        self.color, self.size)
    self.x = new_x
    self.y = new_y
    self.screen.show()
    
    
  def backward(self, distance):
    '''move the sparrow backward by distance'''
    new_x, new_y = new_coordinate((self.x, self.y), self.angle, -distance)
    if self.pen:
      cv2.line(self.screen.canvas, (self.x, self.y), (new_x, new_y),
        self.color, self.size)
      
    self.x = new_x
    self.y = new_y
    self.screen.show()
    
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

    
def new_coordinate(coord, angle, distance):
  '''return the new coordinate after moving distance in the angle direction'''
  x,y = screen_2_cartesian(coord)
  new_x = x + distance * np.cos(angle)
  new_y = y + distance * np.sin(angle)
  return cartesian_2_screen((new_x, new_y))    
    

#first i need to remind myself how to use opencv, starting with creating a blank white image, with black lines in the diagonal
def blank():
  '''create a blank white image with a black diagonal line'''
  blank = np.ones((600, 600,3)) * 255
  #cv2.line(blank, (0,0), (600,600), (0,0,0), 3)
  return blank

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
  return (int(x+300), int(300-y))

def screen_2_cartesian(coord):
  '''convert the screen coordinates to cartesian coordinates'''
  x,y = coord
  return (x-300, 300-y)

def deg_2_rad(deg):
  '''convert degrees to radians'''
  return deg * np.pi / 180


def test_directed_triangle():
  blank_ = blank()
  #spot = small_circle(300,300, blank)
  # cv2.imshow('blank', blank_)
  tri = directed_trianlge((0,0), deg_2_rad(30), blank_)
  
  # cv2.imshow('spot', spot)  
  cv2.imshow('tri', tri)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def main():
  wn = Screen()
  sparrow = Sparrow()
  sparrow.forward(100)
  sparrow.left(deg_2_rad(90))
  sparrow.forward(100)
  sparrow.set_color((255,0,0))
  sparrow.goto(0,0)
  
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()
    