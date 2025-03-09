class Screen:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height

class Sparrow:
    def __init__(self):
        # Initialize the Screen instance
        self.canvas = Screen(width=800, height=900)

        # Use self.canvas to initialize other variables
        self.x_min = -self.canvas.width // 2
        self.x_max = self.canvas.width // 2

# Create an instance of Sparrow
jack = Sparrow()

# Check the initialized values
print(f"Canvas width: {jack.canvas.width}")  # Output: Canvas width: 800
print(f"x_min: {jack.x_min}")  # Output: x_min: -400
print(f"x_max: {jack.x_max}")  # Output: x_max: 400