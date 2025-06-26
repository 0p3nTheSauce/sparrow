from screen_mult import Screen
from sparrow_mult import Sparrow
from sparrow import deg_2_rad
import cv2

def test_basic():
  wn = Screen()
  sparr = Sparrow(screen=wn)
  # proc = sparr.fly_parallel(triangle2)
  sparr.set_colour((255,0,0))
  for _ in range(3):
    sparr.forward(100)
    sparr.left(90)
  
  sparr.goto(0,0)
  
  sparr.set_colour((0,255,0))
  for _ in range(3):
    sparr.forward(10)
    sparr.left(90)
  wn.mainloop()

  
def square2(sparr):
  sparr.set_colour((255,0,0))
  for _ in range(3):
    sparr.forward(100)
    sparr.left(deg_2_rad(90))
  
  sparr.goto(0,0)
  
  sparr.set_colour((0,255,0))
  for _ in range(3):
    sparr.forward(10)
    sparr.left(deg_2_rad(90))
    
def main():
  test_basic()
  
if __name__ == '__main__':
  main()
  
  