import pygame

from piece import Piece
from assets import DARKGREY, GREY, BLACK, WHITE, ROWS, COLS, CELL_SIZE


class Board:
    def __init__(self):
        self.board = []
        self.count_grey_keys = 12
        self.count_white_keys = 12
        self.grey_kings = 0
        self.white_kings = 0
        self.create_board()  # initialises board with pieces objects in the form of 2D list

    # move a certain piece to a particular position
    def move(self, piece, row, col):
        temp = self.board[piece.row][piece.col]
        self.board[piece.row][piece.col] = self.board[row][col]
        self.board[row][col] = temp

        piece.row = row
        piece.col = col

        piece.calculate_piece_center()
        # if reaches end of grid , make it king
        if row + 1 == ROWS or row == 0:
            piece.king = True
            if piece.color == DARKGREY:
                self.grey_kings += 1
            else:
                self.white_kings += 1

    # returns piece object from board
    def get_piece(self, row, col):
        return self.board[row][col]

    #
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 != (row + 1) % 2:
                    self.board[row].append(0)
                else:
                    if row <= 2:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row >= 5:
                        self.board[row].append(Piece(row, col, DARKGREY))
                    else:
                        self.board[row].append(0)

    # draws pieces
    def draw(self, win):
        # draws the empty grid
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, GREY, (row * CELL_SIZE, col * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # draws pieces as circles
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(win)

    # remove pieces which have been walked over by another piece
    def remove_pieces(self, pieces):
        for piece in pieces:
            if piece.color == DARKGREY:
                self.count_grey_keys -= 1
            else:
                self.count_white_keys -= 1
            self.board[piece.row][piece.col] = 0

    def winner(self):
        if self.count_grey_keys <= 0:
            return WHITE
        elif self.count_white_keys <= 0:
            return DARKGREY
        return None

    def get_valid_moves(self, piece):
        moves = {}
        current_col = piece.col
        current_row = piece.row

        if piece.color == DARKGREY or piece.king:
            moves.update(self.travel_left(current_row - 1, max(current_row - 3, -1), -1, piece.color, current_col - 1))
            moves.update(self.travel_right(current_row - 1, max(current_row - 3, -1), -1, piece.color, current_col + 1))
        if piece.color == WHITE or piece.king:
            moves.update(self.travel_left(current_row + 1, min(current_row + 3, 8), 1, piece.color, current_col - 1))
            moves.update(self.travel_right(current_row + 1, min(current_row + 3, 8), 1, piece.color, current_col + 1))

        return moves

    #
    def travel_left(self, start_row, end_row, step, color: object, left, skipped=None):
        moves = {}
        last = []
        for r in range(start_row, end_row, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self.travel_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self.travel_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def travel_right(self, start_row, end_row, step, color, right, skipped=None):
        if skipped is None:
            skipped = []
        moves = {}
        last = []
        for r in range(start_row, end_row, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self.travel_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self.travel_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
