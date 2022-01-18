def get_words():
    with open("csw19.txt") as f:
        return f.read().rstrip("\n").split("\n")
