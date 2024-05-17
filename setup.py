from cx_Freeze import setup, Executable
import sys

# Список дополнительных файлов, которые нужно включить в сборку
include_files = [
    ('./piecess/black_bishop.png', 'piecess/black_bishop.png'),
    ('./piecess/black_king.png', 'piecess/black_king.png'),
    ('./piecess/black_knight.png', 'piecess/black_knight.png'),
    ('./piecess/black_pawn.png', 'piecess/black_pawn.png'),
    ('./piecess/black_queen.png', 'piecess/black_queen.png'),
    ('./piecess/black_rook.png', 'piecess/black_rook.png'),
    ('./piecess/white_bishop.png', 'piecess/white_bishop.png'),
    ('./piecess/white_king.png', 'piecess/white_king.png'),
    ('./piecess/white_knight.png', 'piecess/white_knight.png'),
    ('./piecess/white_pawn.png', 'piecess/white_pawn.png'),
    ('./piecess/white_queen.png', 'piecess/white_queen.png'),
    ('./piecess/white_rook.png', 'piecess/white_rook.png'), #
    ('./chess_pieces/black_bishop.png', 'chess_pieces/black_bishop.png'),
    ('./chess_pieces/black_king.png', 'chess_pieces/black_king.png'),
    ('./chess_pieces/black_knight.png', 'chess_pieces/black_knight.png'),
    ('./chess_pieces/black_pawn.png', 'chess_pieces/black_pawn.png'),
    ('./chess_pieces/black_queen.png', 'chess_pieces/black_queen.png'),
    ('./chess_pieces/black_rook.png', 'chess_pieces/black_rook.png'),
    ('./chess_pieces/white_bishop.png', 'chess_pieces/white_bishop.png'),
    ('./chess_pieces/white_king.png', 'chess_pieces/white_king.png'),
    ('./chess_pieces/white_knight.png', 'chess_pieces/white_knight.png'),
    ('./chess_pieces/white_pawn.png', 'chess_pieces/white_pawn.png'),
    ('./chess_pieces/white_queen.png', 'chess_pieces/white_queen.png'),
    ('./chess_pieces/white_rook.png', 'chess_pieces/white_rook.png'),
    ('board.py', '.'),
    ('board2.py', '.'),
    ('client.py', '.'),
    ('pieces.py', '.'),
    ('player.py', '.')
]

# Определите базу (только для Windows)
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Используйте "Console" для консольных приложений

# Список используемых пакетов
packages = [
    "pygame",
]

# Создайте объект Executable
executables = [Executable("test.py", base=base)]

# Определите параметры настройки
setup(
    name="P2P Chess",
    version="1.0",
    description="Chess Project",
    options={
        "build_exe": {
            "packages": packages,
            "include_files": include_files,
        }
    },
    executables=executables,
)