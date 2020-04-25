from Move import Move
# Moveset class, really simple class that just makes 4 Moves.


class MoveSet:
    def __init__(self):
        self.up = Move("up")
        self.down = Move("down")
        self.left = Move("left")
        self.right = Move("right")

    def __str__(self):
        return f"The Move Set: \n{self.up}\n{self.down}\n{self.left}\n{self.right}"

    def as_array(self):
        return [self.up, self.down, self.left, self.right]

    def as_array_filter(self, array_filter):
        moves_as_array = self.as_array()
        possible_moves_array = []
        if(array_filter == "is_possible"):
            for move in moves_as_array:
                if(move.is_possible):
                    possible_moves_array.append(move)

        return possible_moves_array

    def condensed_output(self):
        return f"""
MOVE TYPE : IS POSSIBLE
{self.up.move_type}:{self.up.is_possible}
{self.down.move_type}:{self.down.is_possible}
{self.left.move_type}:{self.left.is_possible}
{self.right.move_type}:{self.right.is_possible}
"""

    def get_prioritized_moves(self):
        prioritized_sets = []
        move_set_array = self.as_array()
        for move in move_set_array:
            move.set_move_priority()
            x = 0
            inserted_move = False
            while(not inserted_move):
                if(x == len(prioritized_sets)):
                    prioritized_sets.append([move])
                    inserted_move = True
                elif(prioritized_sets[x][0].move_priority == move.move_priority):
                    prioritized_sets[x].append(move)
                    inserted_move = True
                elif(prioritized_sets[x][0].move_priority < move.move_priority):
                    prioritized_sets.insert(x, [move])
                    inserted_move = True
                x = x + 1

        return prioritized_sets

    @staticmethod
    def move_array_to_string_array(move_array):
        string_array = []
        for move in move_array:
            string_array.append(move.move_type)
        return string_array
