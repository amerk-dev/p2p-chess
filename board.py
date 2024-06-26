import pygame
from pieces import King, Queen, Pawn, Rook, Bishop, Knight

WHITE_PAWN_POS = [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7]]
WHITE_QUEEN_POS = [[7, 3]]
WHITE_KING_POS = [[7, 4]]
WHITE_ROOK_POS = [[7, 0], [7, 7]]
WHITE_BISHOP_POS = [[7, 2], [7, 5]]
WHITE_KNIGHT_POS = [[7, 1], [7, 6]]

BLACK_PAWN_POS = [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]]
BLACK_QUEEN_POS = [[0, 3]]
BLACK_KING_POS = [[0, 4]]
BLACK_ROOK_POS = [[0, 0], [0, 7]]
BLACK_BISHOP_POS = [[0, 2], [0, 5]]
BLACK_KNIGHT_POS = [[0, 1], [0, 6]]

PIECES_DATA = [
    [0, {Queen: BLACK_QUEEN_POS, Pawn: BLACK_PAWN_POS, King: BLACK_KING_POS, Rook: BLACK_ROOK_POS,
         Bishop: BLACK_BISHOP_POS, Knight: BLACK_KNIGHT_POS}],
    [1, {Queen: WHITE_QUEEN_POS, Pawn: WHITE_PAWN_POS, King: WHITE_KING_POS, Rook: WHITE_ROOK_POS,
         Bishop: WHITE_BISHOP_POS, Knight: WHITE_KNIGHT_POS}],
]

SELECTED = "#a85f3b"
TARGET = "#FF0000"
POSSIBLE_MOVE = "#ba7350"
MOVE_PLAYED = "!MOVE_PLAYED"


class Square:
    def __init__(self, piece, x_pos: int, y_pos: int, side_length: int, neutral_color: str, player_color: int):
        self.piece = piece
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.neutral_color = neutral_color
        self.side_length = side_length
        self.player_color = player_color
        self.current_color = neutral_color
        self.selected = False
        self.target = False
        self.possible_move = False
        self.eliminated = False

    def set_dimensions(self, sq_x, sq_y):
        self.sq_x, self.sq_y = sq_x, sq_y

    def is_target(self):
        self.current_color = TARGET

    def is_possible_move(self):
        self.current_color = POSSIBLE_MOVE

    def is_selected(self):
        self.current_color = SELECTED

    def neutralize(self):
        self.current_color = self.neutral_color

    def update(self, x_pos, y_pos, sq_x, sq_y, neutral_color):
        self.x_pos, self.y_pos = x_pos, y_pos
        self.sq_x, self.sq_y = sq_x, sq_y
        self.neutral_color = neutral_color
        self.neutralize()
        if self.piece: self.piece.update_pos(x_pos, y_pos)

    def __str__(self):
        return f"{self.piece} at {self.x_pos}, {self.y_pos}"


