use pyo3::prelude::*;

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
enum Side {
    White,
    Black,
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
enum Piece {
    Pawn,
    Rook,
    Knight,
    Bishop,
    Queen,
    King,
    Star,
    Joker,
}

type Board = Vec<Vec<Option<(Side, Piece)>>>;

type Position = (usize, usize);

fn decode_board(board: &[Vec<String>]) -> Board {
    board
        .iter()
        .map(|row| {
            row.iter()
                .map(|piece_str| {
                    if piece_str.is_empty() {
                        None
                    } else {
                        let mut chars = piece_str.chars();
                        let side = chars.next().expect("2-char str");
                        let piece = chars.next().expect("2-char str");
                        Some((
                            match side {
                                'w' => Side::White,
                                'b' => Side::Black,
                                _ => panic!("invalid piece {}", piece_str),
                            },
                            match piece {
                                ' ' => Piece::Pawn,
                                'R' => Piece::Rook,
                                'N' => Piece::Knight,
                                'B' => Piece::Bishop,
                                'Q' => Piece::Queen,
                                'K' => Piece::King,
                                'S' => Piece::Star,
                                'J' => Piece::Joker,
                                _ => panic!("invalid piece {}", piece_str),
                            },
                        ))
                    }
                })
                .collect()
        })
        .collect()
}

fn offset_maybe((br, bc): Position, (or, oc): (isize, isize)) -> Option<Position> {
    match (br.checked_add_signed(or), bc.checked_add_signed(oc)) {
        (Some(row), Some(column)) if row < 6 && column < 6 => Some((row, column)),
        _ => None,
    }
}

fn offset(base: Position, offset: (isize, isize)) -> (Position, Position) {
    (base, offset_maybe(base, offset).unwrap_or((7, 7)))
}

fn get_all_moves(side: &Side, board: &Board) -> Vec<(Position, Position)> {
    // Black moves +, white moves - row
    board
        .iter()
        .enumerate()
        .flat_map(|(r, row)| {
            row.iter().enumerate().flat_map(move |(c, cell)| {
                let Some(piece) = cell else {
                    return vec![];
                };
                if piece.0 != *side {
                    return vec![];
                }
                let from = (r, c);
                match piece.1 {
                    Piece::Pawn => vec![],
                    Piece::Rook => vec![],
                    Piece::Knight => vec![
                        offset(from, (-1, -2)),
                        offset(from, (-1, 2)),
                        offset(from, (1, -2)),
                        offset(from, (1, 2)),
                        offset(from, (-2, -1)),
                        offset(from, (-2, 1)),
                        offset(from, (2, -1)),
                        offset(from, (2, 1)),
                    ],
                    Piece::Bishop => vec![],
                    Piece::Queen => vec![],
                    Piece::King => vec![
                        offset(from, (-1, -1)),
                        offset(from, (0, -1)),
                        offset(from, (1, -1)),
                        offset(from, (-1, 0)),
                        offset(from, (1, 0)),
                        offset(from, (-1, 1)),
                        offset(from, (0, 1)),
                        offset(from, (1, 1)),
                    ],
                    Piece::Star => vec![
                        offset(from, (-1, -1)),
                        offset(from, (-1, 1)),
                        offset(from, (1, -1)),
                        offset(from, (1, 1)),
                        offset(from, (0, -2)),
                        offset(from, (0, 2)),
                        offset(from, (-2, 0)),
                        offset(from, (2, 0)),
                    ],
                    Piece::Joker => vec![],
                }
            })
        })
        .filter(|&(start, end): &(Position, Position)| {
            if end.0 == 7 {
                return false;
            }
            let start = board[start.0][start.1];
            let end = board[end.0][end.1];
            match (start, end) {
                // Cannot eat your own piece
                (Some((start_side, _)), Some((end_side, _))) => start_side != end_side,
                _ => true,
            }
        })
        .collect()
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn perform_move(
    side: String,
    board: Vec<Vec<String>>,
) -> PyResult<((usize, usize), (usize, usize))> {
    let side = match side.as_str() {
        "black" => Side::Black,
        "white" => Side::White,
        _ => panic!("Unexpected side {}", side),
    };
    let board = decode_board(&board);
    println!("board: {:?}", board);
    let ((sy, sx), (ey, ex)) = get_all_moves(&side, &board)[0];
    Ok(((sx, sy), (ex, ey)))
}

/// A Python module implemented in Rust.
#[pymodule]
fn ai_chessbot(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(perform_move, m)?)?;
    Ok(())
}
