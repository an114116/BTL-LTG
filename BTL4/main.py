from game.player import PlayerBoard
from game.ai_player import AIBoard
from ui.display import Display
from config import BOARD_SIZE, SHIP_SIZES

import random
import pygame

def player_turn(display, ai_board):
    while True:
        x, y = display.get_input()
        if x is None or y is None:
            continue
        if ai_board.valid_target(x, y):
            ai_board.shoot(x, y)
            return

def ai_turn(player_board):
    while True:
        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE - 1)
        if player_board.valid_target(x, y):
            player_board.shoot(x, y)
            return

def main():
    display = Display()

    player_board = PlayerBoard(display, BOARD_SIZE, SHIP_SIZES)
    ai_board = AIBoard(BOARD_SIZE, SHIP_SIZES)

    while True:
        display.show(ai_board, player_board)
        display.show_text("Click to shoot at AI", upper=True)
        display.flip()

        player_turn(display, ai_board)
        if ai_board.gameover:
            print("You win!")
            break

        ai_turn(player_board)
        if player_board.gameover:
            print("You lose!")
            break

    display.show(ai_board, player_board, include_top_ships=True)
    display.show_text("Game over. Close window to exit.", upper=True)
    display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    display.close()

if __name__ == "__main__":
    main()