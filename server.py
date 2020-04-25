import os
import random
import copy
import cherrypy
from Board import Board
from Food import Food
from Snake import Snake
from SnakeSquare import SnakeSquare
from MoveSet import MoveSet

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that"s about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json
        return {"color": "#1a75ff", "headType": "safe", "tailType": "round-bum"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It"s how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        possible_moves = find_move(data)
        # Choose a random direction to move in
        move = random.choice(possible_moves)

        print(f"MOVE: {move}")
        return {"move": move, "shout": "it really do be like that sometimes"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It"s purely for informational purposes, you don"t have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"


def find_move(request_data):
    # Possible moves
    move_set = MoveSet()

    # Initiate Board
    # Maybe we put this into the request.session?
    board = Board(request_data["board"]['height'],
                  request_data["board"]["width"])

    # Get food_list, also maybe we can put into the request.session?
    food_list = parse_food_list(request_data["board"]["food"], board)
    # Get My Snake
    my_snake = parse_snake(request_data["you"], board)
    # Snake List, just returns a snake list of 1 which is my snake.
    snake_list = parse_snake_list(
        request_data["board"]['snakes'], request_data["you"], board)

    print(request_data['you'])
    # Removes the snake from request_data["you"] from the snake_list parsed.
    snake_list.remove(my_snake)

    # Get possible moves in the immediate next step
    move_set = get_possible_moves(move_set, board, my_snake)

    move_set = avoid_enemy_snakes(
        move_set, my_snake, snake_list)

    if(my_snake.health > 50):
        my_snake.closest_food = my_snake.tail
    else:
        my_snake = get_closest_food(food_list, my_snake)

    if(my_snake.closest_food != None):
        # Possible move towards food.
        move_set = my_snake.move_towards_food(move_set)
    # Get possible unsafe moves
    move_set = are_moves_unsafe(
        move_set, my_snake, snake_list)
    # Check if that move towards the food is actually going to harm us.
    # Will we be trapped?
    for move in move_set.as_array():
        if(move.is_possible):

            if(len(move_set.as_array_filter("is_possible")) >= 3):
                check_spaces = 3
            else:
                check_spaces = 5
                if(my_snake.length < 5):
                    check_spaces = my_snake.length
            print(check_spaces)
            enough_space = is_there_space(
                move, my_snake, board, check_spaces, snake_list)
            if(not enough_space):
                move.set_is_possible(False)

    # If there are no possible moves just go up idk what to do here.
    # Prioritizing move set
    prioritized_move_set = move_set.get_prioritized_moves()

    moves_as_strings = MoveSet.move_array_to_string_array(
        prioritized_move_set[0])
    print(moves_as_strings)
    return moves_as_strings


def get_closest_food(food_data, snake):
    # gets closest food and then appends it to the snake object
    if(len(food_data) == 0):
        snake.closest_food = None
        return snake
    elif(len(food_data) == 1):
        food_data[0].closest = True
        snake.closest_food = food_data[0]
        return snake
    else:
        closest_food = food_data[0]
        for food in food_data:
            if(food.get_delta_sum(snake.head) < closest_food.get_delta_sum(snake.head)):
                closest_food = food

        snake.closest_food = closest_food

        return snake


def parse_food_list(raw_food_list, board):
    food_list = []
    # get the list of food and parses it into a list of food objects
    for json_food in raw_food_list:
        new_food_object = Food(int(json_food["x"]), int(json_food['y']))
        food_list.append(new_food_object)
        '''
        board.add_to_representation("F", new_food_object.x, new_food_object.y)
        '''
    return food_list


def parse_snake(snake_json, board):
    head = snake_json["body"][:1][0]
    body = snake_json["body"][1:]
    tail = body.pop()
    snake_length = len(snake_json["body"])

    snake = Snake(
        snake_json["id"], snake_json["name"],
        [SnakeSquare("B", square["x"], square["y"])
         for square in body],
        SnakeSquare("H", head["x"], head["y"]),
        SnakeSquare("T", tail["x"], tail["y"]),
        snake_length, snake_json["health"])

    # This is for logging
    '''
    board.add_to_representation(
        snake.head.square_type, snake.head.x, snake.head.y)
    for body_square in snake.body:
        board.add_to_representation(
            body_square.square_type, body_square.x, body_square.y)
    board.add_to_representation(
        snake.tail.square_type, snake.tail.x, snake.tail.y)
    '''
    return snake


def parse_snake_list(raw_snake_list, my_snake, board):
    # Parsing the snake list, currently I just make a
    # list with my snake in it and then return my Snake object

    snake_list = []
    for snake_json in raw_snake_list:
        snake = parse_snake(snake_json, board)

        # Append to the snake object list
        snake_list.append(snake)

    return snake_list


def get_possible_moves(possible_moves, board, my_snake):
    # Possible moves completely based on herustics of
    # Will it hit something
    if(my_snake.head.y == 0):
        possible_moves.up.set_is_possible(False)
    if(my_snake.head.y == (board.height - 1)):
        possible_moves.down.set_is_possible(False)
    if(my_snake.head.x == 0):
        possible_moves.left.set_is_possible(False)
    if(my_snake.head.x == (board.width - 1)):
        possible_moves.right.set_is_possible(False)

    for body_square in my_snake.body:
        if(my_snake.head.x == body_square.x):
            if((my_snake.head.y - body_square.y) == -1):
                possible_moves.down.set_is_possible(False)
            if((my_snake.head.y - body_square.y) == 1):
                possible_moves.up.set_is_possible(False)

        if(my_snake.head.y == body_square.y):
            if((my_snake.head.x - body_square.x) == 1):
                possible_moves.left.set_is_possible(False)
            if((my_snake.head.x - body_square.x) == -1):
                possible_moves.right.set_is_possible(False)

    return possible_moves


def avoid_enemy_snakes(move_set, my_snake, enemy_snakes):
    for enemy_snake in enemy_snakes:
        move_set = my_snake.will_snake_hit_enemy(move_set, enemy_snake)

    return move_set


def are_moves_unsafe(
        move_set, my_snake, snake_list):

    for enemy_snake in snake_list:
        move_set = my_snake.will_snake_kill_enemy(
            move_set, enemy_snake)

    return move_set


def is_there_space(move, snake, board, space_needed, snake_list):
    # Checking if there is space based on length of snake
    if(space_needed == 0):
        return True
    if(not move.is_possible):
        return False
    else:
        # instantiate new move set.
        move_set = MoveSet()
        # Creating a new snake
        new_snake = snake.next_move(move)
        # Creating a new board and updating
        '''
        board_next_turn = copy.deepcopy(board)

        # For logging purposes
        board_next_turn.add_to_representation(
            new_snake.tail.square_type, new_snake.tail.x, new_snake.tail.y)

        board_next_turn.add_to_representation(
            new_snake.head.square_type, new_snake.head.x, new_snake.head.y)

        for body_square in new_snake.body:
            board_next_turn.add_to_representation(
                body_square.square_type, body_square.x, body_square.y)
        # When a food is eaten the last piece of the snake is appended by one
        # but is an exact x/y replica of the latest element in the list.
        if(not snake.tail == new_snake.tail and not snake.tail == new_snake.head):
            board_next_turn.add_to_representation(
                " ", snake.tail.x, snake.tail.y)
        '''
        # Checking if moves are possible
        move_set = get_possible_moves(
            move_set, board, new_snake)
        move_set = avoid_enemy_snakes(
            move_set, new_snake, snake_list)

        possible_moves_as_array = move_set.as_array_filter("is_possible")

        if(len(possible_moves_as_array) > 0):
            up = is_there_space(
                move_set.up, new_snake, board, space_needed-1, snake_list
            )
            down = is_there_space(
                move_set.down, new_snake, board, space_needed-1, snake_list
            )
            right = is_there_space(
                move_set.right, new_snake, board, space_needed-1, snake_list
            )
            left = is_there_space(
                move_set.left, new_snake, board, space_needed-1, snake_list
            )
            return up or down or right or left
        else:
            return False


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")), }
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
