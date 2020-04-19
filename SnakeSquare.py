class SnakeSquare:
    def __init__(self, square_type, x, y):
        self.square_type = square_type
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"{self.square_type} at x:{self.x}, y:{self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
