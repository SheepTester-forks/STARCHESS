import os
import shutil
import sys
import time
from typing import TYPE_CHECKING, Literal

# TODO: inline file contents in bot.py
shutil.copy(
    ".venv/lib/python3.12/site-packages/ai_chessbot/ai_chessbot.cpython-312-x86_64-linux-gnu.so",
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"ai_chessbot.cpython-{''.join(sys.version.split('.')[:2])}-x86_64-linux-gnu.so",
    ),
)

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
            return ai_chessbot.perform_move(side, board.get_board_state())
        finally:
            end = time.perf_counter()
            print(f"Took {end - start:.4f} seconds")
