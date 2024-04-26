import os
from random import randrange 
import User

class Wordle:
    # static diplay encoding
    # CHANGE BASED ON OUTPUT DISPLAY
    correct = 'O '
    close = '/ '
    empty = 'X '

    gameName = 'Wordle'

    def __init__(self, user):
        self.User = user

    # generate an Answer from the Valid Answer dictionary
    def GenerateAnswer(self):
        # wordle answer path
        localFolder = os.getcwd()
        answerDb = os.path.join(localFolder, "Db", "wordleAnswers.txt")

        # read all potential answers
        answer = ""
        with open(answerDb, "r") as fin:
            # readlines() includes new line character
            # read.splitlines() excludes new line character
            allAnswers = fin.read().splitlines()
            totAnswers = allAnswers.__len__()
            randIndex = randrange(totAnswers)
            answer = allAnswers[randIndex] 

        return answer

    # check if Guess word exists in the Valid Guess dictionary
    # static methods save a few bytes for call; only valuable for heavy recursion
    # @staticmethod
    def ValidateGuess(self, userGuess):
        # wordle valid guesses path
        localFolder = os.getcwd()
        guessDb = os.path.join(localFolder, "Db", "wordleGuess.txt")

        validGuess = False
        # read all valie guesses
        with open(guessDb, "r") as fin:
            # readlines() includes new line character
            # read.splitlines() excludes new line character
            allGuesses = fin.read().splitlines()
            validGuess = userGuess in allGuesses
            
        return validGuess

    def Play(self):

        # current answer
        answer = self.GenerateAnswer()
        answerLen  = answer.__len__()

        guesslimit = 5

        # game loop
        for x in range(0, guesslimit, 1):
            
            # receive guess from user
            guess = ""
            guessEncode = [None] * answerLen

            validGuess = False
            while validGuess is False:
                
                notif = "Guess {guessnum}"
                print(notif.format(guessnum = x+1))

                guess = input()
                validGuess = self.ValidateGuess(guess)

            # current loop win/lose state
            win = True

            # loop through each character in guess
            for y in range(0, answerLen, 1):
                character = guess[y]

                if answer[y]==character:
                    guessEncode[y] = self.correct
                elif answer.__contains__(character):
                    guessEncode[y] = self.close
                    win = False
                else:
                    guessEncode[y] = self.empty
                    win = False
            
            # *array prints the array as a contiguous string
            print(*guessEncode)

            if win == True:
                print("{user} wins!".format(user=self.User.UserName))
                return True
            
        loseStr = "{user} loses, the correct answer was {ans}".format(user=self.User.UserName,ans=answer)
        print(loseStr)
        return False
