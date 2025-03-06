import cv2
import numpy as np
import queue
import threading
import time
import lines  # local import

class Screen:
    _instance = None

    def __new__(cls, width=600, height=600, bg_color=(255, 255, 255), colour=(0, 0, 0)):
        if cls._instance is None:
            cls._instance = super(Screen, cls).__new__(cls)
            cls._instance.width = width
            cls._instance.height = height
            cls._instance.bg_color = bg_color
            cls._instance.colour = colour
            cls._instance.slowness = 0
            cls._instance.buffer = queue.Queue()
            cls._instance.canvas = np.ones((height, width, 3),
                                           dtype=np.uint8) * np.array(bg_color, dtype=np.uint8)
        return cls._instance

    def show(self):
        cv2.imshow("Sparrow Screen", self.canvas)
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()

    def clear(self):
        self.canvas[:] = self.bg_color

    def update(self):
        while not self.buffer.empty():
            x, y = self.buffer.get()
            self.canvas[y, x] = self.colour  # HACK: doesn't use sparrows colour, and probably slow

def run_parallel(task, sparrow, *args):
    '''run tasks in parallel'''
    thread = threading.Thread(target=task, args=(sparrow, *args))
    thread.start()
    return thread

def update_screen(screen):
    """Continuously updates and displays the screen while threads are active."""
    while any(thread.is_alive() for thread in threading.enumerate() if thread != threading.main_thread()):
        screen.update()
        screen.show()
        time.sleep(0.05)  # Adjust refresh rate

    # Final update and display
    screen.update()
    screen.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class Sparrow:
    def __init__(self):
        self.screen = Screen()
        self.slowness = 1
        self.x, self.y = self.screen.width // 2, self.screen.height // 2
        self.color = (0, 0, 0)
        self.size = 1
        self.image = 'v^o>'
        self.angle = 0
        self.pen = True
        self.priority = 0  # 0 is the highest, 1 is the next highest, etc.

    def clear(self):
        self.screen.clear()
        self.screen.show()

    def goto(self, x, y):
        x, y = cartesian_2_screen((x, y))
        if self.pen:
            self.__drawline(x, y)
        self.x, self.y = x, y
        # self.screen.show()

    def __drawline(self, *args):
        if len(args) == 1:
            distance = args[0]
            new_x, new_y = new_coordinate((self.x, self.y), self.angle, distance)
        elif len(args) == 2:
            new_x, new_y = args
        else:
            raise ValueError('Invalid number of arguments')

        new_x, new_y = int(new_x), int(new_y)  # Convert to integers

        if self.pen:
            if self.slowness == 0:
                cv2.line(self.screen.canvas, (self.x, self.y), (new_x, new_y),
                         self.color, self.size)
            else:
                self.screen.canvas = lines.bresenham_slowness((self.x, self.y), (new_x, new_y),
                                                              self.screen.canvas, self.color, self.slowness)
        self.x = new_x
        self.y = new_y
        self.screen.show()

    def __drawline_points(self, *args):
        if len(args) == 1:
            distance = args[0]
            new_x, new_y = new_coordinate((self.x, self.y), self.angle, distance)
        elif len(args) == 2:
            new_x, new_y = args
        else:
            raise ValueError('Invalid number of arguments')

        point_generator = lines.bresenham_points((self.x, self.y), (new_x, new_y))
        for point in point_generator:
            self.screen.buffer.put(point)

        self.x = new_x
        self.y = new_y

    def forward(self, distance):
        '''move the sparrow forward by distance'''
        self.__drawline_points(distance)

    def backward(self, distance):
        '''move the sparrow backward by distance'''
        self.__drawline_points(-distance)

    def left(self, angle):
        '''turn the sparrow left by angle'''
        self.angle += angle

    def right(self, angle):
        '''turn the sparrow right by angle'''
        self.angle -= angle

    def penup(self):
        '''stop drawing'''
        self.pen = False

    def pendown(self):
        '''start drawing'''
        self.pen = True

    def set_color(self, color):
        '''set the color of the sparrow'''
        self.color = color

    def set_size(self, size):
        '''set the size of the sparrow'''
        self.size = size

    def set_image(self, image):
        '''set the image of the sparrow'''
        self.image = image

    def set_angle(self, angle):
        '''set the angle of the sparrow'''
        self.angle = angle

    def set_position(self, x, y):
        '''set the position of the sparrow'''
        self.x = x
        self.y = y

    def set_slowness(self, slowness):
        '''set the slowness of the sparrow'''
        self.slowness = slowness

