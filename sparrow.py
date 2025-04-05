#sparrows is a play on turtle graphics
#sparrows is a python library that allows you to draw shapes and images on the screen
#sparrow will be faster than slow turtle, and will be able to 'flock together' in parrallel

import cv2 
import numpy as np
import threading
import time
import random
import sys
import lines #local import
import polygon
from screen import Screen
#Global variables for Sparrow
HOME = (0,0)


  
    
def run_parallel(task, sparrow, *args):
  '''run tasks in parallel'''
  thread = threading.Thread(target=task, args=(sparrow, *args))
  thread.start()
  return thread

# def update_screen(screen):
#   """Continuously updates and displays the screen while threads are active."""
#   while any(thread.is_alive() for thread in threading.enumerate() if thread != threading.main_thread()):
#     screen.update()
#     screen.show()
#     time.sleep(0.001)  # More frequent updates

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
    self.colour = (0,0,0)
    self.size = 1
    self.image = 'v^o>'
    self.angle = 0
    self.pen = True
    self.priority = 0 #0 is the highest, 1 is the next highest, etc.
    self.portal=False
    self.filling=False
    self.edges=[]#for filling polygons
    self.flocking=False
    
  def clear(self):
    self.screen.clear()
    self.screen.show()
    
  def goto(self, x, y, penup=False):
    if not penup and self.pen:
      if self.flocking:
        self.__drawline_points(x, y)
      else:
        self.drawline(x, y)
    self.x, self.y = x, y
    # self.screen.show()
    
  def drawline(self, new_x, new_y, filling=False):
    '''used for serial writing. The serial writing at the moment
    is the fastest'''
    curr_x, curr_y = cartesian_2_screen((self.x, self.y))
    new_x, new_y = cartesian_2_screen((new_x, new_y))
    if filling:
      edge = lines.bresenham_edge(curr_x, curr_y, new_x, new_y)
      self.edges.append(edge)
    if self.slowness == 0:  
      self.screen.canvas = lines.bresenham_line((curr_x, curr_y), (new_x, new_y),
        self.screen.canvas, self.colour)
      self.screen.show()
    else:
      self.screen.canvas = lines.bresenham_line((curr_x, curr_y), (new_x, new_y),
        self.screen.canvas, self.colour, self.slowness)
    
  def __drawline_points(self, new_x, new_y, filling=False):
    '''used for parallel writing. slightly slower, but can make some
    interesting things happen'''
    curr_x, curr_y = cartesian_2_screen((self.x, self.y))
    new_x, new_y = cartesian_2_screen((new_x, new_y))
    point_generator = lines.bresenham_points((curr_x, curr_y), (new_x, new_y), self.colour)
    for point in point_generator:
        self.screen.buffer.put((point[0], point[1], point[2]))# point = (x, y, colour)
        time.sleep(0.001)  # Critical: Allows threads to interleave
    if filling:
      edge = lines.bresenham_edge(curr_x, curr_y, new_x, new_y)
      self.edges.append(edge)
  
  def __fill_shape(self):
    self.screen.canvas = polygon.fill_poly(self.screen.canvas, self.edges,
                                           self.colour, self.slowness)
    
  def __fill_shape_points(self):
    point_generator = polygon.fill_poly_points(self.edges)
    for point in point_generator:
      self.screen.buffer.put((point[0], point[1], point[2]))#point = (x,y,colour)
      time.sleep(0.001)
      
  def __new_coordinate(self, distance):
    '''return the new coordinate after moving distance in the angle direction'''
    new_x = self.x + distance * np.cos(self.angle)
    new_y = self.y + distance * np.sin(self.angle)
    # new_x, new_y = self.__portal(new_x, new_y)  
    self.x = new_x
    self.y = new_y
    return (new_x, new_y)
    
  def forward(self, distance):
    '''move the sparrow forward by distance'''
    new_x, new_y = self.__new_coordinate(distance)
    self.goto(new_x, new_y)
    
  
  def backward(self, distance):
    '''move the sparrow backward by distance'''
    new_x, new_y = self.__new_coordinate(-distance)
    self.goto(new_x, new_y)
  
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

  
    
  
  def begin_fill(self):
    '''To fill a polygon, use begin_fill, then draw the edges, and finally use end_fill'''
    self.filling=True

  def end_fill(self):
    '''To fill a polygon, use begin_fill, then draw the edges, and finally use end_fill'''
    self.filling = False
    if self.flocking:
      self.__fill_shape_points()
    else:
      self.__fill_shape()
      
    
  def set_colour(self, colour):
    '''set the colour of the sparrow'''
    self.colour = colour
  
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
    
  def get_position(self):
    '''return the position of the sparrow''' 
    return (self.x, self.y)
    
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

def cartesian_2_screen(coord, screen_size=(799,799)):
  '''convert the cartesian coordinates to screen coordinates'''
  x,y = coord
  x,y = round(x+300), round(300-y)
  return (x,y)

def screen_2_cartesian(coord):
  '''convert the screen coordinates to cartesian coordinates'''
  x,y = coord
  return (x-300, 300-y)

def deg_2_rad(deg):
  '''convert degrees to radians'''
  return deg * np.pi / 180
  
def main():
  print('Hello Sparrow')
  wn = Screen()
  sparrow = Sparrow()
  sparrow.set_slowness(1)
  sparrow.forward(100)
  sparrow.left(deg_2_rad(90))
  sparrow.forward(100)
  sparrow.set_colour((255,0,0))
  sparrow.goto(0,0)
  wn.mainloop()
  

if __name__ == '__main__':
  main()
    