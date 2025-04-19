with open(
    ".venv/lib/python3.12/site-packages/ai_chessbot/ai_chessbot.cpython-312-x86_64-linux-gnu.so",
    "rb",
) as so_file, open(
    "data/classes/bots/rust/bot.py",
) as src_file, open(
    "target/bot.py", "w"
) as out_file:
    out_file.write(src_file.read().replace('b"..."', repr(so_file.read())))
