from cx_Freeze import setup, Executable
import sys
import os

# Получение пути к библиотекам Tcl/Tk
tcl_library = os.path.join(sys.base_prefix, 'tcl', 'tcl8.6')
tk_library = os.path.join(sys.base_prefix, 'tcl', 'tk8.6')
python_dlls_path = os.path.join(sys.base_prefix, 'DLLs')

# Установка переменных окружения для Tcl/Tk
os.environ['TCL_LIBRARY'] = tcl_library
os.environ['TK_LIBRARY'] = tk_library

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
    ('./piecess/white_rook.png', 'piecess/white_rook.png'),
    ('./chess_pieces/black_bishop.svg', 'chess_pieces/black_bishop.svg'),
    ('./chess_pieces/black_king.svg', 'chess_pieces/black_king.svg'),
    ('./chess_pieces/black_knight.svg', 'chess_pieces/black_knight.svg'),
    ('./chess_pieces/black_pawn.svg', 'chess_pieces/black_pawn.svg'),
    ('./chess_pieces/black_queen.svg', 'chess_pieces/black_queen.svg'),
    ('./chess_pieces/black_rook.svg', 'chess_pieces/black_rook.svg'),
    ('./chess_pieces/white_bishop.svg', 'chess_pieces/white_bishop.svg'),
    ('./chess_pieces/white_king.svg', 'chess_pieces/white_king.svg'),
    ('./chess_pieces/white_knight.svg', 'chess_pieces/white_knight.svg'),
    ('./chess_pieces/white_pawn.svg', 'chess_pieces/white_pawn.svg'),
    ('./chess_pieces/white_queen.svg', 'chess_pieces/white_queen.svg'),
    ('./chess_pieces/white_rook.svg', 'chess_pieces/white_rook.svg'),
    ('board.py', '.'),
    ('board2.py', '.'),
    ('client.py', '.'),
    ('pieces.py', '.'),
    ('player.py', '.'),
    (os.path.join(python_dlls_path, 'tk86t.dll'), 'tk86t.dll'),
    (os.path.join(python_dlls_path, 'tcl86t.dll'), 'tcl86t.dll'),
    (tcl_library, 'lib/tcl8.6'),
    (tk_library, 'lib/tk8.6')
]

# Определите базу (только для Windows)
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Используйте "Console" для консольных приложений

# Список используемых пакетов
packages = [
    "pygame",
    "tkinter",
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
