import cv2
import numpy as np
from lines import bresenham_points, bresenham_edge


class Polygon():
  def __init__(self, colour, edges):
    self.edges = edges
    self.colour = colour


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

def get_fill_boundaries(line_points, edges):
  line_points = sorted(line_points, key=lambda x: x[0])
  neighbours = [] 
  def rec_fill(line_points, neighbours, edges):
    if len(line_points) < 2:
      return line_points  
    else:
      pnt1 = line_points[0]
      pnt2 = line_points[1]
      neighbours.append(pnt1)
      if (pnt2[0] - pnt1[0]) == 1: #points are 1 pixel apart
        return rec_fill(line_points[1:], neighbours,edges)
      else: #each point is on an edge 
        in_2, vertex_edges = in_2_edges(neighbours, edges)
        neighbours=[]
        if in_2:#check if points on 2 different edges
          #need to determine if point on a transistion edge
          horizontal = pnt1[1]
          side_edge1 = side_of_screen(horizontal, vertex_edges[0])
          side_edge2 = side_of_screen(horizontal, vertex_edges[1])
          if side_edge1 == side_edge2 or side_edge1 == 0 or side_edge2 == 0:
            #it is an extremal edge (same side of horizontal)
            return rec_fill(line_points[1:], neighbours,edges)
          else:
            #transition edge, keep (diff side horizontal)          
            return [pnt1] + rec_fill(line_points[1:],neighbours,edges) 
        else:
          return [pnt1] + rec_fill(line_points[1:],neighbours,edges) 
  return rec_fill(line_points,neighbours, edges)
  
def side_of_cart(horizontal, edge):
  '''returns an integer based on wether edge is above, hoizontal, or below  
  1,0,-1 respectively. Uses cartesian coordinates. Makes the assumption that
  we are doing this for a point (and possibly it's neighbours) on a vertex'''
  ans = 0
  for point in edge:
    y = point[1]
    if y > horizontal: 
      ans += 1
    elif y < horizontal:
      ans -= 1
  return sign(ans)     

def side_of_screen(horizontal, edge):
  '''returns an integer based on wether edge is above, hoizontal, or below  
  1,0,-1 respectively. Uses screen coordinates. Makes the assumption that
  we are doing this for a point (and possibly it's neighbours) on a vertex'''
  ans = 0
  for point in edge:
    y = point[1]
    if y < horizontal: 
      ans += 1
    elif y > horizontal:
      ans -= 1
  return sign(ans)

def sign(ans):
  if ans > 0:
    return 1
  elif ans < 0:
    return -1
  else:
    return 0
def remove_duplicate_points(points):
  return list(set(points))


def check_points(w, h, y, x1, x2):
  '''checks if points are in range of screen edges'''
  if x1 < 0:
      x1 = 0
  if x2 < 0:
    x2 = 0
  if x1 >= w:
    x1 = w-1
  if x2 >= h:
    x2 = h-1
  if x1 > x2:
    x1, x2 = x2, x1
  if y < 0:
    y = 0
  if y >= h:
    y = h-1
  return y, x1, x2

def fill_lines(fill_bounds, screen, colour=(0,0,0)):
  '''draws horizontal line on screen'''
  if len(fill_bounds) < 2:
    return screen
  else:
    pnt1 = fill_bounds[0]
    pnt2 = fill_bounds[1]
    y = pnt1[1]
    x1 = pnt1[0]
    x2 = pnt2[0]
    w, h = screen.shape[0], screen.shape[1]
    y, x1, x2 = check_points(w, h, y, x1, x2)
    screen[y, x1:x2] = colour
    return fill_lines(fill_bounds[2:],screen)

def fill_lines_points(fill_bounds, colour=(0,0,0)):
  '''returns pixel coordinatesfor horizontal line'''
  if len(fill_bounds) >= 2:
    pnt1 = fill_bounds[0]
    pnt2 = fill_bounds[1]
    y = pnt1[1]
    x1 = pnt1[0]
    x2 = pnt2[0]
    yield (x1,x2,y,colour)
    yield from fill_lines_points(fill_bounds[2:])  
    
def find_in_edges(point, edges):
  return [edge for edge in edges if point in edge]

def in_2_edges(neighbours, edges):
  '''checks if any neighboring points are in 2 edges, and returns edges'''
  vertex_edges = []
  num_edges = 0
  for edge in edges:
    if any(point in edge for point in neighbours):
      vertex_edges.append(edge)
      num_edges += 1
  return num_edges >= 2, vertex_edges
  #return sum(any(point in edge for point in neighbours) for edge in edges) >= 2

