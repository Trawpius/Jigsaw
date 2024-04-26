from GameDbContext import GameDbContext
from Shiritori import Shiritori
from User import User
from Wordle import Wordle

# try sqlalchemy, django?
import os



gameDb = GameDbContext()

# user 1 login
print("User ID")
id = input()
user = None

user = gameDb.GetUserByIDSingle(id)

if user is None:
    print("User Name")
    name = input()
    user = User(id, name)
    gameDb.AddNewUser(user)

print("Hello {}".format(user.UserName))

# user 2 login
print("User ID")
id = input()
user2 = None

user2 = gameDb.GetUserByIDSingle(id)
1234
if user2 is None:
    print("User Name")
    name = input()
    user2 = User(id, name)
    gameDb.AddNewUser(user2)

print("Hello {}".format(user2.UserName))

shiritori = Shiritori(user)
shiritori.Play()
shiritori.Join(user2)

#winner, loser = shiritori.Play()

#gameDb.UpdateScoreboard(winner, Shiritori.gameName, True)
#gameDb.UpdateScoreboard(loser, Shiritori.gameName, False)

gameDb.PrintWinRateAll(winner)
gameDb.PrintWinRateAll(loser)
