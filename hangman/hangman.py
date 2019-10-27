import random

from hangman.lives import LIVES

with open('hangman/words.txt') as f:
    lines = f.read().splitlines()

action_list = []

first_time = True
word = ""
letters = []
hearts = 10


def random_word():
    return lines[random.randint(0, len(lines))].lower()


def display_letters(letters):
    dashes = ""
    for w in word:
        if w in letters:
            dashes += w
        else:
            dashes += "-"
    return dashes


def hanging_man(hearts):
    i = 10 - hearts
    return LIVES[i]


def first_message(word):
    return "Welcome to hangman. Your word is " + str(
        len(word)) + " letters long. \nYou currently have 10 lives left. \n" + LIVES[0] + "Enter your first letter! \n"


def first_run():
    global first_time
    global word
    word = random_word()
    print(word)
    message = first_message(word)
    first_time = False
    return message


def run_game(letter):
    global hearts
    if first_time:
        return first_run()
    else:
        if letter in word:
            letters.append(letter)
            if "-" not in display_letters(letters):
                return "Well Done! You beat hangman"
            else:
                return hanging_man(hearts) + "You have " + str(hearts) + " lives left \n" + display_letters(letters)
        else:
            hearts -= 1
            if hearts == 0:
                reset()
                return "You failed. Try again next time"
            else:
                return hanging_man(hearts) + "You have " + str(hearts) + " lives left \n" + display_letters(letters)


def reset():
    global first_time
    global hearts
    global word
    global letters
    first_time = True
    hearts = 10
    word = ""
    letters = []