def forbidden_shape(screen):
  pnt1 = (100,200)
  pnt2 = (300,500)
  edge1 = bresenham_edge(pnt1, pnt2)
  pnt3 = (400,200)
  edge2 = bresenham_edge(pnt2, pnt3)
  pnt4 = (300,400)
  edge3 = bresenham_edge(pnt3, pnt4)
  edge4 = bresenham_edge(pnt4, pnt1)
  all_edges = edge1+edge2+edge3+edge4
  for point in all_edges: 
    x,y = point
    screen[y,x] = (0,0,0)
  return screen, [edge1,edge2,edge3,edge4]

def seperate_lines(sorted_by_y):
  # sorted_by_y = sorted(points, key=lambda x: x[1])
  seperated_by_line = []
  remaining = sorted_by_y
  y_min, y_max = sorted_by_y[0][1],sorted_by_y[-1][1]
  for i in range(y_min, y_max+1):
    line, remaining = get_line_points(remaining, i)
    seperated_by_line.append(line)
  return seperated_by_line  
  
def fill_poly(screen, edges, colour=(0,0,0), speed=100, slowness=1):
  # sorted_by_x = sorted(points, key=lambda x: x[0])
  all_points = [point for edge in edges for point in edge]
  rem_dup = remove_duplicate_points(all_points)
  sorted_by_y = sorted(rem_dup, key=lambda x: x[1])
  lines = seperate_lines(sorted_by_y)
  count = 0
  for line in lines:
    fill_bounds = get_fill_boundaries(line, edges)
    if fill_bounds is not None:
      screen = fill_lines(fill_bounds, screen, colour)
      if count == speed:
        cv2.imshow('Sparrow Screen', screen)
        cv2.waitKey(slowness)
        count = 0
      else:
        count += 1
  return screen

def fill_poly_points(edges, colour=(0,0,0)):
  all_points = [point for edge in edges for point in edge]
  rem_dup = remove_duplicate_points(all_points)
  sorted_by_y = sorted(rem_dup, key=lambda x: x[1])
  lines = seperate_lines(sorted_by_y)
  for line in lines:
    fill_bounds = get_fill_boundaries(line, edges)
    if fill_bounds is not None:
      yield from fill_lines_points(fill_bounds, colour)

def hard_shape():
  blank = np.ones((600, 600,3)) * 255
  #blank, edge_points = my_shape(blank)
  blank, edge_points = forbidden_shape(blank)
  cv2.imshow('myshape', blank)
  cv2.waitKey(0)
  blank_filled = fill_poly(blank, edge_points, speed=1000, slowness=1)
  cv2.imshow('myshape filled', blank_filled)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  

def forbidden_shape(screen):
  pnt1 = (100,200)
  pnt2 = (300,500)
  edge1 = bresenham_edge(pnt1, pnt2)
  pnt3 = (400,200)
  edge2 = bresenham_edge(pnt2, pnt3)
  pnt4 = (300,400)
  edge3 = bresenham_edge(pnt3, pnt4)
  edge4 = bresenham_edge(pnt4, pnt1)
  all_edges = edge1+edge2+edge3+edge4
  for point in all_edges: 
    x,y = point
    screen[y,x] = (0,0,0)
  return screen, [edge1,edge2,edge3,edge4]
 
def off_shape(screen):
  w, h = screen.shape[0], screen.shape[1]
  pnt1 = (-100,200)
  pnt2 = (500,h+10)
  edge1 = bresenham_edge(pnt1, pnt2)
  pnt3 = (w+100,400)
  edge2 = bresenham_edge(pnt2, pnt3)
  pnt4 = (100,-100)
  edge3 = bresenham_edge(pnt3, pnt4)
  edge4 = bresenham_edge(pnt4, pnt1)
  all_edges = edge1+edge2+edge3+edge4
  for point in all_edges: 
    x,y = point
    w, h = screen.shape[0], screen.shape[1]
    if x < 0 or x >= w or y < 0 or y >= h:
      continue
    else: 
      screen[y,x] = (0,0,0)
  return screen, [edge1,edge2,edge3,edge4]
  
def off_edge():
  blank = np.ones((600, 600,3)) * 255
  blank, edge_points = off_shape(blank)
  cv2.imshow('myshape', blank)
  cv2.waitKey(0)
  blank_filled = fill_poly(blank, edge_points, speed=1000, slowness=1)
  cv2.imshow('myshape filled', blank_filled)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
def main():
  # hard_shape()
  off_edge()

if __name__ == '__main__':
  main()