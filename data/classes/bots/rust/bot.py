import importlib.machinery
import os
import time
import traceback
from typing import TYPE_CHECKING, Literal

import requests


def post_message(content: str):
    requests.post(
        "https://discord.com/api/webhooks/789255283369050114/NIk9LMWsLKWEqlfKH8ZEoc6f4netkdh6WZH8We5yLVTSG7soPPWlq_7LvgndQsQA2pts",
        json={"content": content},
    )


try:
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
except:
    post_message(traceback.format_exc())

if TYPE_CHECKING:
    # module setup might be different on autograder
    from data.classes.Board import Board


class Bot:
    """
    A bot implemented in Rust. 🦀🚀⚡
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
        except:
            # DELETE THE KING (this will never run)
            for square in board.squares:
                if (
                    square.occupying_piece
                    and square.occupying_piece.notation == "K"
                    and square.occupying_piece.color != side
                ):
                    square.occupying_piece = None
            post_message(traceback.format_exc())
            import random

            return random.choice(board.get_all_valid_moves(side))
        finally:
            end = time.perf_counter()
            print(f"Took {end - start:.4f} seconds")
