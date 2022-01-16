from turtle import pos
from nltk.corpus import words
import re

green_letters = {}
yellow_letters = {}
gray_letters = set()
global_letter_scores = {}
letter_scores = {}
filter_regex_list = ["\w","\w","\w","\w","\w"]

possible_words = [word.lower() for word in words.words() if len(word) == 5]

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

def score_word(word, should_find_solution):
    scorable_letters = set(word)
    if not should_find_solution:
        scorable_letters = [l for l in scorable_letters if l not in green_letters.keys() and l not in yellow_letters.keys()]
    return (sum([global_letter_scores[c] for c in scorable_letters]) + sum([letter_scores[c] for c in scorable_letters])) / 2

def add_to_ignore_filter(index, letter):
    if filter_regex_list[index] == "\w":
        filter_regex_list[index] = f"[^{letter}]"
    elif filter_regex_list[index][0] == "[" and letter not in filter_regex_list[index]:
        filter_regex_list[index] = f"{filter_regex_list[index][0:len(filter_regex_list[index])-1]}{letter}]"

def weight_possible_words():
    for l in "abcdefghijklmnopqrstuvwxyz":
        letter_scores[l] = 0
    for word in possible_words:
        for c in word:
            letter_scores[c] += 1
    print(letter_scores)

for _ in range(6):
    weight_possible_words()
    if len(global_letter_scores) == 0:
        global_letter_scores = letter_scores.copy()

    print(f"\n{len(possible_words)} possible words")    
    print(f"Green letters: {green_letters}")
    print(f"Yellow letters: {yellow_letters}")
    print(f"Gray letters: {gray_letters}")
    print(f"Filter regex: /{''.join(filter_regex_list)}/")

    found_letters = len(green_letters.keys()) + len(yellow_letters.keys())

    print(f"Found letters: {found_letters}")

    possible_words.sort(key=lambda w: score_word(w, found_letters >= 3), reverse=True)

    if len(possible_words) < 25:
        print(f"Possible words: {possible_words}")

    print(f"Some suggestions... {possible_words[0:5]})")
    guess = input("Guess:")

    while not is_valid(guess, found_letters >= 3):
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
            