class Board:
    # These values are just temporary
    BOARD_SIDE_LENGTH = 600
    PIECE_SIDE_LENGTH = 600 / 8

    def __init__(self, color: int) -> None:
        # Color will make sure that the players color is facing them
        self.color = color
        self.rows = 8
        self.col = 8
        self.is_selected = None
        self.is_helper_on = False
        self.possible_moves = []
        self.possible_targets = []
        self.white_captured = []
        self.black_captured = []

        self.board = [[None for i in range(8)] for j in range(8)]
        self.board_color_scheme = [['' for i in range(8)] for j in range(8)]
        for i in range(len(PIECES_DATA)):
            for piece in PIECES_DATA[i][1]:
                for x, y in PIECES_DATA[i][1][piece]:
                    if piece.__name__ == "Pawn":
                        self.board[x][y] = piece(x, y, PIECES_DATA[i][0], pawn_move=0)
                    else:
                        self.board[x][y] = piece(x, y, PIECES_DATA[i][0])

        color = "#decec5"
        isWhite = True
        for i in range(8):
            for j in range(8):
                if isWhite == 1:
                    color = "#decec5"
                else:
                    color = "#733211"

                self.board_color_scheme[i][j] = color
                piece_color = None
                if self.board[i][j]: piece_color = self.board[i][j].color

                self.board[i][j] = Square(self.board[i][j], i, j, Board.PIECE_SIDE_LENGTH, color, piece_color)
                isWhite = not isWhite
            isWhite = not isWhite
        self.black_king = self.board[0][4]
        self.white_king = self.board[7][4]

    def __str__(self):
        return f"This is {self.color} player"

    def draw(self, screen) -> None:
        for i in range(8):
            for j in range(8):
                if self.color:
                    self.board[i][j].set_dimensions(Board.PIECE_SIDE_LENGTH * j, Board.PIECE_SIDE_LENGTH * i)
                else:
                    self.board[i][j].set_dimensions(Board.PIECE_SIDE_LENGTH * (7 - j),
                                                    Board.PIECE_SIDE_LENGTH * (7 - i))

        for row in self.board:
            for data in row:
                if data.piece and (not data.eliminated):
                    pygame.draw.rect(screen, data.current_color,
                                     pygame.Rect(data.sq_x, data.sq_y, data.side_length, data.side_length))
                    piece_image = pygame.image.load(data.piece.image)
                    piece_image_rect = piece_image.get_rect(topleft=(data.sq_x, data.sq_y))
                    screen.blit(piece_image, piece_image_rect)
                else:
                    pygame.draw.rect(screen, data.current_color,
                                     pygame.Rect(data.sq_x, data.sq_y, data.side_length, data.side_length))

    def select_sqaure(self, x: int, y: int) -> bool:
        adj_x, adj_y = int(x / Board.PIECE_SIDE_LENGTH), int(y / Board.PIECE_SIDE_LENGTH)
        if not self.color: adj_x, adj_y = 7 - adj_x, 7 - adj_y

        if self.is_selected:
            self.is_selected.neutralize()
            self.neutralize_board()
            if (adj_x, adj_y) in self.possible_moves:
                if type(self.is_selected.piece).__name__ == "Pawn":
                    self.is_selected.piece.pawn_move += 1
                if type(self.is_selected.piece).__name__ == "King" or type(self.is_selected.piece).__name__ == "Rook":
                    self.is_selected.piece.moved = True
                self.swap_positions(self.is_selected, self.board[adj_x][adj_y])

                self.is_selected = None
                return MOVE_PLAYED

            if (adj_x, adj_y) in self.possible_targets:
                self.board[adj_x][adj_y].eliminated = True

                if self.board[adj_x][adj_y].piece.color:
                    self.white_captured.append(self.board[adj_x][adj_y].piece)
                else:
                    self.black_captured.append(self.board[adj_x][adj_y].piece)

                if type(self.is_selected.piece).__name__ == "Pawn":
                    self.is_selected.piece.pawn_move += 1
                if type(self.is_selected.piece).__name__ == "King" or type(self.is_selected.piece).__name__ == "Rook":
                    self.is_selected.piece.moved = True
                self.swap_positions(self.is_selected, self.board[adj_x][adj_y], eliminate=True)
                self.is_selected = None

                return MOVE_PLAYED

            if self.is_selected == self.board[adj_x][adj_y]:
                self.is_selected = None
                return True
            self.is_selected = None

        if self.board[adj_x][adj_y].piece and self.board[adj_x][adj_y].player_color == self.color:
            self.board[adj_x][adj_y].is_selected()
            self.is_selected = self.board[adj_x][adj_y]
            self.prospective_plays(self.is_selected)
            return True
        return False

    def prospective_plays(self, square) -> None:
        self.possible_moves, self.possible_targets = square.piece.possible_moves(self.board)
        for x, y in self.possible_moves:
            self.board[x][y].is_possible_move()
        for x, y in self.possible_targets:
            self.board[x][y].is_target()

    def neutralize_board(self) -> None:
        for x, y in self.possible_moves:
            self.board[x][y].neutralize()
        for x, y in self.possible_targets:
            self.board[x][y].neutralize()

    def swap_positions(self, sq1: Square, sq2: Square, eliminate=False):
        x1, y1, sq_x1, sq_y1 = sq1.x_pos, sq1.y_pos, sq1.sq_x, sq1.sq_y
        x2, y2, sq_x2, sq_y2 = sq2.x_pos, sq2.y_pos, sq2.sq_x, sq2.sq_y
        nc1, nc2 = sq1.neutral_color, sq2.neutral_color
        sq2.update(x1, y1, sq_x1, sq_y1, nc1)
        sq1.update(x2, y2, sq_x2, sq_y2, nc2)
        self.board[x1][y1], self.board[x2][y2] = sq2, sq1
        if eliminate:
            self.board[x1][y1].piece.in_game = False
            self.board[x1][y1].piece = None
            self.board[x1][y1].player_color = None

    def pawn_imprisonment(self):
        pass
