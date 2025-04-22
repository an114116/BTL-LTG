import pygame

class Display:
    colours = {
        "water": pygame.color.Color("blue"),
        "ship": pygame.color.Color("gray"),
        "hit": pygame.color.Color("red"),
        "miss": pygame.color.Color("lightcyan"),
        "background": pygame.color.Color("navy"),
        "text": pygame.color.Color("white")
    }

    def __init__(self, board_size=10, cell_size=30, margin=15):
        self.board_size = board_size
        self.cell_size = cell_size
        self.margin = margin
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Helvetica", 14)
        width = cell_size * board_size + 2 * margin
        height = 2 * cell_size * board_size + 3 * margin
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption("Battle Ship: Shadow Waters")

    def show(self, upper_board, lower_board, include_top_ships=False):
        if upper_board:
            upper_colours = upper_board.colour_grid(self.colours, include_top_ships)
        if lower_board:
            lower_colours = lower_board.colour_grid(self.colours)

        self.screen.fill(self.colours["background"])
        for y in range(self.board_size):
            for x in range(self.board_size):
                if upper_board:
                    pygame.draw.rect(self.screen, upper_colours[y][x],
                                     [self.margin + x * self.cell_size,
                                      self.margin + y * self.cell_size,
                                      self.cell_size, self.cell_size])

                if lower_board:
                    offset = self.margin * 2 + self.board_size * self.cell_size
                    pygame.draw.rect(self.screen, lower_colours[y][x],
                                     [self.margin + x * self.cell_size,
                                      offset + y * self.cell_size,
                                      self.cell_size, self.cell_size])

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y = y % (self.board_size * self.cell_size + self.margin)
                x = (x - self.margin) // self.cell_size
                y = (y - self.margin) // self.cell_size
                if 0 <= x < self.board_size and 0 <= y < self.board_size:
                    return x, y
        return None, None

    def show_text(self, text, upper=False, lower=False):
        label = self.font.render(text, True, self.colours["text"])
        if upper:
            self.screen.blit(label, (self.margin, self.margin))
        if lower:
            y = self.board_size * self.cell_size + self.margin
            self.screen.blit(label, (self.margin, y))

    def flip(self):
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def close(self):
        pygame.display.quit()
        pygame.quit()
