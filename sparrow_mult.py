import cv2
import numpy as np
import time
from multiprocessing import Process, Queue

#local imports
import lines
import polygon
from screen_mult import Screen

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
    # self.flocking = flocking
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
      spar = Sparrow(self.poly_buff, self.point_buff, self.flock)
      # spar.flock()
      clutch.append(spar)
    return clutch
  
  # def flock(self):
  #   '''make a flock of sparrows'''
  #   self.flocking = True
    # self.flock.put(self)
    # print(f'{self.name} is now flocking')
    
  