import random
import re
import sys

def getRandomWordList(word_length):
    with open('words.txt') as words:
         word_list = words.read()
         regex_exp = r'\b[a-zA-Z]{' + re.escape(str(word_length)) + r'}\b'
         word_list = re.findall(regex_exp, word_list)
    return word_list

def getDifficultyLevel():
    word_length = input('Please provide a word length between 4 and 24: ')
    if not word_length.isnumeric():
        print('you must provide a number')
        return getDifficultyLevel()
    if int(word_length) < 4 or int(word_length) > 24:
        print('you must choose a word length between 4 and 24')
        return getDifficultyLevel()
    else:
        return word_length

def initializeGame():
    print(chr(27) + "[2J")
    guesses_left = 8
    word_length = getDifficultyLevel()
    words = getRandomWordList(word_length)
    output = getWordOutput(word_length)
    print(f"your word has length: {word_length}")
    printAstSepLine()
    print(f"you have {guesses_left} guesses")
    printWordOutput(output)
    actualGame(guesses_left, words, output)

def actualGame(guesses, words, output):
    letters_in_word = list('_' * len(output))
    guessed_letters = []
    num_current_words = len(words)
    word = ''
    while True:
        checkForVictory(letters_in_word, words)
        checkForGuesses(guesses, words)
        guess = getUserGuess()
        new_words_and_family = pareDownWordList(words, guess, letters_in_word)
        words = new_words_and_family[0]
        family = new_words_and_family[1].split('_')
        if guess in guessed_letters:
            print('you have already guessed that letter')
        elif len(words) < num_current_words:
            guessed_letters.append(guess)
            for index in family:
                output[int(index)] = guess
                letters_in_word[int(index)] = guess
            print('you have guessed a correct letter')
            printAstSepLine()
            print(f"you have {guesses} guesses")
            print(f"guessed letters: {guessed_letters}")
            printWordOutput(output)
            num_current_words = len(words)
        else:
            guessed_letters.append(guess)
            guesses = guesses - 1
            print('you have guessed an incorrect letter')
            printAstSepLine()
            print(f"you have {guesses} guesses")
            print(f"guessed letters: {guessed_letters}")
            printWordOutput(output)

def pareDownWordList(words, guess, letters):
    word_lists = {}
    open_spaces = []
    for x in range (len(letters)):
        if letters[x] == '_':
            open_spaces.append(x)
    for word in words:
        word = word.lower()
        word_family = ''
        for x in range(len(word)):
            if word[x] == guess and x in open_spaces:
                if word_family == '':
                    word_family = str(x)
                elif word_family != '':
                    word_family += '_' + str(x)
        if word_family != '' and word_lists.get(word_family, None) == None:
            word_lists[word_family] = []
            word_lists[word_family].append(word)
        elif word_family != '':
            word_lists[word_family].append(word)
    largest_family = ''
    for family in word_lists:
        if largest_family == '':
            largest_family = family
        elif largest_family != '':
            if len(word_lists[family]) > len(word_lists[largest_family]):
                largest_family = family
    if largest_family == '':
        return words, largest_family
    else:
        return word_lists[largest_family], largest_family

def checkForVictory(letters, words):
    victory = True
    for letter in letters:
        if letter == '_':
            victory = False
    if victory:
        print("You have won")
        print(f"The word is: " + words[0])
        playAgain()

def checkForGuesses(guesses, words):
    if guesses == 0:
        print("you have lost")
        print(f"the word is: " + words[0])
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

def getWordOutput(word_length):
    word_output = {}
    for _ in range(int(word_length)):
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
