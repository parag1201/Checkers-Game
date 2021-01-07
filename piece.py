import pygame
from assets import WHITE, CROWN, CELL_SIZE

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        if self.color == WHITE:
            self.direction = 1  # move in downward direction in grid
        else:
            self.direction = -1  # move in upward direction in grid

        self.x = 0
        self.y = 0

    # sets the center(x,y) of the pieces(circles)
    def calculate_piece_center(self):
        self.x = CELL_SIZE*self.col + CELL_SIZE//2
        self.y = CELL_SIZE*self.row + CELL_SIZE//2

    # drawing the actual piece in GUI
    def draw_piece(self, win):
        self.calculate_piece_center()
        pygame.draw.circle(win, self.color, (self.x, self.y), (CELL_SIZE//2) - 12)
        if self.king:
            pygame.draw.circle(win, CROWN, (self.x, self.y), (CELL_SIZE//2) - 30)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_piece_center()
