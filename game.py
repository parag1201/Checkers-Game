import pygame
from board import Board
from assets import RED, CELL_SIZE, DARKGREY, WHITE

# pieces turn white - 1, grey - 0

class Game:
    def __init__(self, window):
        self.selected = None
        self.board = Board()
        self.current_player = DARKGREY
        self.valid_moves = {}
        self.win = window

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def winner(self):
        return self.board.winner()

    def reset(self):
        self.selected = None
        self.board = Board()
        self.current_player = DARKGREY
        self.valid_moves = {}

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.current_player:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)

        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]

            # if we walked over some pieces, then delete those pieces
            if skipped:
                self.board.remove_pieces(skipped)
            self.change_player()
        else:
            return False

        return True

    def draw_valid_moves(self, valid_moves):
        for move in valid_moves:
            row, col = move
            x_center = col * CELL_SIZE + CELL_SIZE//2
            y_center = row * CELL_SIZE + CELL_SIZE//2
            pygame.draw.circle(self.win, RED, (x_center, y_center), 5)

    def change_player(self):
        self.valid_moves = {}
        if self.current_player == DARKGREY:
            self.current_player = WHITE
        else:
            self.current_player = DARKGREY
