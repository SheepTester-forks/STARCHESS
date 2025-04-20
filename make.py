with open("C:\\Users\\Infernis\\Scripts\\notfish.exe","rb") as so_file, open("C:\\Users\\Infernis\\Desktop\\STARCHESS\\data\\classes\\bots\\mybot.py") as src_file, open("target/mybot.py", "w") as out_file:
    out_file.write(src_file.read().replace('b"..."', repr(so_file.read())))
