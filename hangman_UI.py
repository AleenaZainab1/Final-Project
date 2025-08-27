import tkinter as tk
import random
import string

# Constants
WORDLIST_FILENAME = "words.txt"
GUESSES_START = 6

# Load words from file
def load_words():
    try:
        with open(WORDLIST_FILENAME, 'r') as file:
            words = file.read().split()
        return words if words else ["python", "hangman", "game", "computer", "programming"]
    except FileNotFoundError:
        return ["python", "hangman", "game", "computer", "programming"]

# Choose a random word
def choose_word(wordlist):
    return random.choice(wordlist)

# Game functions
def update_display():
    display_word = " ".join([letter if letter in letters_guessed else "_" for letter in secret_word])
    word_label.config(text=display_word)
    guesses_label.config(text=f"Guesses left: {guesses_left}")
    available_label.config(text=f"Available letters: {get_available_letters(letters_guessed)}")

def guess_letter(letter):
    global guesses_left
    if letter not in letters_guessed:
        letters_guessed.append(letter)
        letter_buttons[letter].config(state=tk.DISABLED)  # Disable button after click
        if letter not in secret_word:
            guesses_left -= 1
    update_display()
    check_game_over()

def check_game_over():
    if all(letter in letters_guessed for letter in secret_word):
        result_label.config(text="🎉 You Won!")
        disable_all_buttons()
    elif guesses_left <= 0:
        result_label.config(text=f"💀 You Lost! The word was: {secret_word}")
        disable_all_buttons()

def disable_all_buttons():
    for btn in letter_buttons.values():
        btn.config(state=tk.DISABLED)

def enable_all_buttons():
    for btn in letter_buttons.values():
        btn.config(state=tk.NORMAL)

def get_available_letters(letters_guessed):
    return "".join([letter for letter in string.ascii_lowercase if letter not in letters_guessed])

def new_game():
    global secret_word, guesses_left, letters_guessed
    secret_word = choose_word(wordlist)
    guesses_left = GUESSES_START
    letters_guessed = []
    enable_all_buttons()
    result_label.config(text="")
    update_display()

# Load words and start game
wordlist = load_words()
secret_word = choose_word(wordlist)
guesses_left = GUESSES_START
letters_guessed = []

# Tkinter UI setup
root = tk.Tk()
root.title("Hangman Game")
root.geometry("700x500")
root.config(bg="#f0f0f0")

title_label = tk.Label(root, text="Hangman Game", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

word_label = tk.Label(root, text="", font=("Helvetica", 20), bg="#f0f0f0")
word_label.pack(pady=10)

guesses_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f0f0")
guesses_label.pack()

available_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f0f0")
available_label.pack(pady=5)

# Frame for letter buttons in grid layout
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

letter_buttons = {}
letters = list(string.ascii_lowercase)
for i, letter in enumerate(letters):
    btn = tk.Button(frame, text=letter.upper(), width=4, height=2,
                    command=lambda l=letter: guess_letter(l))
    btn.grid(row=i // 13, column=i % 13, padx=2, pady=2)  # 13 letters per row
    letter_buttons[letter] = btn

result_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
result_label.pack(pady=20)

new_game_btn = tk.Button(root, text="🔄 New Game", font=("Helvetica", 14), command=new_game)
new_game_btn.pack(pady=10)

update_display()
root.mainloop()
