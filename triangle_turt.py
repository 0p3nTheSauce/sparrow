import turtle
import math
    
def triangle(turt, dist, centre=(0,0)):
  #adjust turtles position so triangle is centered
  turt.penup()
  left = dist/2
  down = (math.sqrt(dist**2 - left**2)/2)
  turt.goto(centre[0]-left, centre[1]-down)
  # turt.goto(centre[0]-left, centre[1]+down)
  turt.pendown()
  xs = []
  ys = []
  for i in range(3):
    x, y = turt.pos()
    xs.append(x)
    ys.append(y)
    turt.forward(dist)
    turt.left(120)
    # turt.right(120)
  return xs, ys    

def output(xs, ys):
  for i in range(len(xs)):
    print(f"X: {xs[i]}; Y: {ys[i]}")
  print()

def midpoint(s1, s2):
  return ((s2 - s1)//2)+s1

def midpoints(xs, ys):
  mxs = []
  mys = []
  for i in range(-1, len(xs)-1):
    mxs.append(midpoint(xs[i], xs[i+1]))
    mys.append(midpoint(ys[i], ys[i+1]))
  return mxs, mys

def new_triangles(xs, ys):
  mxs, mys = midpoints(xs, ys)
  #1 triangle products 4 trangles. However, for sierpinskis fractal we are only interested in 3 of them.
  # which is the middle triangle, in this case the 3rd, which is commented out
  #1st
  tr1x = []
  tr1y = []
  tr1x.extend([xs[0], mxs[1], mxs[0]])
  tr1y.extend([ys[0], mys[1], mys[0]])
  tr1 = (tr1x, tr1y)
  #2nd
  tr2x = []
  tr2y = []
  tr2x.extend([mxs[1], xs[1], mxs[2]])
  tr2y.extend([mys[1], ys[1], mys[2]])
  tr2 = (tr2x, tr2y)
  #3rd
  # tr3x = []
  # tr3y = []
  # tr3x.extend([mxs[0], mxs[1], mxs[2]])
  # tr3y.extend([mys[0], mys[1], mys[2]])
  # tr3 = (tr3x, tr3y)
  #4th
  tr4x = []
  tr4y = []
  tr4x.extend([mxs[0], mxs[2], xs[2]])
  tr4y.extend([mys[0], mys[2], ys[2]])
  tr4 = (tr4x, tr4y)
  # return [tr1, tr2, tr3, tr4]
  return [tr1, tr2, tr4]

def draw_triangles(triangles):
  for tr in triangles:
    xs, ys = tr
    connect_pnts(xs, ys)
  
def sierpinski(triangles, depth=7):
  fill = False
  if depth < 1:
    return
  elif depth == 1:
    fill = True
  for tr in triangles:
    xs, ys = tr
    next = new_triangles(xs, ys)
    connect_pnts(xs, ys, fill)
    sierpinski(next, depth-1)

def connect_pnts(xs, ys, fill=False):
  turt = turtle.Turtle()
  if fill:
    turt.fillcolor("black")
    turt.begin_fill()
  turt.speed(0)
  turt.penup()
  turt.goto(xs[0], ys[0])
  turt.pendown()
  for i in range(len(xs)):
    turt.goto(xs[i], ys[i])
  turt.goto(xs[0], ys[0])
  if fill:
    turt.end_fill()
  
  turt.hideturtle()

def testing(turt, xs, ys):
  bean = turt
  
  output(xs, ys)
  
  
  mxs, mys = midpoints(xs, ys)
  
  connect_pnts(mxs, mys)
  
  nmxs, nmys = midpoints(mxs, mys)
  
  connect_pnts(nmxs, nmys)
  
  #clear screen
  bean.clear()
  
  draw_triangles(new_triangles(xs, ys))
  
  output(mxs, mys)

def main():
  bean = turtle.Turtle()
  bean.speed(0)
  wn = turtle.Screen()
  
  xs, ys = triangle(bean, 600)
  # xs, ys, mxs, mys = triangle(bean, 400)
  
  sierpinski([(xs, ys)])
  
  #testing(bean, xs, ys)
  
  bean.hideturtle()
  wn.mainloop()
    
if __name__ == "__main__":
  main()
  