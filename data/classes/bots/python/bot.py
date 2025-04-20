import math
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

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    def draw(self, _):
        pass


class Bot:
    """
    A bot implemented in Python.
    """

    def __init__(self):
        pass

    def _eval_board(self, side: Literal["black", "white"], board: "Board") -> float:
        score = 0
        piece_scores = {
            " ": 1,
            "R": 5,
            "N": 3,
            "B": 3,
            "Q": 9,
            "K": 100,
            "S": 5,
            "J": 7,  # it's not *as* good as a queen i think
        }
        for _, end_pos in board.get_all_valid_moves(side):
            # victim
            square = board.get_square_from_pos(end_pos)
            if square.occupying_piece:
                assert square.occupying_piece.color != side
                piece_score = piece_scores[square.occupying_piece.notation]
                if square.occupying_piece.notation == " ":
                    # this is KILLING an enemy pawn
                    # for black it starts at y=2 and goes up to y=5 (so from scores 1 to 4)
                    piece_score = square.y - 1 if side == "black" else 5 - square.y
                # points for being able to kill the victim
                score *= 1.5
                score += piece_score * 0.5
        for square in board.squares:
            if square.occupying_piece:
                piece_score = piece_scores[square.occupying_piece.notation]
                if square.occupying_piece.notation == " ":
                    piece_score = square.y - 1 if side == "black" else 5 - square.y
                score += piece_score * (
                    1 if square.occupying_piece.color == side else -1
                )
        return score

    def _set_board_squares(self, board: "Board", squares: list[FakeSquare]):
        board.squares = squares
        board._square_map = {square.pos: square for square in squares}

    def move(
        self, side: Literal["black", "white"], board: "Board"
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        start_time = time.perf_counter()
        try:
            # optimized version
            orig_meth = type(board).get_square_from_pos
            # board.get_square_from_pos = types.MethodType(
            #     (lambda self, pos: self._square_map[pos]), board
            # )
            type(board).get_square_from_pos = lambda self, pos: (
                self._square_map[pos]
                if hasattr(self, "_square_map")
                else orig_meth(self, pos)
            )
            self._set_board_squares(board, board.squares)

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
                self._set_board_squares(
                    board,
                    [
                        FakeSquare(square.x, square.y, square.occupying_piece)
                        for square in orig_squares
                    ],
                )
                start_square = board.get_square_from_pos(start)
                end_square = board.get_square_from_pos(end)
                if end_square.occupying_piece:
                    assert end_square.occupying_piece.color != side
                    if end_square.occupying_piece.notation == "K":
                        # that's GOOD, EAT the king
                        return start, end
                end_square.occupying_piece = start_square.occupying_piece
                start_square.occupying_piece = None
                after_one_turn = board.squares
                worst_poss_score = math.inf
                for opponent_move in board.get_all_valid_moves(
                    "white" if side == "black" else "black"
                ):
                    self._set_board_squares(
                        board,
                        [
                            FakeSquare(square.x, square.y, square.occupying_piece)
                            for square in after_one_turn
                        ],
                    )
                    start_square = board.get_square_from_pos(opponent_move[0])
                    end_square = board.get_square_from_pos(opponent_move[1])
                    if end_square.occupying_piece:
                        assert end_square.occupying_piece.color == side
                        if end_square.occupying_piece.notation == "K":
                            # that's bad, they could insta kill us this way
                            worst_poss_score = -math.inf
                            break
                    end_square.occupying_piece = start_square.occupying_piece
                    start_square.occupying_piece = None
                    score = self._eval_board(side, board)
                    if score < worst_poss_score:
                        worst_poss_score = score
                scores.append((start, end, worst_poss_score))
            self._set_board_squares(board, orig_squares)
            # board.get_square_from_pos = orig_meth
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
