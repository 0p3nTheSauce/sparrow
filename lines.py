'''Implement Bresenhams line algorithm'''
import cv2
import numpy as np
import math

def bresenham_slowness(start, end, screen, colour=(0,0,0), slowness=1):
  '''draw a line from start to end on the screen'''
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
    screen[y1,x1] = colour
    cv2.imshow('bresenham', screen)
    key = cv2.waitKey(slowness)
    if key == 27: #esc key
      cv2.destroyAllWindows()
      break
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

def bresenham_line(start, end, screen, colour=(0,0,0)):
  '''draw a line from start to end on the screen'''
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
    screen[y1,x1] = colour
    # cv2.imshow('bresenham', screen)
    # cv2.waitKey(slowness)
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