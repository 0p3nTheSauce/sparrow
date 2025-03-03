#sparrows is a play on turtle graphics
#sparrows is a python library that allows you to draw shapes and images on the screen
#sparrow will be faster than slow turtle, and will be able to 'flock together' in parrallel

import cv2 
import numpy as np

class Sparrow:
  def __init__(self, name, speed):
    self.name = name
    self.speed = speed
    self.x = 0
    self.y = 0
    self.color = (0,0,0)
    self.size = 1
    self.image = 'v^o>'
    self.angle = 0
    self.pen = False
    
  def forward(self, distance):
    '''move the sparrow forward by distance'''
    new_x, new_y = new_coordinate(self.x, self.y, self.angle, distance)
    self.x = new_x
    self.y = new_y
    
  def backward(self, distance):
    '''move the sparrow backward by distance'''
    new_x, new_y = new_coordinate(self.x, self.y, self.angle, -distance)
    self.x = new_x
    self.y = new_y
    
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
  x,y = coord
  new_x = x + distance * np.cos(angle)
  new_y = y + distance * np.sin(angle)
  return (new_x, new_y)    
    

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
  return (x+300, 300-y)

def screen_2_cartesian(coord):
  '''convert the screen coordinates to cartesian coordinates'''
  x,y = coord
  return (x-300, 300-y)

def deg_2_rad(deg):
  '''convert degrees to radians'''
  return deg * np.pi / 180

def main():
  blank_ = blank()
  #spot = small_circle(300,300, blank)
  # cv2.imshow('blank', blank_)
  tri = directed_trianlge((0,0), deg_2_rad(30), blank_)
  
  # cv2.imshow('spot', spot)  
  cv2.imshow('tri', tri)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()
    