# Simple class - one square, good for helping
# undersatnd the snake intuitively/logging


class SnakeSquare:
    def __init__(self, square_type, x, y):
        self.square_type = square_type
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"{self.square_type} at x:{self.x}, y:{self.y}"

    def __eq__(self, other):
        if(isinstance(other, SnakeSquare)):
            return self.x == other.x and self.y == other.y
        else:
            return False

    # Gets delta of food from snake
    def get_y_delta_from_snake(self, head):
        return self.y - head.y

    def get_x_delta_from_snake(self, head):
        return self.x - head.x

    # Sum of delta to find closest food.
    def get_delta_sum(self, head):
        y_delta = self.get_y_delta_from_snake(head)
        x_delta = self.get_x_delta_from_snake(head)
        return abs(y_delta) + abs(x_delta)
