import random
import sys

def getRandomWord():
    with open('words.txt') as words:
         word_list = words.read().splitlines()
         ran_word = random.choice(word_list)
    return ran_word

def getDifficultyLevel():
    level = input('Would you like easy, medium, or hard difficulty? ')
    if level == 'easy' or level == 'medium' or level == 'hard':
        return level
    else:
        print('you must choose a level easy, medium or hard')
        return getDifficultyLevel()

def chooseWordOfCorrectLength(level):
    chosen_word = getRandomWord()
    if (level == 'easy'):
        while len(chosen_word) < 4 or len(chosen_word) > 6:
            chosen_word = getRandomWord()
    elif (level == 'medium'):
        while len(chosen_word) < 6 or len(chosen_word) > 8:
            chosen_word = getRandomWord()
    elif (level == 'hard'):
        while len(chosen_word) < 8:
            chosen_word = getRandomWord()
    return chosen_word

def initializeGame():
    print(chr(27) + "[2J")
    guesses_left = 8
    level = getDifficultyLevel()
    word = chooseWordOfCorrectLength(level)
    output = getWordOutput(word)
    print(f"your word has length: {len(word)}")
    printAstSepLine()
    print(f"you have {guesses_left} guesses")
    printWordOutput(output)
    actualGame(guesses_left, word, output)

def actualGame(guesses, word, output):
    letters_in_word = list(word)
    guessed_letters = []
    while True:
        checkForVictory(letters_in_word, word)
        checkForGuesses(guesses, word)
        guess = getUserGuess()
        if guess in guessed_letters:
            print('you have already guessed that letter')
        elif guess in letters_in_word:
            guessed_letters.append(guess)
            for _ in range(len(letters_in_word)):
                if guess == letters_in_word[_]:
                    output[_] = guess
                    letters_in_word[_] = ''
            print('you have guessed a correct letter')
            printAstSepLine()
            print(f"you have {guesses} guesses")
            print(f"guessed letters: {guessed_letters}")
            printWordOutput(output)
        else:
            guessed_letters.append(guess)
            guesses = guesses - 1
            print('you have guessed an incorrect letter')
            printAstSepLine()
            print(f"you have {guesses} guesses")
            print(f"guessed letters: {guessed_letters}")
            printWordOutput(output)

def checkForVictory(letters, word):
    victory = True
    for letter in letters:
        if letter != '':
            victory = False
    if victory:
        print("You have won")
        print(f"The word is {word}")
        playAgain()

def checkForGuesses(guesses, word):
    if guesses == 0:
        print("you have lost")
        print(f"the word is {word}")
        playAgain()

def playAgain():
    play_again = input("would you like to play again? yes or no: ")
    if play_again == 'no':
        print(chr(27) + "[2J")
        sys.exit(0)
    elif play_again == 'yes':
        initializeGame()
    else:
        print("you must answer yes or no")
        playAgain()

def getWordOutput(word):
    word_output = {}
    for _ in range(len(word)):
        word_output[_] = '_'
    return word_output

def printWordOutput(output):
    formated_output = ''
    for letter in output.items():
        if letter[0] == len(output)-1:
            formated_output += letter[1]
        else:
            formated_output += letter[1] + ' '
    print(formated_output)

def getUserGuess():
    letter_guess = input('Please guess a letter: ')
    if len(letter_guess) != 1:
        print("you must guess a single letter")
        return getUserGuess()
    elif not letter_guess.isalpha():
        print("you must guess a letter")
        return getUserGuess()
    elif letter_guess == '':
        print("you must provide a guess")
        return getUserGuess()
    else:
        letter_guess = letter_guess.lower()
        return letter_guess


def printAstSepLine():
    print('*' * 60)


if __name__ == "__main__":
    initializeGame()
