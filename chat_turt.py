import numpy as np
import cv2

class Screen:
    _instance = None  # Singleton instance

    def __new__(cls, width=500, height=500, bg_color=(255, 255, 255)):
        if cls._instance is None:
            cls._instance = super(Screen, cls).__new__(cls)
            cls._instance.width = width
            cls._instance.height = height
            cls._instance.bg_color = bg_color
            cls._instance.canvas = np.ones((height, width, 3), dtype=np.uint8) * np.array(bg_color, dtype=np.uint8)
        return cls._instance

    def show(self):
        cv2.imshow("Turtle Screen", self.canvas)
        cv2.waitKey(1)

    def clear(self):
        self.canvas[:] = self.bg_color

    def update(self):
        cv2.imshow("Turtle Screen", self.canvas)
        cv2.waitKey(1)

class Turtle:
    def __init__(self):
        self.screen = Screen()  # Get the singleton instance
        self.x, self.y = self.screen.width // 2, self.screen.height // 2
        self.color = (0, 0, 0)
        self.thickness = 2

    def move_to(self, x, y):
        cv2.line(self.screen.canvas, (self.x, self.y), (x, y), self.color, self.thickness)
        self.x, self.y = x, y
        self.screen.update()

    def set_color(self, color):
        self.color = color

    def clear(self):
        self.screen.clear()
        self.screen.update()


wn = Screen()  # Creates the screen
turt = Turtle()  # Turtle automatically uses the screen

turt.move_to(100, 100)
turt.set_color((255, 0, 0))  # Change to red
turt.move_to(200, 200)

cv2.waitKey(0)  # Keep the window open
cv2.destroyAllWindows()