from SnakeSquare import SnakeSquare


class Snake:
    def __init__(self, snake_id, name, body, head, length, health):
        self.snake_id = snake_id
        self.name = name
        self.body = [SnakeSquare("B", square["x"], square["y"])
                     for square in body]
        self.head = SnakeSquare("H", head["x"], head["y"])
        self.length = length
        self.health = health
        self.closest_food = None

    def __eq__(self, another_object):
        return self.snake_id == another_object.snake_id

    def __str__(self):
        return f"Snake: {self.name}, with a length of {self.length}"

    def move_towards_food(self, possible_moves):
        closest_food = self.closest_food
        food_snake_y_delta = closest_food.get_y_delta_from_snake(
            self.head)
        food_snake_x_delta = closest_food.get_x_delta_from_snake(self.head)

        if(abs(food_snake_x_delta) - abs(food_snake_y_delta) > 0):
            if(food_snake_x_delta < 0 and "left" in possible_moves):
                possible_moves = ["left"]
            elif(food_snake_x_delta > 0 and "right" in possible_moves):
                possible_moves = ["right"]
        elif(abs(food_snake_x_delta) - abs(food_snake_y_delta) < 0):
            if(food_snake_y_delta > 0 and "down" in possible_moves):
                possible_moves = ["down"]
            elif(food_snake_y_delta < 0 and "up" in possible_moves):
                print("The only way to go is up")
                possible_moves = ["up"]
        else:
            print("It doesn't really matter what way you go")
            return possible_moves

        return possible_moves
