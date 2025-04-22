import random
from game.board import Board, Ship, Direction

class AIBoard(Board):
    def __init__(self, board_size, ship_sizes):
        super().__init__(board_size, ship_sizes)
        for ship_length in self.ship_sizes:
            ship_added = False
            while not ship_added:
                x = random.randint(0, board_size - 1)
                y = random.randint(0, board_size - 1)
                ship_direction = random.choice(list(Direction))
                ship = Ship(x, y, ship_direction, ship_length)
                if self.is_valid(ship):
                    self.add_ship(ship)
                    ship_added = True