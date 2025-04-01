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
  pnt1 = (100,200)
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
  #seems to be a non destructive version of get_line points
  line = []
  pnt = sorted_by_y[i]
  while pnt[1] == line_num:
    line.append(pnt)
    i += 1
    if i < len(sorted_by_y):
      break
    pnt = sorted_by_y[i]
  return line, i

def get_line_points(points, curr_y):
  #gets the current line, and removes the remaining points
  line_points = []
  removed = 0
  for point in points:
    if point[1] == curr_y:
      line_points.append(point)
      removed += 1
    else:
      break
  return line_points, points[removed:]

def get_fill_boundaries(line_points):
  line_points = sorted(line_points, key=lambda x: x[0])
  
  def rec_fill(line_points):
    if len(line_points) < 2:
      return line_points  
    else:
      pnt1 = line_points[0]
      pnt2 = line_points[1]
      if (pnt2[0] - pnt1[0]) == 1: #points are 1 pixel apart, take second
        return rec_fill(line_points[1:])
      else: #each point is on an edge and should be kept
        return [pnt1] + rec_fill(line_points[1:])
  
  return rec_fill(line_points)
  
        
def remove_duplicate_points(points):
  return list(set(points))

def fill_lines(fill_bounds, screen):
  if len(fill_bounds) < 2:
    return screen
  else:
    pnt1 = fill_bounds[0]
    pnt2 = fill_bounds[1]
    y = pnt1[1]
    x1 = pnt1[0]
    x2 = pnt2[0]
    screen[y, x1:x2] = (0,0,0)
    return fill_lines(fill_bounds[2:],screen)

def forbidden_shape(screen):
  pnt1 = (100,200)
  pnt2 = (300,500)
  edge1 = bresenham_points(pnt1, pnt2)
  pnt3 = (400,200)
  edge2 = bresenham_points(pnt2, pnt3)
  pnt4 = (300,400)
  edge3 = bresenham_points(pnt3, pnt4)
  edge4 = bresenham_points(pnt4, pnt1)
  all_edges = edge1+edge2+edge3+edge4
  for point in all_edges: 
    x,y = point
    screen[y,x] = (0,0,0)
  return screen, all_edges

def seperate_lines(sorted_by_y):
  # sorted_by_y = sorted(points, key=lambda x: x[1])
  seperated_by_line = []
  remaining = sorted_by_y
  y_min, y_max = sorted_by_y[0][1],sorted_by_y[-1][1]
  for i in range(y_min, y_max+1):
    line, remaining = get_line_points(remaining, i)
    seperated_by_line.append(line)
  return seperated_by_line  
  
def fill_poly(screen, points):
  # sorted_by_x = sorted(points, key=lambda x: x[0])
  rem_dup = remove_duplicate_points(points)
  sorted_by_y = sorted(rem_dup, key=lambda x: x[1])
  lines = seperate_lines(sorted_by_y)
  for line in lines:
    fill_bounds = get_fill_boundaries(line)
    screen = fill_lines(fill_bounds, screen)
  return screen

def main():
  blank = np.ones((600, 600,3)) * 255
  # blank, edge_points = my_shape(blank)
  blank, edge_points = forbidden_shape(blank)
  cv2.imshow('myshape', blank)
  cv2.waitKey(0)
  blank_filled = fill_poly(blank, edge_points)
  cv2.imshow('myshape filled', blank_filled)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()