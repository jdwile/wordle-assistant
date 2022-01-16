# Description

This is an assistant for the web game
[Wordle](https://www.powerlanguage.co.uk/wordle/). This isn't meant to boost
scores or anything, it's just to see how good I can make automated guessing
through a combination of heuristics.

# Todos

- Position-based weightings (vowels come after consonants, average position in 5
  letter word, etc)
- Weight previous Wordle solutions lower
- Keep list of "unknown words" that Wordle doesn't accept (to filter out
  `nltk`'s list of words)
- Maybe make some sort of UI or something
