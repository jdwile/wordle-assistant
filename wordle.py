from turtle import pos
import re
import csw19

green_letters = {}
yellow_letters = {}
gray_letters = set()
global_letter_scores = {}
global_lexical_positions = {}
GLOBAL_BEST_POSSIBLE_WORD_SCORE = 0
BEST_POSSIBLE_WORD_SCORE = 0
letter_scores = {}
lexical_positions = {}
filter_regex_list = ["\w","\w","\w","\w","\w"]

possible_words = [word.lower() for word in csw19.get_words() if len(word) == 5]

def is_valid(guess, should_find_solution):
    try:
        assert len(guess) == 5
        if should_find_solution:
            filter_regex = re.compile(''.join(filter_regex_list))
            assert filter_regex.match(guess)
            assert all([l in guess for l in yellow_letters.keys()])
        return True
    except (AssertionError):
        return False

def score_word(word, should_find_solution, dbg = False):
    scorable_letters = set(word)
    if not should_find_solution:
        scorable_letters = [l for l in scorable_letters if l not in green_letters.keys() and l not in yellow_letters.keys()]
    
    global_letter_weighting = sum([global_letter_scores[c] for c in scorable_letters]) / GLOBAL_BEST_POSSIBLE_WORD_SCORE
    local_letter_weighting = sum([letter_scores[c] for c in scorable_letters]) / BEST_POSSIBLE_WORD_SCORE
    global_lexical_weighting = sum([2 - abs(global_lexical_positions[c] - i) for c, i in zip(word, range(len(word)))]) / (5 * 2)
    local_lexical_weighting = sum([2 - abs(lexical_positions[c] - i) for c, i in zip(word, range(len(word)))]) / (5 * 2)
    if (dbg):
        print(f"\nScoring {word}")
        print(f"Global Letter Weighting: {global_letter_weighting}")
        print(f"Local Letter Weighting: {local_letter_weighting}")
        print(f"Global Lexical Weighting: {global_lexical_weighting}")
        print(f"Local Lexical Weighting: {local_lexical_weighting}")
        print(f"Total Score: {(global_letter_weighting + local_letter_weighting + global_lexical_weighting + local_lexical_weighting) / 4}")
    return (global_letter_weighting + local_letter_weighting + global_lexical_weighting + local_lexical_weighting) / 4

def add_to_ignore_filter(index, letter):
    if filter_regex_list[index] == "\w":
        filter_regex_list[index] = f"[^{letter}]"
    elif filter_regex_list[index][0] == "[" and letter not in filter_regex_list[index]:
        filter_regex_list[index] = f"{filter_regex_list[index][0:len(filter_regex_list[index])-1]}{letter}]"

def weight_possible_words():
    for l in "abcdefghijklmnopqrstuvwxyz":
        letter_scores[l] = 0
        lexical_positions[l] = 0
    for word in possible_words:
        for i in range(len(word)):
            letter_scores[word[i]] += 1
            lexical_positions[word[i]] += i    
    for l in "abcdefghijklmnopqrstuvwxyz":
        if(letter_scores[l] > 0):
            lexical_positions[l] = lexical_positions[l]/letter_scores[l]

def calculate_best_word_score():
    best_score = 0
    for word in possible_words:
        best_score = max(best_score, sum([letter_scores[c] for c in set(word)]))
    return best_score

for _ in range(6):
    possible_words = list(set(possible_words))
    weight_possible_words()
    if len(global_letter_scores) == 0:
        global_letter_scores = letter_scores.copy()
    if len(global_lexical_positions) == 0:
        global_lexical_positions = lexical_positions.copy()
    BEST_POSSIBLE_WORD_SCORE = calculate_best_word_score()
    if GLOBAL_BEST_POSSIBLE_WORD_SCORE == 0:
        GLOBAL_BEST_POSSIBLE_WORD_SCORE = BEST_POSSIBLE_WORD_SCORE

    print(f"\n{len(possible_words)} possible words")    
    print(f"Green letters: {green_letters}")
    print(f"Yellow letters: {yellow_letters}")
    print(f"Gray letters: {gray_letters}")
    print(f"Filter regex: /{''.join(filter_regex_list)}/")

    found_letters = len(green_letters.keys()) + len(yellow_letters.keys())
    should_attempt_solution = found_letters >= 3 or len(possible_words) < 25

    print(f"Found letters: {found_letters}")

    possible_words.sort(key=lambda w: score_word(w, should_attempt_solution), reverse=True)

    if len(possible_words) < 25:
        print(f"Possible words: {possible_words}")

    # for word in possible_words[0:5]:
    #     score_word(word, should_attempt_solution, True)

    print(f"Some suggestions... {possible_words[0:5]})")
    guess = input("Guess:")

    while not is_valid(guess, should_attempt_solution):
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
        filter_regex_list[i] = l

    for l, indices in yellow_letters.items():
        for i in indices:
            add_to_ignore_filter(i, l)

    for l in gray_letters:
        for i in range(len(filter_regex_list)):
            add_to_ignore_filter(i, l)

    filter_regex = re.compile(''.join(filter_regex_list))
    possible_words = list(filter(filter_regex.match, possible_words))
    possible_words = list(filter(lambda w: all([l in w for l in yellow_letters]), possible_words))
            
