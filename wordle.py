from random import choice
from collections import defaultdict

def dictsum(d1, d2):
    """modifies d1 in place. Adds the values of each key."""
    for k in d2:
        d1[k] += d2[k]

class Wordle:
    """Represents a in progress game with undetermined answer"""
    def __init__(self, g=None):
        """Optional argument g is a Wordle game to clone."""
        if g is not None:
            self.deepcopy(g)
            return
        with open("words", "r") as f:
            self.words = f.read().split('\n')
        self.contains_letters = []
        self.position_letters = ["", "", "", "", ""]
        self.omitted_letters = []
        self.limited_letters = {}
        self.position_exclusions = [ [], [], [], [], [] ]
        self.guesses = {}
        self.frequencies = {}

    def deepcopy(self, wordle):
        """copy all lists without entanglement"""
        self.words = wordle.words[::]
        self.contains_letters = wordle.contains_letters[::]
        self.position_letters = wordle.position_letters[::]
        self.omitted_letters = wordle.omitted_letters[::]
        self.limited_letters = {}
        self.limited_letters.update(wordle.limited_letters)
        self.position_exclusions = []
        for l in wordle.position_exclusions:
            self.position_exclusions.append(l[::])
        self.guesses = {}
        self.guesses.update(wordle.guesses)

    def letterfreq(self, position=None):
        if len(self.words) in self.frequencies:
            if position in self.frequencies[len(self.words)]:
                return self.frequencies[len(self.words)][position]
        else: self.frequencies[len(self.words)] = {}
        letters = defaultdict(int)
        if position is None:
            [dictsum(letters, self.letterfreq(i)) for i in range(5)]
            self.frequencies[len(self.words)][position] = letters
            return letters
        for w in self.words:
            letters[w[position]] += 1
        self.frequencies[len(self.words)][position] = letters
        return letters

    def valid(self, word):
        """returns True or False if a word complies with results evaluated so far"""
        for i, letter in enumerate(word):
            if letter in self.omitted_letters: return False
            if letter in self.position_exclusions[i]: return False
        
        for i, position in enumerate(self.position_letters):
            if position == '': continue
            if word[i] != position: return False
        for letter in self.contains_letters:
            if letter not in word: return False
        for letter in self.limited_letters:
            if word.count(letter) > self.limited_letters[letter]: return False
        return True

    def evaluate(self, w, result):
        """Updates possible words by evaluating a guess and result.
Use these characters:
    X - letter is in the correct position
    x - letter is correct, but in the incorrect position
    _ - letter is incorrect
"""
        self.guesses[w] = result
        for i, inchar in enumerate(result):
            if inchar == 'x':
                self.contains_letters.append(w[i])
                self.position_exclusions[i].append(w[i])
            elif inchar == 'X': self.position_letters[i] = w[i]
            elif inchar == '_':
                if w.count(w[i]) == 1:
                    self.omitted_letters.append(w[i])
                else:
                    self.limited_letters[w[i]] = w.count(w[i])-1
        self.words = [word for word in self.words if self.valid(word)]

    def meta_evaluate(self):
        players = []
        for word in self.words:
            clone = Wordle(self)
            players.append(WordlePlayer(word, clone))
        results = [p.best_guess() for p in players]
        results.sort(key = lambda t: t[1], reverse = True)
        #print(f"Best: {results[0]}\nWorst: {results[-1]}")
        return results[0][0]

    def fast_play(self):
        while len(self.words) > 1:
            if len(self.words) > 500:
                print("Selecting randomly.")
                w = choice(self.words)
            else:
                print("Selecting via metaevaluation.")
                w = self.meta_evaluate()

            intext = input(f"({len(self.words)}) result of trying '{w}': ")
            self.evaluate(w, intext)
        return self.words[0]

    def distrib_score(self, word):
        frequencies = self.letterfreq()
        denominator = sum(frequencies.values())
        score = 0
        for letter in word:
            score += frequencies[letter] / denominator
        return score

    def letterwise_distrib_score(self, word):
        frequencies = [self.letterfreq(i) for i in range(5)]
        score = 0
        for i, letter in enumerate(word):
            denominator = sum(frequencies[i].values())
            score += frequencies[i][letter] / denominator
        return score

    def __repr__(self):
        return f"<Wordle {len(self.guesses)} guesses, {len(self.words)} possibilities>"

class WordlePlayer:
    """Represents a game with definite answer, for evaluating guesses"""
    def __init__(self, answer=None, base=None):
        if base is None:
            self.base_game = Wordle()
        else: self.base_game = base
        if answer is None:
            self.answer = choice(self.base_game.words)
        else: self.answer = answer

    def result(self, w):
        out = ""
        counted_contents = []
        for i, letter in enumerate(w):
            if self.answer[i] == letter:
                out += 'X'
                continue
            elif letter in self.answer:
                if counted_contents.count(letter) < w.count(letter):
                    counted_contents.append(letter)
                    out += 'x'
                    continue
            out += '_'
        return out

    def best_guess(self):
        best = 0
        best_word = None
        for w in self.base_game.words:
            
            if w == self.answer: continue # obviously the best one
            g = Wordle(self.base_game)
            g.evaluate(w, self.result(w))
            reduced = len(g.words)
            reduction = 1 - (reduced / len(self.base_game.words))
            if reduction > best:
                best = reduction
                best_word = w
        return (best_word, best)

    def __repr__(self):
        return f"<WordlePlayer answer={self.answer} game={self.base_game}>"

def play():
    game = Wordle()
    while len(game.words) > 1:
        print(game)
        w = input(f"{len(game.words)} words remain. guess (enter for random): ")
        if w == "":
            w = choice(game.words)
            print(w)
        intxt = ""
        while (len(intxt) != 5):
            intxt = input("X for correct position, x for correct letter, _ for incorrect: ")
        game.evaluate(w, intxt)

if __name__ == '__main__':
    g = Wordle()
    print(g.fast_play())
    
