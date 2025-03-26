import cv2
import numpy as np
def bresenham_points(start, end,colour=(0,0,0)):
  '''generate the points of a line from start to end'''
  x1,y1 = start
  x2,y2 = end
  points = []
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
    # yield (x1,y1,colour)
    points.append((x1,y1))
    if x1==x2 and y1==y2:
      break
    e2 = 2*err
    if e2 > -dy:
      err = err - dy
      x1 = x1 + sx
    if e2 < dx:
      err = err + dx
      y1 = y1 + sy
  return points

def my_shape(screen):
  pnt1 = (100,100)
  pnt2 = (500,500)
  edge1 = bresenham_points(pnt1, pnt2)
  pnt3 = (500,400)
  edge2 = bresenham_points(pnt2, pnt3)
  pnt4 = (100,400)
  edge3 = bresenham_points(pnt3, pnt4)
  edge4 = bresenham_points(pnt4, pnt1)
  all_edges = edge1+edge2+edge3+edge4
  for point in all_edges: 
    x,y = point
    screen[y,x] = (0,0,0)
  return screen, all_edges
    
def one_line(screen):
  pnt1 = (100,100)
  pnt2 = (500,500)
  edge1 = bresenham_points(pnt1, pnt2)
  for point in edge1: 
    x,y = point
    screen[y,x] = (0,0,0)
  return screen
  
def get_line(sorted_by_y, i, line_num):
  line = []
  pnt = sorted_by_y[i]
  while pnt[1] == line_num:
    line.append(pnt)
    i += 1
    if i < len(sorted_by_y):
      break
    pnt = sorted_by_y[i]
  return line, i
  
  
def fill_poly(screen, points):
  # sorted_by_x = sorted(points, key=lambda x: x[0])
  sorted_by_y = sorted(points, key=lambda x: x[1])

  y_min = sorted_by_y[0][1]
  y_max = sorted_by_y[-1][1]
  i = 0
  line_num = y_min
  while i < len(points):
    line, i = get_line(sorted_by_y, i, line_num)
    line = sorted(line, key=lambda x: x[0])
    line_num += 1
    point_pos = 1
    x_min = line[0][0]
    if point_pos < len(line):
      next_x = line[point_pos][0]
    else:
      next_x = line[-1][0]
    x_max = line[-1][0]
    on_shape = True
    for j in range(x_min+1, x_max):
      if (j == next_x):
        point_pos += 1
        if point_pos >= len(line):
          break
        next_x = line[point_pos][0]
        on_shape = not on_shape
      if on_shape:
        if i < 600 and j < 600:
          screen[i,j] = (0,0,0)
    cv2.imshow('filling', screen)
    cv2.waitKey(5)
        
        
  return screen

def main():
  blank = np.ones((600, 600,3)) * 255
  blank, edge_points = my_shape(blank)
  cv2.imshow('myshape', blank)
  cv2.waitKey(0)
  blank_filled = fill_poly(blank, edge_points)
  cv2.imshow('myshape filled', blank_filled)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()