import csw19
from assistant import Assistant


class Tester:
    def __init__(self, word) -> None:
        self.set_word(word)

    def set_word(self, word):
        self.word = word

    def guess(self, guess) -> str:
        result = ""
        for i in range(len(guess)):
            if guess[i] == self.word[i]:
                result += "g"
            elif guess[i] in self.word:
                result += "y"
            else:
                result += " "
        return result


words = csw19.get_words()
print(len(words))
num_guesses = 0
assistant = Assistant()
tester = Tester("")

for i in range(len(words)):
    tester.set_word(words[i])

    if i % 100 == 0:
        print(f"{i}: {num_guesses / (i + 1)}")

    for j in range(6):
        guess = assistant.get_guess()
        hint = tester.guess(guess)
        solved = assistant.handle_hints(guess, hint)
        if solved:
            # print(f"solved {words[i]} in {j+1}")
            num_guesses += j + 1
            break

    assistant.reset()

print(f"Average guesses: {num_guesses/len(words)}")
