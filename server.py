import os
import random
import copy
import cherrypy
from Board import Board
from Food import Food
from Snake import Snake
from SnakeSquare import SnakeSquare

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
        return {"color": "#1a75ff", "headType": "smile", "tailType": "fat-rattle"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It"s how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        print("REQUEST_DATA", data)
        print("____________")
        print("Data regarding a move:")
        possible_moves = find_move(data)
        print("_______________")
        # Choose a random direction to move in
        move = random.choice(possible_moves)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It"s purely for informational purposes, you don"t have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"


def find_move(request_data):
    possible_moves = ['up', 'down', 'left', 'right']
    board = Board(request_data["board"]['height'],
                  request_data["board"]["width"])

    food_list = parse_food_list(request_data["board"]["food"], board)
    snake_list = parse_snake_list(
        request_data["board"]['snakes'], request_data["you"], board)
    my_snake = snake_list[0]

    possible_moves = get_possible_moves(possible_moves, board, my_snake)
    print(possible_moves)
    my_snake = get_closest_food(food_list, my_snake)
    print(board)
    food_moves = my_snake.move_towards_food(possible_moves)

    for move in food_moves:
        is_possible = is_there_space(move, board, my_snake, my_snake.length)

        print("Was there enough space?", is_possible)
        if(is_possible):
            print("It was possible!")
            possible_moves = food_moves
        else:
            print("It was not possible!!")
            if move in possible_moves:
                possible_moves.remove(move)

    print("possible_moves", possible_moves)
    if(len(possible_moves) == 0):
        return ["up"]
    return possible_moves


def get_closest_food(food_data, snake):
    if(len(food_data) == 1):
        food_data[0].closest = True
        snake.closest_food = food_data[0]
        return snake
    closest_food = food_data[0]
    for food in food_data:
        if(food.get_delta_sum(snake.head) < closest_food.get_delta_sum(snake.head)):
            closest_food = food

    snake.closest_food = closest_food

    return snake


def parse_food_list(raw_food_list, board):
    food_list = []
    for json_food in raw_food_list:
        new_food_object = Food(int(json_food["x"]), int(json_food['y']))
        food_list.append(new_food_object)
        board.add_to_representation("F", new_food_object.x, new_food_object.y)
    return food_list


def parse_snake_list(raw_snake_list, my_snake, board):
    snake_list = []
    raw_snake_list = [my_snake]
    for snake_json in raw_snake_list:
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

        board.add_to_representation(
            snake.head.square_type, snake.head.x, snake.head.y)
        for body_square in snake.body:
            board.add_to_representation(
                body_square.square_type, body_square.x, body_square.y)
        board.add_to_representation(
            snake.tail.square_type, snake.tail.x, snake.tail.y)

        snake_list.append(snake)

    return snake_list


def get_possible_moves(possible_moves, board, my_snake):
    if(my_snake.head.y == 0):
        print("Unable to go up")
        if("up" in possible_moves):
            possible_moves.remove("up")
    if(my_snake.head.y == (board.height - 1)):
        print("Unable to go down")
        if("down" in possible_moves):
            possible_moves.remove("down")
    if(my_snake.head.x == 0):
        print("Unable to go left")
        if("left" in possible_moves):
            possible_moves.remove("left")
    if(my_snake.head.x == (board.width - 1)):
        print("Unable to go right")
        if("right" in possible_moves):
            possible_moves.remove("right")

    for body_square in my_snake.body:
        if(my_snake.head.x == body_square.x):
            if((my_snake.head.y - body_square.y) == -1):
                print("Unable to go down")
                if("down" in possible_moves):
                    possible_moves.remove("down")
            if((my_snake.head.y - body_square.y) == 1):
                print("Unable to go up")
                if("up" in possible_moves):
                    possible_moves.remove("up")

        if(my_snake.head.y == body_square.y):
            if((my_snake.head.x - body_square.x) == 1):
                print("Unable to go left")
                if("left" in possible_moves):
                    possible_moves.remove("left")
            if((my_snake.head.x - body_square.x) == -1):
                print("Unable to go right")
                if("right" in possible_moves):
                    possible_moves.remove("right")

    return possible_moves


def is_there_space(move, board, snake, space_needed):
    if(space_needed == 0):
        return True
    else:
        possible_moves = ["up", "down", "left", "right"]
        # Creating a new space
        new_snake = snake.next_move(move)
        # Creating a new board and updating
        board_next_turn = copy.deepcopy(board)

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

        # Checking if moves are possible

        possible_moves_next_turn = get_possible_moves(
            possible_moves, board_next_turn, new_snake)

        if(len(possible_moves_next_turn) > 0):
            for new_move in possible_moves_next_turn:
                return is_there_space(new_move, board_next_turn,
                                      new_snake, space_needed-1)
        else:
            print("Returning False!")
            return False


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")), }
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
