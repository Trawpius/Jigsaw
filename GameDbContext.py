import os
import sqlite3
import sqlalchemy
# refactor with sqlalchemy

# data = [
#     ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
#     ("Monty Python's The Meaning of Life", 1983, 7.5),
#     ("Monty Python's Life of Brian", 1979, 8.0),
# ]
# cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
# con.commit()  # Remember to commit the transaction after executing INSERT.
# notice that ? placeholders are used to bind data to the query. Always use placeholders instead of string formatting to bind Python values to SQL statements, to avoid SQL injection attacks (see How to use placeholders to bind values in SQL queries for more details).

# We can verify that the new rows were inserted by executing a SELECT query, this time iterating over the results of the query:

from User import User

class GameDbContext:
    # connect to gamedata.db
    def __init__(self):
        localFolder = os.getcwd()
        self.dbPath = os.path.join(localFolder, "Db", "gamedata.db")
        self.connection  = sqlite3.connect(self.dbPath)

    # check connection
    def IsConnected(self):
        return self.connection is not None

    # add new User object to user table
    def AddNewUser(self, user):
        self.connection.execute("INSERT INTO user VALUES({id},'{name}')".format(id=user.UserId, name=user.UserName))
        gameIds = self.GetGameIdAll()
        for x in gameIds:
            injectStr = '0,0,{uId},{gId}'.format(uId=user.UserId, gId=x)
            self.AddData('scoreboard',injectStr)
        self.connection.commit()
    
    def AddNewGame(self, gameName):
        res = self.connection.execute("SELECT gameID FROM game")
        resAll = res.fetchall()
        
        intSet = set()
        for x in resAll:
            intSet.add(x[0])
        id = max(intSet) + 1

        self.connection.execute("INSERT INTO game VALUES({id},'{name}')".format(id=id, name=gameName))
        self.connection.commit()

    # insert generic UNCONTROLLED
    def AddData(self, tableName, injectStr):
        self.connection.execute('INSERT INTO {table} VALUES({inject})'.format(table=tableName,inject=injectStr))
        self.connection.commit()

    def CreateTable(self, injectStr):
        self.connection.execute(injectStr)
        self.connection.commit()

    def GetGameIdAll(self):
        res = self.connection.execute('SELECT * FROM game')
        resAll = res.fetchall()
        gameIdList = []
        for x in resAll:
            gameIdList.append(x[0])
        return gameIdList

    def GetGameIdByName(self, gameName):
        res = self.connection.execute("SELECT * FROM game WHERE gameName='{name}'".format(name=gameName))
        resSingle = res.fetchone()
        if resSingle is None:
            return None
        else:
            # first element is gameId
            return resSingle[0]

    def GetUserSingle(self, user):
        res = self.connection.execute('SELECT * FROM user WHERE userID={id} AND userName={user}'.format(id=user.UserId, user=user.UserName))
        resSingle = res.fetchone()
        if resSingle is None:
            return None
        else:
            rtnUser = User(resSingle[0], resSingle[1])
            return rtnUser

    def GetUserByIDSingle(self, userId):
        res = self.connection.execute('SELECT * FROM user WHERE userID={id}'.format(id=userId))
        resSingle = res.fetchone()
        if resSingle is None:
            return None
        else:
            rtnUser = User(resSingle[0], resSingle[1])
            return rtnUser
        
    def PrintTable(self, tableName):
        res = self.connection.execute('SELECT * FROM {table}'.format(table=tableName))
        resAll = res.fetchall()
        print(resAll)
    
    def PrintAllTables(self):
        res = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        resAll = res.fetchall()
        for r in resAll:
            self.PrintTable(r[0])
    
    def UpdateScoreboard(self, user, gameName, winlose):
        uId = user.UserId
        gId = self.GetGameIdByName(gameName)
       
        columnName = "lose"
        if winlose == True:
            columnName = "win"
        
        res = self.connection.execute('SELECT {columnName} FROM scoreboard WHERE gameID={gId} AND userID={uId}'.format(columnName=columnName, gId=gId, uId=uId))
        resOne = res.fetchone()
        
        if resOne is not None:
            scoreCount = resOne[0] + 1
            res = self.connection.execute('UPDATE scoreboard SET {columnName} = {scoreCount} WHERE gameID={gId} AND userID={uId}'.format(columnName = columnName, scoreCount=scoreCount, gId=gId, uId=uId))
        else:
            if winlose == True:
                self.connection.execute("INSERT INTO scoreboard VALUES(1,0,{uId},{gId})".format(gId=gId, uId=uId))
            else:
                self.connection.execute("INSERT INTO scoreboard VALUES(0,1,{uId},{gId})".format(gId=gId, uId=uId))
        self.connection.commit()
    
    def PrintWinRate(self, user, gameName):

        uId = user.UserId
        gId = self.GetGameIdByName(gameName)

        res = self.connection.execute('SELECT win FROM scoreboard WHERE gameID={gId} AND userID={uId}'.format(gId=gId, uId=uId))
        win = res.fetchone()[0]
        res = self.connection.execute('SELECT lose FROM scoreboard WHERE gameID={gId} AND userID={uId}'.format(gId=gId, uId=uId))
        lose = res.fetchone()[0]

        total = win + lose
        perc = win / total * 100
        print('{username} has a {percent:.2f} win rate at {gamename}'.format(username=user.UserName, percent=perc, gamename=gameName))
    
    def PrintWinRateAll(self, user):
        allIDs = self.GetGameIdAll()
        for x in allIDs:
            print(x)
            self.PrintWinRate(user, x)

