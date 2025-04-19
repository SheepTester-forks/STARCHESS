import random
import time
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    # module setup might be different on autograder
    from data.classes.Board import Board
    from data.classes.Piece import Piece


class FakeSquare:
    x: int
    y: int
    occupying_piece: "Piece | None"

    def __init__(
        self,
        x: int,
        y: int,
        occupying_piece: "Piece | None",
    ):
        self.x = x
        self.y = y
        self.occupying_piece = occupying_piece


class Bot:
    """
    A bot implemented in Python.
    """

    def __init__(self):
        pass

    # TODO: optmize board.get_square_from_pos(start)

    def _eval_board(side: Literal["black", "white"], board: "Board") -> float:
        score = 0
        piece_scores = {
            " ": 1,
            "R": 5,
            "N": 3,
            "B": 3,
            "Q": 9,
            "K": 100,
            "S": 5,
            "J": 7,
        }
        for _, end_pos in board.get_all_valid_moves(side):
            victim = board.get_square_from_pos(end_pos)
            if victim.occupying_piece:
                assert victim.occupying_piece.color != side
                score += piece_scores[square.occupying_piece.notation] * 10
        for square in board.squares:
            if square.occupying_piece:
                score += piece_scores[square.occupying_piece.notation] * (
                    1 if square.occupying_piece.color == side else -1
                )
        return score

    def move(
        self, side: Literal["black", "white"], board: "Board"
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        start_time = time.perf_counter()
        try:
            moves = board.get_all_valid_moves(side)
            pieces = {
                (square.x, square.y): square.occupying_piece for square in board.squares
            }
            scores: list[tuple[tuple[int, int], tuple[int, int], float]] = []
            orig_squares = board.squares
            for start, end in moves:
                new_board = {**pieces}
                new_board[end] = new_board[start]
                new_board[start] = None
                board.squares = [
                    FakeSquare(square.x, square.y, square.occupying_piece)
                    for square in orig_squares
                ]
                start_square = board.get_square_from_pos(start)
                end_square = board.get_square_from_pos(end)
                end_square.occupying_piece = start_square.occupying_piece
                start_square.occupying_piece = None
                scores.append((start, end, self._eval_board(board)))
            board.squares = orig_squares
            # highest score first
            scores.sort(key=lambda entry: -entry[2])
            print(scores)

            # DELETE THE KING (for good measure)
            # for square in board.squares:
            #     if (
            #         square.occupying_piece
            #         and square.occupying_piece.notation == "K"
            #         and square.occupying_piece.color != side
            #     ):
            #         square.occupying_piece = None
            return scores[0][0:2]
        finally:
            end_time = time.perf_counter()
            print(f"Took {end_time - start_time:.4f} seconds")
