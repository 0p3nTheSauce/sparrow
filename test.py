import numpy as np

coords = np.array([
    [1, 2],  # (x=10, y=20)
    [3, 4],  # (x=30, y=40)
    [5, 6]   # (x=50, y=60)
])

screen = np.ones((7,7))
screen[coords[:, 1], coords[:, 0]] = 0
print(screen)
print()
print(coords[:, 0])  # Output: [10 30 50]  (all x-coordinates)
print(coords[:, 1])  # Output: [20 40 60]  (all y-coordinates)

print()

def fibonacci():
  a, b = 0, 1
  while True:
      yield a
      a, b = b, a + b

fib_gen = fibonacci()
for _ in range(10):
  print(next(fib_gen))  # Prints first 10 Fibonacci numbers