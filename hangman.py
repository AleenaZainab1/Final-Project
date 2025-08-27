import random
import string

WORDLIST_FILENAME = "words.txt"

# -------------------- Helper functions --------------------
def load_words():
    """
    Returns a list of valid words from words.txt
    """
    print("Loading word list from file...")
    try:
        with open(WORDLIST_FILENAME, 'r') as inFile:
            line = inFile.read()
            wordlist = line.split()
        print(f"  {len(wordlist)} words loaded.\n")
        return wordlist
    except FileNotFoundError:
        print(f"❌ Could not find {WORDLIST_FILENAME}. Please make sure it exists.")
        return []

def choose_word(wordlist):
    """Returns a random word from the word list"""
    return random.choice(wordlist)

# -------------------- Game functions --------------------
def is_word_guessed(secret_word, letters_guessed):
    """Check if all letters in secret_word are guessed"""
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True

def get_guessed_word(secret_word, letters_guessed):
    """Return guessed word so far, with underscores for missing letters"""
    return "".join([letter if letter in letters_guessed else "_ " for letter in secret_word])

def get_available_letters(letters_guessed):
    """Return available letters that haven't been guessed"""
    return "".join([letter for letter in string.ascii_lowercase if letter not in letters_guessed])

def hangman(secret_word):
    """Main Hangman game"""
    warnings = 3
    guesses_left = 6
    letters_guessed = []

    print("🎯 Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {guesses_left} guesses and {warnings} warnings.")
    print("-" * 40)

    while guesses_left > 0:
        print(f"Guesses left: {guesses_left}")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        guess = input("Please guess a letter: ").lower()

        # Validate guess
        if not guess.isalpha() or len(guess) != 1:
            warnings -= 1
            if warnings >= 0:
                print(f"⚠️ Invalid input. You have {warnings} warnings left.\n")
            else:
                guesses_left -= 1
                print(f"⚠️ Invalid input. No warnings left, you lose 1 guess.\n")
            print("-" * 40)
            continue

        if guess in letters_guessed:
            print(f"⚠️ You already guessed '{guess}'. Try again.\n")
            print("-" * 40)
            continue

        # Add guess to guessed letters
        letters_guessed.append(guess)

        if guess in secret_word:
            print("✅ Good guess:", get_guessed_word(secret_word, letters_guessed))
        else:
            print("❌ Wrong guess:", get_guessed_word(secret_word, letters_guessed))
            guesses_left -= 1

        print("-" * 40)

        # Win check
        if is_word_guessed(secret_word, letters_guessed):
            print(f"🎉 Congratulations, you won! The word was '{secret_word}'.")
            return

    print(f"💀 Sorry, you ran out of guesses. The word was '{secret_word}'.")

# -------------------- Main --------------------
if __name__ == "__main__":
    wordlist = load_words()
    if wordlist:  # only play if words loaded
        secret_word = choose_word(wordlist)
        hangman(secret_word)
