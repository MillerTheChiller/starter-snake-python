# Simple class - helps better track the moves across the algorithm
# It has three boleans, food, unsafe and possible.
# Over the algorithm it changes the False to True, and based on that,
# It will prioritize in the end.


class Move:
    def __init__(self, move_type):
        self.move_type = move_type
        self.is_possible = True
        self.is_safe = True
        self.is_towards_food = False
        self.could_destory_enemy = False
        self.move_priority = 0

    def set_is_possible(self, boolean):
        self.is_possible = boolean

    def set_is_safe(self, boolean):
        self.is_safe = boolean

    def set_is_towards_food(self, boolean):
        self.is_towards_food = boolean

    def set_could_destroy_enemy(self, boolean):
        self.could_destory_enemy = boolean

    def set_move_priority(self):
        priority = 0

        if(not self.is_possible):
            priority = priority - 1000
        # If it is not safe and if the movement is towards food chances are the snake is going to
        # be going in that direction as well.
        if(self.is_towards_food and not self.is_safe):
            priority = priority - 15
        if(self.is_towards_food):
            priority = priority + 10
        if(not self.is_safe):
            priority = priority - 15

        if(self.could_destory_enemy):
            priority = priority + 100
        # Reverse and - 100, defs a good chance that if it is not safe the bigger snake will be trying to destroy the enemy.
        if(self.could_destory_enemy and not self.is_safe):
            priority = priority - 200

        self.move_priority = priority

    def __str__(self):
        return f"Moving {self.move_type}, is move possible: {self.is_possible}, is move towards food: {self.is_towards_food}, & is move safe: {self.is_safe}."

    def __eq__(self, other_move):
        if(isinstance(other_move, Move)):
            return self.move_type == other_move.move_type
        elif(isinstance(other_move, str)):
            return self.move_type == other_move
        else:
            return False
