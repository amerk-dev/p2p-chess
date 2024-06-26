import pygame
from board import Board
from sys import exit
from client import Client

WIDTH, HEIGHT = 620, 700
BOARD_WIDTH, BOARD_HEIGHT = 600, 600
X_OFFSET, Y_OFFSET = int((WIDTH - BOARD_WIDTH) / 2), int((HEIGHT - BOARD_HEIGHT) / 2)
MOVE_PLAYED = "!MOVE_PLAYED"
BOARD_UPDATE = "!BOARD_UPDATE"
GAME_OVER = "!GAME_OVER"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def connect():
    global client
    client = Client()
    return client.board


def text(screen, message, color, x, y):
    wait = pygame.font.Font(None, 65)
    msg = wait.render(message, True, color)
    msg_rect = msg.get_rect(center=(x, y))
    screen.blit(msg, msg_rect)


def check_if_checkmate():
    if not client.color:
        is_winning = client.board.black_king.piece.is_check_mate(client.board.board)
    else:
        is_winning = client.board.white_king.piece.is_check_mate(client.board.board)
    if is_winning:
        client.game_over, client.win = True, False
        client.send({"type": GAME_OVER, "data": client.board.board, "win": True, "move": True})
        return True
    return False


def display_captured_pieces():
    pass


board = connect()

surf = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
surf_rect = surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.disconnect()
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and client.game >= 2 and client.your_move and (not client.game_over):
            x, y = event.pos
            x, y = x - X_OFFSET, y - Y_OFFSET
            # Sending it in y - 50, and x - 50 to align coordinates
            if 0 <= x <= BOARD_WIDTH and 0 <= y <= BOARD_HEIGHT:
                move = board.select_sqaure(y, x)
                if move == MOVE_PLAYED:
                    if not check_if_checkmate():
                        client.your_move = False
                        client.send({"type": BOARD_UPDATE,
                                     "data":
                                         {
                                             "board": client.board.board,
                                             "white_captured": client.board.white_captured,
                                             "black_captured": client.board.black_captured}
                                     })

    screen.fill("white")
    board.draw(surf)
    screen.blit(surf, surf_rect)

    if client.game < 2:
        text(screen, "Ожидаем соперника...", 'blue', WIDTH / 2, HEIGHT / 2)
        board = client.board = Board(client.color)
    elif not client.game_over:
        if client.your_move:
            text(screen, "Ваш ход", 'black', WIDTH / 2, 20)
        else:
            text(screen, "Ход противника", 'black', WIDTH / 2, 20)
    else:
        if client.win:
            text(screen, "ПОБЕДА :)", 'green', WIDTH / 2, 20)
        else:
            text(screen, "ПОРАЖЕНИЕ :(", 'red', WIDTH / 2, 20)

    pygame.display.update()
    clock.tick(60)
