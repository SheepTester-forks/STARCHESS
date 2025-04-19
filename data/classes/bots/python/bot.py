import random
import time
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    # module setup might be different on autograder
    from data.classes.Board import Board


class Bot:
    """
    A bot implemented in Python.
    """

    def __init__(self):
        pass

    def move(self, side: Literal["black", "white"], board: "Board"):
        start = time.perf_counter()
        try:
            move = random.choice(board.get_all_valid_moves(side))
            print(move)
            # DELETE THE KING
            for square in board.squares:
                if (
                    square.occupying_piece
                    and square.occupying_piece.notation == "K"
                    and square.occupying_piece.color != side
                ):
                    square.occupying_piece = None
            return move
        finally:
            end = time.perf_counter()
            print(f"Took {end - start:.4f} seconds")
