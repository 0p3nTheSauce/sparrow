import threading

def run_parallel(task, sparrow, *args):
    """Helper function to run tasks in parallel"""
    thread = threading.Thread(target=task, args=(sparrow, *args))
    thread.start()
    return thread  # Return thread so we can join later if needed

def triangle(sparrow, distance, pos):
    sparrow.penup()
    sparrow.goto(*pos)
    sparrow.pendown()
    for _ in range(3):
        sparrow.forward(distance)
        sparrow.right(120)

def circle(sparrow, radius, pos):
    sparrow.penup()
    sparrow.goto(pos[0], pos[1] - radius)
    sparrow.pendown()
    for _ in range(36):
        sparrow.forward(2 * 3.14 * radius / 36)
        sparrow.right(10)

# Create sparrows
sparrow1 = Sparrow()
sparrow2 = Sparrow()

# Run functions in parallel using threading
thread1 = run_parallel(triangle, sparrow1, 50, (100, 100))
thread2 = run_parallel(circle, sparrow2, 30, (200, 200))

# Wait for all threads to complete
thread1.join()
thread2.join()