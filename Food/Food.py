# Simple food object, some coordinates and simple function
class Food:
    def __init__(self, x, y, closest=False):
        self.x = x
        self.y = y
        self.closest = closest

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

    # Simple logging function
    def __str__(self):
        return f"Food is at position x={self.x} and y={self.y}"
