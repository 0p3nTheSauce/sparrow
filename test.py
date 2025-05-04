import numpy as np
import cv2
import random
from sparrow import Sparrow, run_parallel, directed_trianlge, deg_2_rad, screen_2_cartesian
from screen import Screen
import time

def test_directed_triangle():
  blank = np.ones((600,600), np.int8)*255
  #spot = small_circle(300,300, blank)
  # cv2.imshow('blank', blank_)
  tri = directed_trianlge((0,0), deg_2_rad(30), blank)
  
  # cv2.imshow('spot', spot)  
  cv2.imshow('tri', tri)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def test_basic():
  wn = Screen()
  sparrow = Sparrow()
  sparrow.set_slowness(1)
  sparrow.forward(100)
  sparrow.left(deg_2_rad(90))
  sparrow.forward(100)
  sparrow.set_color((255,0,0))
  sparrow.goto(0,0)
  # sparrow.screen.show()
  wn.show()
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
def test_parallel():
  start_time = time.perf_counter()
  wn = Screen()
  rock = Sparrow()
  petronia = Sparrow()
  house = Sparrow()
  eurasian_tree = Sparrow()
  # thread1 = run_parallel(rand_triangle, rock, 100)
  # thread2 = run_parallel(rand_triangle, petronia, 100)
  # thread3 = run_parallel(rand_triangle, house, 100)
  # thread4 = run_parallel(rand_triangle, eurasian_tree, 100)
  thread1 = run_parallel(swim_randomly, rock, 10)
  thread2 = run_parallel(swim_randomly, petronia, 10)
  thread3 = run_parallel(swim_randomly, house, 10)
  thread4 = run_parallel(swim_randomly, eurasian_tree, 10)
  
  
  wn.mainloop()
  end_time = time.perf_counter()
  print(f"Time taken: {end_time-start_time} seconds")
  thread1.join()
  thread2.join()
  thread3.join()
  thread4.join()

def better_triangle(sparrow, distance, pos=(0,0)):
  sparrow.goto(*pos, penup=True)
  sparrow.drawline(distance)
  sparrow.right(deg_2_rad(120))
  sparrow.drawline(distance)
  sparrow.goto(*pos,drawline=True) 

def triangle(sparrow, distance):
  # sparrow.penup()
  # sparrow.goto(*pos)
  # sparrow.pendown()
  for _ in range(3):
    sparrow.drawline(distance)
    sparrow.right(deg_2_rad(120))

def test_big_triangle():
  wn = Screen()
  rock = Sparrow()
  triangle(rock, 100, (100,100))
  
  wn.mainloop()
  
def rand_triangle(sparrow,distance,drawline=False):
  sparrow.portal=True
  for _ in range(100):
    sparrow.penup()
    rand_x = random.randint(-200,200)
    rand_y = random.randint(-200,200)
    sparrow.goto(rand_x,rand_y)
    sparrow.pendown()
    point_up = random.choice([True, False])
    if point_up:
      for _ in range(3):
        sparrow.forward(distance,drawline)
        sparrow.left(deg_2_rad(120))
    else:
      for _ in range(3):
        sparrow.forward(distance,drawline)
        sparrow.right(deg_2_rad(120))

def test_more_triangles():
  wn = Screen()
  rock = Sparrow()
  rock.set_slowness(0)
  #triangle(rock, 100)
  dl=True
  for _ in range(4):
    rand_triangle(rock, 100,drawline=dl)
  wn.mainloop(drawline=dl)
  
def benchmark(func):
  start_time = time.perf_counter()
  func()
  end_time = time.perf_counter()
  print(f"Time taken: {end_time-start_time} seconds")

def swim_randomly(sparrow, distance):
  for _ in range(100):
    for _ in range(100):
      dir = random.randint(-360,360)
      sparrow.left(deg_2_rad(dir))
      sparrow.forward(distance)
      
def cross_y_borders_left():
  wn = Screen()
  rock = Sparrow()
  # rock.set_slowness(1)
  # rock.right(deg_2_rad(90))
  fsx,fsy = screen_2_cartesian((0,0))
  rock.goto(fsx,fsy,penup=True)
  print("got passed goto")
  # for _ in range(798):
  #   rock.forward(1, drawline=True)
  # print("succeeded")
  rock.left(deg_2_rad(90))
  for _ in range(798):
    rock.forward(1, drawline=True)  
  

def cross_y_borders_right():
  wn = Screen()
  rock = Sparrow()
  # rock.set_slowness(1)
  # rock.right(deg_2_rad(90))
  fsx,fsy = screen_2_cartesian((0,798))
  rock.goto(fsx,fsy,penup=True)
  print("got passed goto")
  # for _ in range(798):
  #   rock.forward(1, drawline=True)
  # print("succeeded")
  rock.right(deg_2_rad(90))
  for _ in range(798):
    rock.forward(1, drawline=True)  
  # wn.mainloop()
  # rock.goto()



def test_basic_shape(sparr):
  sparr.penup()
  # sparr.begin_fill()
  sparr.goto(-100,200)
  sparr.pendown()
  sparr.goto(-90,0)
  sparr.goto(90, 10)
  sparr.goto(100, 210)
  sparr.goto(-100,200)
  # sparr.set_speed(0)
  # sparr.set_slowness(2)
  # sparr.end_fill()
  
def test_basic_shape_serial():
  wn = Screen()
  rock = Sparrow()
  test_basic_shape(rock)
  wn.mainloop()
  
def test_basic_shape_parallel():
  wn = Screen()
  rock = Sparrow()
  rock.flock()
  run_parallel(test_basic_shape, rock)
  wn.mainloop()
  
def main():
  #test_parallel()
  #test_big_triangle()
  #test_more_triangles()
  #test_basic_shape_seriel()
  test_basic_shape_parallel()
  # test_basic_shape_serial()
  #benchmark(test_parallel)
  
  #benchmark(test_more_triangles)
  #cross_y_borders_left()
  #cross_y_borders_right()
  
if __name__ == '__main__':
  main()