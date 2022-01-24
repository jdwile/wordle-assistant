import re
import csw19

class Assistant:
    def __init__(self, DBG=False) -> None:
        self.green_letters = {}
        self.yellow_letters = {}
        self.gray_letters = set()
        self.global_letter_scores = {}
        self.global_lexical_positions = {}
        self.GLOBAL_BEST_POSSIBLE_WORD_SCORE = 0
        self.BEST_POSSIBLE_WORD_SCORE = 0
        self.letter_scores = {}
        self.lexical_positions = {}
        self.filter_regex_list = ["\w","\w","\w","\w","\w"]
        self.csw19_cache = csw19.get_words()
        self.possible_words = [word.lower() for word in self.csw19_cache if len(word) == 5]
        self.DBG = DBG

    def is_valid(self, guess, should_find_solution):
        try:
            assert len(guess) == 5
            if should_find_solution:
                filter_regex = re.compile(''.join(self.filter_regex_list))
                assert filter_regex.match(guess)
                assert all([l in guess for l in self.yellow_letters.keys()])
            return True
        except (AssertionError):
            return False

    def score_word(self, word, should_find_solution):
        scorable_letters = set(word)
        if not should_find_solution:
            scorable_letters = [l for l in scorable_letters if l not in self.green_letters.keys() and l not in self.yellow_letters.keys()]
        
        global_letter_weighting = sum([self.global_letter_scores[c] for c in scorable_letters]) / self.GLOBAL_BEST_POSSIBLE_WORD_SCORE
        local_letter_weighting = sum([self.letter_scores[c] for c in scorable_letters]) / self.BEST_POSSIBLE_WORD_SCORE
        global_lexical_weighting = sum([2 - abs(self.global_lexical_positions[c] - i) for c, i in zip(word, range(len(word)))]) / (5 * 2)
        local_lexical_weighting = sum([2 - abs(self.lexical_positions[c] - i) for c, i in zip(word, range(len(word)))]) / (5 * 2)
        coverage_score = len(set(word)) / 5
        total_score = sum([global_letter_weighting, local_letter_weighting, global_lexical_weighting, local_lexical_weighting, coverage_score]) / 5
        if (self.DBG):
            print(f"\nScoring {word}")
            print(f"Global Letter Weighting: {global_letter_weighting}")
            print(f"Local Letter Weighting: {local_letter_weighting}")
            print(f"Global Lexical Weighting: {global_lexical_weighting}")
            print(f"Local Lexical Weighting: {local_lexical_weighting}")
            print(f"Coverage Score: {coverage_score}")
            print(f"Total Score: {total_score}")
        return total_score

    def add_to_ignore_filter(self, index, letter):
        if self.filter_regex_list[index] == "\w":
            self.filter_regex_list[index] = f"[^{letter}]"
        elif self.filter_regex_list[index][0] == "[" and letter not in self.filter_regex_list[index]:
            self.filter_regex_list[index] = f"{self.filter_regex_list[index][0:len(self.filter_regex_list[index])-1]}{letter}]"

    def weight_possible_words(self):
        for l in "abcdefghijklmnopqrstuvwxyz":
            self.letter_scores[l] = 0
            self.lexical_positions[l] = 0
        for word in self.possible_words:
            for i in range(len(word)):
                self.letter_scores[word[i]] += 1
                self.lexical_positions[word[i]] += i    
        for l in "abcdefghijklmnopqrstuvwxyz":
            if(self.letter_scores[l] > 0):
                self.lexical_positions[l] = self.lexical_positions[l]/self.letter_scores[l]

    def calculate_best_word_score(self):
        best_score = 0
        for word in self.possible_words:
            best_score = max(best_score, sum([self.letter_scores[c] for c in set(word)]))
        return best_score

    def setup(self):        
            self.possible_words = list(set(self.possible_words))
            self.weight_possible_words()
            if len(self.global_letter_scores) == 0:
                self.global_letter_scores = self.letter_scores.copy()
            if len(self.global_lexical_positions) == 0:
                self.global_lexical_positions = self.lexical_positions.copy()
                if self.DBG:
                    print(self.global_lexical_positions)
            self.BEST_POSSIBLE_WORD_SCORE = self.calculate_best_word_score()
            if self.GLOBAL_BEST_POSSIBLE_WORD_SCORE == 0:
                self.GLOBAL_BEST_POSSIBLE_WORD_SCORE = self.BEST_POSSIBLE_WORD_SCORE

            if self.DBG:
                print(f"\n{len(self.possible_words)} possible words")    
                print(f"Green letters: {self.green_letters}")
                print(f"Yellow letters: {self.yellow_letters}")
                print(f"Gray letters: {self.gray_letters}")
                print(f"Filter regex: /{''.join(self.filter_regex_list)}/")

            self.found_letters = len(self.green_letters.keys()) + len(self.yellow_letters.keys())
            self.should_attempt_solution = self.found_letters >= 3 or len(self.possible_words) < 25

            if self.DBG:
                print(f"Found letters: {self.found_letters}")

            self.possible_words.sort(key=lambda w: self.score_word(w, self.should_attempt_solution), reverse=True)

            if self.DBG and len(self.possible_words) < 25:
                print(f"Possible words: {self.possible_words}")

            # for word in possible_words[0:5]:
            #     score_word(word, should_attempt_solution, True)

    def handle_hints(self, guess, colors):
            if colors == "ggggg":
                if self.DBG: 
                    print("Hooray!")
                return True

            for i in range(len(colors)):
                match colors[i]:
                    case "g":
                        if guess[i] in self.green_letters.keys():
                            self.green_letters[guess[i]].append(i)
                        self.green_letters[guess[i]] = [i]
                    case "y":
                        if guess[i] in self.yellow_letters.keys():
                            self.yellow_letters[guess[i]].append(i)
                        else:
                            self.yellow_letters[guess[i]] = [i]
                    case " ":
                        self.gray_letters.add(guess[i])


            for l, indices in self.green_letters.items():
                for i in indices:
                    self.filter_regex_list[i] = l

            for l, indices in self.yellow_letters.items():
                for i in indices:
                    self.add_to_ignore_filter(i, l)

            for l in self.gray_letters:
                for i in range(len(self.filter_regex_list)):
                    self.add_to_ignore_filter(i, l)

            filter_regex = re.compile(''.join(self.filter_regex_list))
            self.possible_words = list(filter(filter_regex.match, self.possible_words))
            self.possible_words = list(filter(lambda w: all([l in w for l in self.yellow_letters]), self.possible_words))

            return False

    def run_simulation(self):
        for _ in range(6):
            self.setup()

            print(f"Some suggestions... {self.possible_words[0:5]})")
            guess = input("Guess:")

            while not self.is_valid(guess, self.should_attempt_solution):
                guess = input("Invalid guess, try again:")

            colors = input("What colors did we get? (Green = 'g', Yellow = 'y', gray = ' '):")

            solved = self.handle_hints(guess, colors)
            if solved: break
    
    def get_guess(self) -> str:
        self.setup()            
        return self.possible_words[0]

    def reset(self):
        self.green_letters = {}
        self.yellow_letters = {}
        self.gray_letters = set()
        self.BEST_POSSIBLE_WORD_SCORE = 0
        self.letter_scores = {}
        self.lexical_positions = {}
        self.filter_regex_list = ["\w","\w","\w","\w","\w"]
        self.possible_words = [word.lower() for word in self.csw19_cache if len(word) == 5]