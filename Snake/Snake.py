from SnakeSquare import SnakeSquare
import copy
# Snake class.


class Snake:
    # Meta data and some data regarding body/head/tail
    def __init__(self, snake_id, name, body, head, tail, length, health):
        self.snake_id = snake_id
        self.name = name
        self.head = head
        self.body = body
        self.tail = tail
        self.length = length
        self.health = health
        self.closest_food = None

    # Check if objects are equal
    def __eq__(self, another_object):
        return self.snake_id == another_object.snake_id

    # Simple to string method can be appended upon
    def __str__(self):
        return f"Snake: {self.name}, with a length of {self.length}"

    # Next_move is where the magic happens in terms of
    # predicting where the snake will be in move N+1
    # Lets say you have a board of 1x5 and a snake
    # of length 3 with T/B/H. It will look like this:
    # ['T','B','H',' ', ' ']
    # What next move does is it moves everything one
    # square in the position you are trying to go
    # [' ', 'N_T', 'N_B', "N_H"]
    def next_move(self, positional_move):
        new_head = None
        # Make new_head of snake
        if(positional_move.move_type == "up"):
            new_head = SnakeSquare(self.head.square_type,
                                   self.head.x, self.head.y-1)
        elif(positional_move.move_type == "down"):
            new_head = SnakeSquare(self.head.square_type,
                                   self.head.x, self.head.y + 1)
        elif(positional_move.move_type == "right"):
            new_head = SnakeSquare(self.head.square_type,
                                   self.head.x+1, self.head.y)
        elif(positional_move.move_type == "left"):
            new_head = SnakeSquare(self.head.square_type,
                                   self.head.x-1, self.head.y)

        # Add old head to new_body, to inch the snake along
        # the vector it is moving
        new_body = copy.deepcopy(self.body)
        new_body.insert(0, SnakeSquare("B", self.head.x, self.head.y))
        # Pop off the new tail.
        new_tail = new_body.pop()
        new_tail.square_type = "T"

        # Create new deep copy of the snake object to avoid PBR
        return Snake(self.snake_id, self.name, new_body, new_head, new_tail, len(new_body), self.health-1)

    def move_towards_food(self, move_set):
        # Move towards food, gets the delta of the closest food and also the possible moves
        # and then based on the possible moves/where the food is, return a
        # possible move or the fact that it doesn't really matter wherever you go.
        closest_food = self.closest_food
        food_snake_y_delta = closest_food.get_y_delta_from_snake(
            self.head)
        food_snake_x_delta = closest_food.get_x_delta_from_snake(self.head)
        # If the food is different then the head of the snake on x vector
        if(abs(food_snake_x_delta) > 0):
            if(food_snake_x_delta < 0):
                move_set.left.set_is_towards_food(True)
            elif(food_snake_x_delta > 0):
                move_set.right.set_is_towards_food(True)
        # If the food is different then the head of the snake on y vector
        elif(abs(food_snake_y_delta) > 0):
            if(food_snake_y_delta > 0):
                move_set.down.set_is_towards_food(True)
            elif(food_snake_y_delta < 0):
                move_set.up.set_is_towards_food(True)
        else:
            return move_set

        return move_set

    def will_snake_hit_enemy(self, move_set, enemy_snake):
        if(not isinstance(enemy_snake, Snake)):
            return move_set

        enemy_snake_full = [enemy_snake.head] + \
            enemy_snake.body + [enemy_snake.tail]
        for snake_square in enemy_snake_full:
            if(snake_square.square_type == "H"):
                if(snake_square.y == self.head.y):
                    if((snake_square.x - self.head.x) == 1):
                        move_set.right.set_is_possible(False)
                    if((snake_square.x - self.head.x) == -1):
                        move_set.left.set_is_possible(False)
                if(snake_square.x == self.head.x):
                    if((snake_square.y - self.head.y) == 1):
                        move_set.down.set_is_possible(False)
                    if((snake_square.y - self.head.y) == -1):
                        move_set.up.set_is_possible(False)

            if(snake_square.square_type == "B"):
                if((snake_square.y == self.head.y)):
                    if((snake_square.x - self.head.x) == 1):
                        move_set.right.set_is_possible(False)
                    if((snake_square.x - self.head.x) == -1):
                        move_set.left.set_is_possible(False)
                if((snake_square.x == self.head.x)):
                    if((snake_square.y - self.head.y) == 1):
                        move_set.down.set_is_possible(False)
                    if((snake_square.y - self.head.y) == -1):
                        move_set.up.set_is_possible(False)

        return move_set

    def will_snake_kill_enemy(self, move_set, enemy_snake):
        head_delta_x = self.head.x - enemy_snake.head.x
        head_delta_y = self.head.y - enemy_snake.head.y
        if((abs(head_delta_x) + abs(head_delta_y)) == 2):
            if(head_delta_x == 2):
                if(enemy_snake.length >= self.length):
                    move_set.left.set_is_safe(False)
                else:
                    move_set.left.set_could_destroy_enemy(True)
            if(head_delta_x == -2):
                if(enemy_snake.length >= self.length):
                    move_set.right.set_is_safe(False)
                else:
                    move_set.right.set_could_destroy_enemy(True)
            if(head_delta_y == 2):
                if(enemy_snake.length >= self.length):
                    move_set.up.set_is_safe(False)
                else:
                    move_set.up.set_could_destroy_enemy(True)
            if(head_delta_y == -2):
                if(enemy_snake.length >= self.length):
                    move_set.down.set_is_safe(False)
                else:
                    move_set.down.set_could_destroy_enemy(True)

            if(head_delta_y == 1 and head_delta_x == 1):
                if(enemy_snake.length >= self.length):
                    move_set.up.set_is_safe(False)
                    move_set.left.set_is_safe(False)
                else:
                    move_set.up.set_could_destroy_enemy(True)
                    move_set.left.set_could_destroy_enemy(True)
            if(head_delta_y == -1 and head_delta_x == 1):
                if(enemy_snake.length >= self.length):
                    move_set.down.set_is_safe(False)
                    move_set.left.set_is_safe(False)
                else:
                    move_set.down.set_could_destroy_enemy(True)
                    move_set.left.set_could_destroy_enemy(True)
            if(head_delta_y == 1 and head_delta_x == -1):
                if(enemy_snake.length >= self.length):
                    move_set.up.set_is_safe(False)
                    move_set.right.set_is_safe(False)
                else:
                    move_set.up.set_could_destroy_enemy(True)
                    move_set.right.set_could_destroy_enemy(True)
            if(head_delta_y == -1 and head_delta_x == -1):
                if(enemy_snake.length >= self.length):
                    move_set.down.set_is_safe(False)
                    move_set.right.set_is_safe(False)
                else:
                    move_set.down.set_could_destroy_enemy(True)
                    move_set.right.set_could_destroy_enemy(True)

        return move_set
