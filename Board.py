class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.twoDimensionalRepresentation = self.create_initial_representation(
            height, width)

    def __str__(self):
        return f"Board Height: {self.height} squares \nBoard Width: {self.width} squares\nA 2D Representation: \n{self.clean_representation_output()}"

    def create_initial_representation(self, height, width):
        board = []
        for x in range(0, self.height):
            board.append([" "] * self.width)

        return board

    def clean_representation_output(self):
        string = ""
        for row in self.twoDimensionalRepresentation:
            string += f"{row}\n"
        return string

    def add_to_representation(self, object_symbol, x_position, y_position):
        self.twoDimensionalRepresentation[y_position][x_position] = object_symbol
