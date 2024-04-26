from nltk.corpus import words

class Shiritori:
    
    gameName = 'Shiritori'
    maxScore = 50
    maxStrike = 3
    enDict = None

    # last letter first letter
    # one last letter = 1 point
    # two last letter = 2 points
    # 3 strikes per user    
    def __init__(self, user1):
        self.Player1 = Shiritori.Player(user1)
        self.Player2 = None
        self.UsedWords = set()

        # set dict if it doesnt already exist
        if Shiritori.enDict is None:
            Shiritori.enDict = set(words.words())
    
    # two players required
    def Join(self, user2):
        self.Player2 = Shiritori.Player(user2)

    # Game loop
    def Play(self):
        
        if self.Player2 is None:
            print("Second user must join")
            return None, None

        previousWord = None
        activePlayer = self.Player1

        while self.Player1.CanPlay() and self.Player2.CanPlay():
            
            nextLoop = False
            while not nextLoop and activePlayer.CanPlay():
                print("{uName} enter a word".format(uName=activePlayer.User.UserName))
                uWord = input().lower().strip()
                valid = self.ValidWord(uWord, previousWord)
            
                if not valid:
                    activePlayer.AddStrike()
                else:
                    score, isScoring = self.ScoringWord(uWord, previousWord)
                    if isScoring:
                        activePlayer.AddScore(score)
                        self.UsedWords.add(uWord)
                        previousWord = uWord
                        nextLoop = True
                        print("{user} has played '{prev}'".format(user=activePlayer.User.UserName, prev=previousWord))
                    else:
                        activePlayer.AddStrike()
            
            #swap player
            if activePlayer is self.Player1:
                activePlayer = self.Player2
            else:
                activePlayer = self.Player1
        
        winner = self.Winner().User
        loser = self.Player2.User if winner is self.Player1 else self.Player1.User
        print("{user} has beat {user2}".format(user=winner.UserName, user2=loser.UserName))

        return winner, loser

    # Check is matching substring at end of old word/beginning of new word
    def ScoringWord(self, uWord, previousWord):
        score = 0
        isScoring = False

        if previousWord is None:
            isScoring = True
            return score, isScoring

        # https://stackoverflow.com/questions/509211/how-slicing-in-python-works
        # https://stackoverflow.com/questions/663171/how-do-i-get-a-substring-of-a-string-in-python

        length1 = previousWord.__len__()
        length2 = uWord.__len__()
        truelen = length1 if (length1 < length2) else length2

        for i in range(1, truelen):
            # substring end of previous word == substring start of new word
            score = i
            if uWord[0:i] == previousWord[-i:]:
                isScoring = True
                return score, isScoring

        if not isScoring:
            print("Start of {word} does not match end of {prevword}".format(word=uWord, prevword=previousWord))
            return 0, isScoring

    # word exists in English dict; word is not equal to previous word; word has not been used
    def ValidWord(self, uWord, previousWord):
        isWord = (uWord in Shiritori.enDict)
        isNotEqual = previousWord != uWord
        isNotUsed = uWord not in self.UsedWords
        
        # snake -> snakes
        doesNotContain = True
        if previousWord is not None:
            doesNotContain = uWord not in previousWord and previousWord not in uWord

        if not isWord:
            print("{word} does not exist in English dictionary".format(word=uWord))
            return False
        if not isNotEqual:
            print("Word cannot be the same as the previous word")
            return False
        if not isNotUsed:
            print("{word} has already been used in this game".format(word=uWord))
            return False
        if not doesNotContain:
            print("{previousword} contains {word}, or vice versa".format(previousword=previousWord, word=uWord))
            return False
        
        return True

    # report winner
    def Winner(self):
        if self.Player1.OverStrike():
            return self.Player2
        elif self.Player1.OverScore():
            return self.Player1
        elif self.Player2.OverStrike():
            return self.Player1
        elif self.Player2.OverScore():
            return self.Player2
        else:
            raise Exception("Scoring and Strike logic is faulty, no winner")

    # player internal class
    class Player:
        def __init__(self, user):
            self.User = user
            self.Score = 0
            self.Strike = 0
        
        def CanPlay(self):
            if self.Score >= Shiritori.maxScore:
                return False
            if self.Strike >= Shiritori.maxStrike:
                return False
            return True
        
        def OverStrike(self):
            if self.Strike >= Shiritori.maxStrike:
                return True
            return False
        
        def OverScore(self):
            if self.Strike >= Shiritori.maxScore:
                return True
            return False
        
        def AddStrike(self):
            self.Strike += 1
            print("{username} has {strike} strike(s). {remainStrike} strike(s) left."
                  .format(username=self.User.UserName, strike=self.Strike, remainStrike=(Shiritori.maxStrike-self.Strike)))
        
        def AddScore(self, score):
            self.Score = self.Score + score
            