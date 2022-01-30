# wordle-solver

Get the words list from https://github.com/tabatkins/wordle-list .

## How to use it:

To solve puzzles automatically, run the script with the `words` file present.

The script will present a word, which you should type in. Type in the result you receive, with 'X' indicating position match or green square, 'x' for letter match or yellow square, and '\_' for a non-match.

```
Selecting randomly.
(12972) result of trying 'saddo': _x___
Selecting randomly.
(1360) result of trying 'enema': ____x
Selecting randomly.
(617) result of trying 'bigae': __xx_
Selecting via metaevaluation.
(12) result of trying 'grapy': XXX_X
gravy
```

That last word out indicates there is exactly one word left, and must be the answer.

## How does it work?

Currently, the script starts by guessing. The 12,972 word list is too large to immediately scan for best guesses.

Once the number of possible words has been reduced by about a factor of 25, we an start hypothesizing every possible answer and seeing which guesses will eliminate the most possibilities. the script selects the word that will shrink the possibility list by the largest fraction.

## What's next?

The script sometimes needs all 6 guesses, but seems reliable.

I suspect Wordle chooses common English words more frequently than the gibberish-adjacent words from the dustiest part of a Scrabble dictionary. I may include a word frequency library in the future to prefer guesses that have a better chance of being the solve instead of indefinitely eliminating possibilities.
