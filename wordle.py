from nltk.corpus import words

green_letters = {}
yellow_letters = {}
gray_letters = set()
letter_scores = {l: 0 for l in "abcdefghijklmnopqrstuvwxyz"}

possible_words = []

def is_valid(guess):
    try:
        assert len(guess) == 5
        assert all([guess[i] == l for l, i in green_letters.items()])
        assert all(
            [
                l in guess and all([not guess[i] == l for i in indices])
                for l, indices in yellow_letters.items()
            ]
        )
        return True
    except (AssertionError):
        return False

def score_word(word):
    return sum([letter_scores[c] for c in set(word)])


for word in words.words():
    if len(word) == 5:
        lower_word = word.lower()
        possible_words.append(lower_word)
        for c in lower_word:
            letter_scores[c] += 1

for _ in range(6):
    print(f"{len(possible_words)} possible words")    
    print(f"Green letters: {green_letters}")
    print(f"Yellow letters: {yellow_letters}")
    print(f"Gray letters: {gray_letters}")

    if len(possible_words) < 25:
        print(possible_words)

    possible_words.sort(key=lambda w: score_word(w), reverse=True)

    print(f"Try picking {possible_words[0]} ({score_word(possible_words[0])})")
    guess = input("Guess:")

    while not is_valid(guess):
        guess = input("Invalid guess, try again:")

    colors = input("What colors did we get? (Green = 'g', Yellow = 'y', gray = ' '):")

    if colors == "ggggg":
        print("Hooray!")
        break

    for i in range(len(colors)):
        match colors[i]:
            case "g":
                green_letters[guess[i]] = i # TODO: multiple identical green letters (e.g. "pills")
            case "y":
                if guess[i] in yellow_letters.keys():
                    yellow_letters[guess[i]].append(i)
                else:
                    yellow_letters[guess[i]] = [i]
            case " ":
                gray_letters.add(guess[i])

    for l, i in green_letters.items():
        possible_words = list(filter(lambda w: w[i] == l, possible_words))
    for l, indices in yellow_letters.items():
        possible_words = list(filter(lambda w: l in w, possible_words))
        for i in indices:
            possible_words = list(filter(lambda w: not w[i] == l, possible_words))
    for l in gray_letters:
        if l in green_letters.keys() or l in yellow_letters.keys(): 
            continue # TODO: gray hints if a letter is in one of the lists
        possible_words = list(filter(lambda w: l not in w, possible_words))
            
