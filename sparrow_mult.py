import cv2
import numpy as np
import time
from multiprocessing import Process, Queue

#local imports
import lines
import polygon
from screen_mult import Screen
from sparrow import cartesian_2_screen, screen_2_cartesian, deg_2_rad

def run_parallel(task, *args):
  '''run tasks in parallel'''
  proc = Process(target=task, args=args)
  proc.start()
  return proc

class Sparrow:
  def __init__(self, poly_buff, point_buff, flock
      , name='rock'
      , speed=5, slowness=1, x=0, y=0
      , colour=(0,0,0), size=1, image='v^o>'
      , angle=0, pen=True, portal=False
      , filling=False, edges=[]
      # , flocking=False
      ):
    self.name=name
    self.speed=speed
    self.slowness=slowness
    self.x = x
    self.y = y
    self.colour = colour
    self.size = size
    self.image = image
    self.angle = angle
    self.pen = pen
    self.portal = portal
    self.filling = filling
    self.edges = edges #for filling polygons
    self.point_buff = point_buff
    self.poly_buff = poly_buff
    self.flock = flock
      
  def fly_parallel(self, task, args=()):
    spargs = (self,) + args
    proc = Process(target=task, args=spargs)
    self.flock.put(proc)
    proc.start()
    return proc
  
  def spawn(self, n):
    clutch = []
    for _ in range(n):
      spar = Sparrow(self.poly_buff, self.point_buff
                     , self.flock)
      clutch.append(spar)
    return clutch

  def goto(self, x, y, penup=False):
    '''move to a new position'''
    if not penup and self.pen:
      self.__drawline_points(x, y)
    self.x, self.y = x, y
    
  def __drawline_points(self, x, y):
    '''draw a line to the new position'''
    if self.x == x and self.y == y:
      return
    curr_x, curr_y = cartesian_2_screen((self.x
      , self.y))
    new_x, new_y = cartesian_2_screen((x, y))
    point_generator = lines.bresenham_points(
      (curr_x, curr_y), (new_x, new_y), self.colour)
    edge = []
    for point in point_generator:
      self.point_buff.put(point)
      if self.filling:
        edge.append(point[:2])
      time.sleep(0.001) #allow processes to interleave
    if self.filling:
      self.edges.append(edge)
        
  def __fill_shape_flock(self):
    poly = polygon.Polygon(self.colour, self.edges)
    self.poly_buff.put(poly)
    
  def __new_coordinate(self, distance):
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
    
    self.angle += deg_2_rad(angle)
  
  def right(self, angle):
    '''turn the sparrow right by angle'''
    self.angle -= deg_2_rad(angle)
  
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
    self.__fill_shape_flock()
    
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

  def set_speed(self, speed):
    self.speed = speed