def new_coordinate(coord, angle, distance):
    '''return the new coordinate after moving distance in the angle direction'''
    x, y = screen_2_cartesian(coord)
    new_x = x + distance * np.cos(angle)
    new_y = y + distance * np.sin(angle)
    return cartesian_2_screen((new_x, new_y))

def blank():
    '''create a blank white image with a black diagonal line'''
    blank = np.ones((600, 600, 3)) * 255
    # cv2.line(blank, (0,0), (600,600), (0,0,0), 3)
    return blank

def small_circle(coord, screen, colour=(0, 0, 0)):
    '''draw a small circle at x,y on the screen'''
    x, y = coord
    x, y = cartesian_2_screen((x, y))
    cv2.circle(screen, (x, y), 10, colour, -1)
    return screen

def small_triangle(coord, screen, colour=(0, 0, 0)):
    '''draw a small triangle at x,y on the screen'''
    x, y = coord
    x, y = cartesian_2_screen((x, y))
    points = np.array([[x, y-5], [x-5, y+5], [x+5, y+5]], dtype=np.int32)
    cv2.fillPoly(screen, [points], colour)
    return screen

def tup_2_np(tup):
    '''convert a tuple to a numpy array'''
    return np.array(tup)

def directed_triangle(coord, angle, screen, colour=(0, 0, 0), size=10):
    '''draw a small triangle at x,y on the screen'''
    x, y = coord
    a_angle = angle + np.pi / 2  # 90 degrees
    b_angle = angle - np.pi / 2  # 90 degrees
    a = new_coordinate((x, y), a_angle, size)
    b = new_coordinate((x, y), b_angle, size)
    c = new_coordinate((x, y), angle, size)

    a = cartesian_2_screen(a)
    b = cartesian_2_screen(b)
    c = cartesian_2_screen(c)

    points = np.array([a, b, c], dtype=np.int32)

    cv2.fillPoly(screen, [points], colour)
    return screen

def cartesian_2_screen(coord):
    '''convert the cartesian coordinates to screen coordinates'''
    x, y = coord
    return (int(x + 300), int(300 - y))

def screen_2_cartesian(coord):
    '''convert the screen coordinates to cartesian coordinates'''
    x, y = coord
    return (x - 300, 300 - y)

def deg_2_rad(deg):
    '''convert degrees to radians'''
    return deg * np.pi / 180

def test_directed_triangle():
    blank_ = blank()
    tri = directed_triangle((0, 0), deg_2_rad(30), blank_)
    cv2.imshow('tri', tri)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def triangle(sparrow, distance, pos):
    sparrow.penup()
    sparrow.goto(*pos)
    sparrow.pendown()
    for _ in range(3):
        sparrow.forward(distance)
        sparrow.right(120)

def test_basic():
    wn = Screen()
    sparrow = Sparrow()
    sparrow.set_slowness(1)
    sparrow.forward(100)
    sparrow.left(deg_2_rad(90))
    sparrow.forward(100)
    sparrow.set_color((255, 0, 0))
    sparrow.goto(0, 0)
    wn.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_parallel():
    wn = Screen()
    rock = Sparrow()
    petronia = Sparrow()

    # Start drawing tasks in parallel
    thread1 = run_parallel(triangle, rock, 50, (100, 100))
    thread2 = run_parallel(triangle, petronia, 30, (200, 200))

    # Start screen updates in a separate thread
    screen_thread = threading.Thread(target=update_screen, args=(wn,))
    screen_thread.start()

    # Wait for drawing tasks to finish
    thread1.join()
    thread2.join()

    # Once all drawing threads finish, wait for the screen update thread to exit
    screen_thread.join()

    

def main():
    test_parallel()

if __name__ == '__main__':
    main()