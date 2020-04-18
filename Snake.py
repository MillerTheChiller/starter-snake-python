from SnakeSquare import SnakeSquare
import copy


class Snake:
    def __init__(self, snake_id, name, body, head, length, health):
        self.snake_id = snake_id
        self.name = name
        self.body = body
        self.head = head
        self.length = length
        self.health = health
        self.closest_food = None

    def __eq__(self, another_object):
        return self.snake_id == another_object.snake_id

    def __str__(self):
        return f"Snake: {self.name}, with a length of {self.length}"

    def next_move(self, positional_move):
        new_head = None
        if(positional_move == "up"):
            new_head = SnakeSquare(self.head.square_type,
                                   self.head.x, self.head.y-1)
        elif(positional_move == "down"):
            new_head = SnakeSquare(self.head.square_type,
                                   self.head.x, self.head.y + 1)
        elif(positional_move == "right"):
            new_head = SnakeSquare(self.head.square_type,
                                   self.head.x+1, self.head.y)
        elif(positional_move == "left"):
            new_head = SnakeSquare(self.head.square_type,
                                   self.head.x-1, self.head.y)

        new_body = copy.deepcopy(self.body)
        new_body.insert(0, SnakeSquare("B", self.head.x, self.head.y))
        print("----")
        for square in new_body:
            print(square)
        new_body.pop()
        print("NEW BODY")
        for square in new_body:
            print(square)

        return Snake(self.snake_id, self.name, new_body, new_head, len(new_body), self.health-1)

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
