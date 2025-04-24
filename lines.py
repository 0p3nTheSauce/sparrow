'''Implement Bresenhams line algorithm'''
import cv2
import numpy as np
import math

def bresenham_points(start, end,colour=(0,0,0)):
  '''generate the points of a line from start to end'''
  x1,y1 = start
  x2,y2 = end
  dx = abs(x2-x1)
  dy = abs(y2-y1)
  if x1<x2:
    sx = 1
  else:
    sx = -1
  if y1<y2:
    sy = 1
  else:
    sy = -1
  err = dx-dy
  while True:
    yield (x1,y1,colour)
    if x1==x2 and y1==y2:
      break
    e2 = 2*err
    if e2 > -dy:
      err = err - dy
      x1 = x1 + sx
    if e2 < dx:
      err = err + dx
      y1 = y1 + sy

def bresenham_edge(start, end):
  '''generate the points of a line from start to end'''
  edge = []
  x1,y1 = start
  x2,y2 = end
  dx = abs(x2-x1)
  dy = abs(y2-y1)
  if x1<x2:
    sx = 1
  else:
    sx = -1
  if y1<y2:
    sy = 1
  else:
    sy = -1
  err = dx-dy
  while True:
    edge.append((x1,y1))
    if x1==x2 and y1==y2:
      break
    e2 = 2*err
    if e2 > -dy:
      err = err - dy
      x1 = x1 + sx
    if e2 < dx:
      err = err + dx
      y1 = y1 + sy
  return edge

def bresenham_line(start, end, screen, colour=(0,0,0), slowness=0):
  '''draw a line from start to end on the screen'''
  x1,y1 = start
  x2,y2 = end
  wait = 1
  num_skip = 0
  if slowness > 0:
    if slowness > 10:
      wait = slowness // 10
      slowness = 10
    num_skip = 10 - slowness

  count = 0
  dx = abs(x2-x1)
  dy = abs(y2-y1)
  if x1<x2:
    sx = 1
  else:
    sx = -1
  if y1<y2:
    sy = 1
  else:
    sy = -1
  err = dx-dy
  while True:
    screen[y1,x1] = colour
    if count != 0 and count == num_skip:
      cv2.imshow('Sparrow Screen', screen)
      cv2.waitKey(wait)
      count = 0
    else:
      count += 1
    if x1==x2 and y1==y2:
      break
    e2 = 2*err
    if e2 > -dy:
      err = err - dy
      x1 = x1 + sx
    if e2 < dx:
      err = err + dx
      y1 = y1 + sy
  return screen


  

def edge_dir(edge):
  '''assumes edge is a collection of points'''
  x0,y0 = edge[0]
  x1,y1 = edge[-1]
  slope = (y1-y0)/(x1-x0)
  intercept = y1 - (slope * x1)
  return slope, intercept
  
def main():
  blank = np.ones((600, 600,3)) * 255
  start = (300,10)
  end = (590,590)
  blank = bresenham_line(start, end, blank)
  cv2.imshow('bresenham', blank)
  cv2.waitKey(0)
  cv2.destroyAllWindows()



if __name__ == '__main__':
  main()