from typing import TYPE_CHECKING, Literal
import ai_chessbot

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
        print(side, board.get_board_state())
        return ai_chessbot.perform_move(side, board.get_board_state())
