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

/// Formats the sum of two numbers as string.
#[pyfunction]
fn perform_move(
    _side: String,
    board: Vec<Vec<String>>,
) -> PyResult<((usize, usize), (usize, usize))> {
    let board = decode_board(&board);
    println!("board: {:?}", board);
    Ok(((1, 2), (3, 4)))
}

/// A Python module implemented in Rust.
#[pymodule]
fn ai_chessbot(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(perform_move, m)?)?;
    Ok(())
}
