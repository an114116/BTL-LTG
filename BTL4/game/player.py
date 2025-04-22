from game.board import Board, Ship, Direction
from itertools import zip_longest
import pygame

class PlayerBoard(Board):
    def __init__(self, display, board_size, ship_sizes):
        super().__init__(board_size, ship_sizes)
        self.display = display
        direction = Direction.NORTH

        while True:
            self.display.show(None, self)
            if self.ship_to_place:
                text = f"Click to place a {self.ship_to_place}-long ship"
            else:
                text = "Click to rotate a ship or click elsewhere if done."

            self.display.show_text(text, lower=True)
            x, y = self.display.get_input()

            if x is not None and y is not None:
                ship = self.get_ship(x, y)
                if ship:
                    self.remove_ship(ship)
                    ship.rotate()
                    if self.is_valid(ship):
                        self.add_ship(ship)
                elif self.ship_to_place:
                    ship = Ship(x, y, direction, self.ship_to_place)
                    if self.is_valid(ship):
                        self.add_ship(ship)
                    else:
                        direction = direction.next
                else:
                    break

            self.display.flip()

    @property
    def ship_to_place(self):
        placed_sizes = sorted(ship.length for ship in self.ships_list)
        sizes = sorted(self.ship_sizes)
        for placed, to_place in zip_longest(placed_sizes, sizes):
            if placed != to_place:
                return to_place
        return None