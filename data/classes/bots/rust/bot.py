import importlib.machinery
import os
import time
from typing import TYPE_CHECKING, Literal

current_dir = os.path.dirname(os.path.abspath(__file__))
so_path = os.path.join(
    current_dir,
    "ai_chessbot" + importlib.machinery.EXTENSION_SUFFIXES[0],
)
contents = b"..."
if len(contents) > 10:
    import sys

    with open(so_path, "wb") as file:
        file.write(contents)

    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

import ai_chessbot

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
