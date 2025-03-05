import threading
import numpy as np
import cv2
import queue
import time
import lines  # Local import

class Screen:
    _instance = None

    def __new__(cls, width=500, height=500, bg_color=(255, 255, 255)):
        if cls._instance is None:
            cls._instance = super(Screen, cls).__new__(cls)
            cls._instance.width = width
            cls._instance.height = height
            cls._instance.bg_color = bg_color
            cls._instance.buffer = queue.Queue()  # Thread-safe queue
            cls._instance.canvas = np.ones((height, width, 3), dtype=np.uint8) * np.array(bg_color, dtype=np.uint8)
        return cls._instance

    def update(self):
        """Apply buffered updates from the queue to the screen canvas."""
        while not self.buffer.empty():
            x, y = self.buffer.get()
            self.canvas[y, x] = (0, 0, 0)  # Update with black color

    def show(self):
        cv2.imshow("Sparrow Screen", self.canvas)
        cv2.waitKey(1)  # Allows real-time updates

class Sparrow(threading.Thread):
    def __init__(self, name, start_pos, end_pos):
        super().__init__()
        self.screen = Screen()
        self.name = name
        self.x, self.y = start_pos
        self.end_x, self.end_y = end_pos

    def __drawline_points(self):
        """Generate points and add them to the screen buffer."""
        point_generator = lines.bresenham_points((self.x, self.y), (self.end_x, self.end_y))
        for point in point_generator:
            self.screen.buffer.put(point)  # Thread-safe update
            time.sleep(0.01)  # Simulate movement delay

    def run(self):
        """Thread's execution starts here."""
        print(f"{self.name} started drawing.")
        self.__drawline_points()
        print(f"{self.name} finished drawing.")

# Initialize screen
screen = Screen()

# Create multiple Sparrow instances running in parallel
sparrow1 = Sparrow("Sparrow 1", (50, 50), (450, 450))
sparrow2 = Sparrow("Sparrow 2", (450, 50), (50, 450))
sparrow3 = Sparrow("Sparrow 3", (250, 50), (250, 450))

# Start sparrows in separate threads
sparrow1.start()
sparrow2.start()
sparrow3.start()

# Keep updating and showing the screen in the main thread
while sparrow1.is_alive() or sparrow2.is_alive() or sparrow3.is_alive():
    screen.update()
    screen.show()
    time.sleep(0.05)  # Adjust refresh rate

# Final update and display
screen.update()
screen.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
