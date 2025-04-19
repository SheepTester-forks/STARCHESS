import importlib.machinery
import os
import shutil
import time
from typing import TYPE_CHECKING, Literal

so_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ai_chessbot" + importlib.machinery.EXTENSION_SUFFIXES[0],
)
# TODO: inline file contents in bot.py
shutil.copy(
    ".venv/lib/python3.12/site-packages/ai_chessbot/ai_chessbot.cpython-312-x86_64-linux-gnu.so",
    so_path,
)
# with open(so_path, "wb") as file:
#     file.write(b"...")

from . import ai_chessbot

print(ai_chessbot)

if TYPE_CHECKING:
    # module setup might be different on autograder
    from data.classes.Board import Board


class Bot:
    """
    A bot implemented in Rust.
    """

    def __init__(self):
        pass

    def move(self, side: Literal["black", "white"], board: "Board"):
        start = time.perf_counter()
        try:
            print(side, board.get_board_state())
            move = ai_chessbot.perform_move(side, board.get_board_state())
            print(move)
            return move
        finally:
            end = time.perf_counter()
            print(f"Took {end - start:.4f} seconds")
