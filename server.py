import os
import random

import cherrypy

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
        print_board_position(data)
        return {"color": "#1a75ff", "headType": "smile", "tailType": "fat-rattle"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It"s how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        print("Data regarding a move:")
        possible_moves = get_correct_move(data)
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


def get_correct_move(request_data):
    board_data = request_data["board"]
    print("Board_Data", board_data)

    possible_moves = ['up', 'down', 'left', 'right']

    board = []
    for row in range(0, board_data["height"]):
        board.append([""] * board_data["width"])

    snake_data = request_data["board"]['snakes']
    food_data = request_data["board"]["food"]

    head = {}

    for snake in snake_data:
        head = snake["body"][:1][0]
        head_y = int(head["y"])
        head_x = int(head["x"])
        if(head_y == 0):
            print("Unable to go up")
            if("up" in possible_moves):
                possible_moves.remove("up")
        if(head_y == (board_data["height"] - 1)):
            print("Unable to go down")
            if("down" in possible_moves):
                possible_moves.remove("down")
        if(head_x == 0):
            print("Unable to go left")
            if("left" in possible_moves):
                possible_moves.remove("left")
        if(head_x == (board_data['width'] - 1)):
            print("Unable to go right")
            if("right" in possible_moves):
                possible_moves.remove("right")

        board[head_y][head_x] = "H"
        body = snake["body"][1:]
        for body_square in body:
            body_y = int(body_square["y"])
            body_x = int(body_square["x"])
            if(head_x == body_x):
                if((head_y - body_y) == -1):
                    print("Unable to go down")
                    if("down" in possible_moves):
                        possible_moves.remove("down")
                if((head_y - body_y) == 1):
                    print("Unable to go up")
                    if("up" in possible_moves):
                        possible_moves.remove("up")

            if(head_y == body_y):
                if((head_x - body_x) == 1):
                    print("Unable to go left")
                    if("left" in possible_moves):
                        possible_moves.remove("left")
                if((head_x - body_x) == -1):
                    print("Unable to go right")
                    if("right" in possible_moves):
                        possible_moves.remove("right")

            board[body_y][body_x] = "B"

    closest_food = []
    closest_food = food_data[0]
    for food in food_data:
        food_y = food["y"]
        food_x = food["x"]
        board[food_y][food_x] = "F"

    print("Possible Moves", possible_moves)

    for row in board:
        print(row)

    food_snake_y_delta = int(closest_food["y"]) - int(head["y"])
    food_snake_x_delta = int(closest_food['x']) - int(head["x"])
    print(food_snake_y_delta)
    print(food_snake_x_delta)
    larger_delta = ""
    if(abs(food_snake_x_delta) - abs(food_snake_y_delta) > 0):
        larger_delta = "x"
        if(food_snake_x_delta < 0 and "left" in possible_moves):
            print("The only way to go is left")
            return ["left"]
        elif(food_snake_x_delta > 0 and "right" in possible_moves):
            print("The only way to go is right")
            return ["right"]
    elif(abs(food_snake_x_delta) - abs(food_snake_y_delta) < 0):
        larger_delta = "y"
        if(food_snake_y_delta > 0 and "down" in possible_moves):
            return ["down"]
        elif(food_snake_y_delta < 0 and "up" in possible_moves):
            print("The only way to go is up")
            return ["up"]
    else:
        print("It doesn't really matter what way you go")
        return possible_moves

    return possible_moves


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")), }
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
