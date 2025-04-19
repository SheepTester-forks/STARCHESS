import subprocess

def board_to_fen(board):
    rows = board.get_board_state()
    fen_ranks = []
    for rank in rows:
        empties = 0
        fen_rank = ""
        for sq in rank:
            if sq == "":
                empties += 1
            else:
                if empties > 0:
                    fen_rank += str(empties)
                    empties = 0
                color = sq[0]
                piece = sq[1] if len(sq) > 1 and sq[1] != " " else "P"  # default to pawn
                if color == "w":
                    fen_rank += piece.upper()
                else:
                    fen_rank += piece.lower()
        if empties > 0:
            fen_rank += str(empties)
        fen_ranks.append(fen_rank)
    side = "w" if board.turn == "white" else "b"
    return "/".join(fen_ranks) + f" {side} - - 0 1"

class Bot:
    """
    A bot that asks Fairy-Stockfish for the best move in our 6x6 Star & Joker variant.
    """
    def __init__(self, engine_path="stockfish"):
        print("no")
        # start the engine process with pipes for UCI
        self.engine = subprocess.Popen(
            [engine_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        print("help")
        self._init_engine()

    def _init_engine(self):
        # enter UCI mode and configure our variant
        self._send("uci")
        # where variants.ini lives; if it's in cwd, "." works
        self._send("setoption name VariantPath value ./variants.ini")
        self._send("setoption name UCI_Variant value my6x6variant")
        self._send("ucinewgame")

    def _send(self, cmd):
        self.engine.stdin.write(cmd + "\n")
        self.engine.stdin.flush()

    def get_possible_moves(self, side, board):
        # you can still expose pyffish’s legal-move list if needed
        return board.get_all_valid_moves(side)

    def move(self, side, board):
        # build FEN of the current position
        fen = board_to_fen(board)
        # tell engine the position
        self._send(f"position fen {fen}")
        # ask it to search to depth 10 (tune as you like)
        self._send("go depth 10")
        # read until bestmove appears
        while True:
            text = self.engine.stdout.readline().strip()
            if text.startswith("bestmove"):
                parts = text.split()
                uci_move = parts[1]      # e.g. "b1c3" or "e2e8j" for promotion
                # return as a tuple of ((from_x, from_y), (to_x, to_y))
                return ((ord(uci_move[0]) - ord('a'),
                        6- int(uci_move[1])),
                        (ord(uci_move[2]) - ord('a'),
                        6- int(uci_move[3])))
