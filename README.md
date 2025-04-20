we worked independently but in the same repo

Nick method: [bot.py](https://github.com/SheepTester-forks/STARCHESS/blame/main/data/classes/bots/bot.py) and other files

> hide shut up shut up shut up shut up shut up shut up over here okay so basically what I did was I used very stock fish fairy stock fish furry it's not very like fairy tale fairy as in ferry okay good so what we do is we have the executable as a string inside of the python file and then when we run the program we write the executable file for fairy stockfish wait okay continue please okay write the file for fairy stockfish to the file system then we run it as a subprocess and we also have a variance.ini file that runs well that has the rules for star chest and then star chest so then afterwards it queries the stockfish fairy stockfish runner and gets the next best move that takes 0.93.0 like less than one like like 90 milliseconds right then then after it does that it returns the move so it would have beaten all of your bots except for the fact that they disallowed pee open from sub-processor but so I tried to investigate it by hiding it in the middle of the binary like splitting the string in half and adding import statements in the middle and also making sure that the strings sub-process never went in there and actually did adhere to the rules I didn't import sub-process I am ported cis which allows you to access sub-process through so using

🚫 disqualified, but always beats `python.bot` (below) 😎 

Sean's method: [python/bot.py](https://github.com/SheepTester-forks/STARCHESS/blame/main/data/classes/bots/python/bot.py)

> for every possible move, get the worst possible board score across the opponent's possible subsequent moves. select my move with the best score
>
> what's the score? add points for each of my pieces remaining on the board, subtract points for the opponent's pieces. pieces have different point values; pawns are worth more as they get to the end
>
> also, for good measure, it deletes the opponent's king from the board

🥇 first place with 1 loss??

# Rust shit

```shell
$ maturin develop --release
$ python make.py
```

worked on my machine but not Steven's 😔

turns out my method (`python.bot`) was fast enough in Python anyways

---

# StarChess.AI 2025

Welcome to ACM AI's Spring 2025 competition, StarChess.AI!

## Rule

Our chess rules are slightly different from the classical chess. Please check [`rules.md`](rules.md).

## Setup

To start, clone the repository:

```bash
git clone https://github.com/acmucsd/ai-chessbot.git
```

To setup the virtual environment:

```bash
python -m venv venv
# For MacOS/Linux:
source venv/bin/activate
# On Windows (use command line if powershell gives any issues):
venv\Scripts\activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

You are welcome to look over the repository to get better ideas on how you should implement your bot. We suggest that you start with a simple non-ML bot. We also provide three example bots, which are stored in the `data/classes/bots`.

- Random Bot: The bot chooses random move.
- Single Step Optimized Bot: The bot chooses the best move among the all possible moves at the moment. It does not consider the consequences of later moves.
- Minimax Bot: The bot is implemented with minimax algorithm (check [Resources](#resources)). However, we cannot guarentee the bot will work as expected, as it serves as an example for how your bot can be optimized.

The main function that you will be writing is the `move` function, which takes in a `side` parameter which represents if you're currently playing black or white, and a `board` parameter, which represents the current state of the board. This function should return a ((int, int), (int, int)) tuple, where the first element are the indices of the piece you wish to move, and the second element are the indices of the square you want to move to.

Some functions you may find useful in the `Board.py` file are: -`get_board_state`, which returns the board setup as a 6x6 array. Each element in this array is either empty (which means it is not occupied by a piece), or has a two-character string in the format `{color}{Piece}`. For example `wB` would be white bishop, and `bK` would be black king. -`get_all_valid_moves`, which returns an array containing all legal moves -`handle_move`, which attempts to make a move on the board, returning True if the move is valid and false otherwise

⚠️ Warning: Please do not call API for other chess engines (such as Stockfish) because our chess rule and the implementation is different.

## Submission and Evaluation

You should only submit your [`bot.py`](data/classes/bots/bot.py), which should include class `Bot` with function `move(self, side, board)`.

Your bot will be matched against every other submitted bot in a round robin style tournament, where a win is worth 3 points, a draw is worth 1 point, and a loss is worth no points.

Your bot will have 0.1 seconds to make a move. If your bot exceeds this time, a random move will be made on your bot's behalf. Likewise, if your bot returns an illegal move, a random move will also be made. **If your bot fails to compile, your bot will not be entered into the round robin tournamet, and score 0 points by default.**

## Packages

Please check [`requirements.py`](requirements.txt). Beside built-in modules, the modules on that list are the only 3rd party libraries we allow.

## Resources

Here is some suggested algorithms to try and implement:

1. Minimax Algorithm:
   - [Wikipedia](https://en.wikipedia.org/wiki/Minimax)
   - [Datacamp](https://www.datacamp.com/tutorial/minimax-algorithm-for-ai-in-python)
2. Alpha-beta pruning:
   - [Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
   - [Chess Programming Wiki](https://www.chessprogramming.org/Alpha-Beta)
3. Monte-Carlo Tree Search:
   - [Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
   - [Chess Programming Wiki](https://www.chessprogramming.org/Monte-Carlo_Tree_Search)
   - [Medium Article](https://medium.com/@ishaan.gupta0401/monte-carlo-tree-search-application-on-chess-5573fc0efb75) by Ishaan Gupta
4. Reinforcement Learning Algorithms:
   - [Chess Programming Wiki](https://www.chessprogramming.org/Reinforcement_Learning)
   - [Medium Article](https://medium.com/@samgill1256/reinforcement-learning-in-chess-73d97fad96b3) by @Aditya
   - [Policy Gradients](https://en.wikipedia.org/wiki/Policy_gradient_method)
