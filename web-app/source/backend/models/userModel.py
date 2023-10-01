import env as Env

import sqlite3
from dataclasses import dataclass

# #########################################################
# #########################################################
# 
# Model: userModel
# 
# the user model defines user related data and the interface for
# the Users database table.
# 
# the Handler linked to this model is the userHandler. any
# access to this model should be via the Handler
# 
# #########################################################


# 
# Section: data definitions
# 

@dataclass
class User:
    username:str
    password:str
    privilege:int

class Privilege:
    PUBLIC  = 0
    ADMIN   = 1

class Columns:
    ID          = 0
    USERNAME    = 1
    PASSWORD    = 2
    PRIVILEGE   = 3

# return a User object representation of a user record
# id is excluded as it is unecessary
def userRecordToObj(userRecord):
    try:
        userObj = User(
            userRecord[Columns.USERNAME],
            userRecord[Columns.PASSWORD],
            userRecord[Columns.PRIVILEGE])
    except:
        userObj = None
    
    return userObj

# return a dictionary representation of a User object
# password is intentionaly excluded for protection
def userObjToDict(userObj):
    try:
        userDict = {
            'username': userObj.username,
            'privilege': userObj.privilege,
        }
    except:
        userDict = None
    
    return userDict


# 
# Section: define Users table
# 

def createUsersTable():
    sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

            username    TEXT UNIQUE     NOT NULL,
            password    TEXT            NOT NULL,
            privilege   INTEGER         NOT NULL
        )
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql)
    finally:
        conn.commit()
        conn.close()

def dropUsersTable():
    sql = """
        DROP TABLE IF EXISTS Users
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql)
    finally:
        conn.commit()
        conn.close()


# 
# Section: Users Table CRUD
# 

# create user with username, password and privilege
# return the new user as a User object
# reutrn None if user could not be created
def createUser(username, password, privilege):
    sql = """
        INSERT INTO Users (username, password, privilege)
        VALUES (?, ?, ?)
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql, (username, password, privilege,))
    except:
        conn.commit()
        conn.close()
        newUserObj = None
    else:
        conn.commit()
        conn.close()
        newUserObj = getUser(username)

    return newUserObj

# retrive user by username
# return user as User object
# reutrn None if no user was retrieved
def getUser(username):
    sql = """
        SELECT *
        FROM Users
        WHERE username=?
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql, (username,))
        userRecord = curs.fetchone()
    except:
        userRecord = None
    finally:
        conn.commit()
        conn.close()
    
    return userRecordToObj(userRecord)

# retrieve the first admin user in the table
# return the admin user as User object
# return None if there are no admin users
def getFristAdminUser():
    sql = """
        SELECT *
        FROM Users
        WHERE privilege=?
        LIMIT 1
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql, (Privilege.ADMIN,))
        adminRecord = curs.fetchone()
    except:
        adminRecord = None
    finally:
        conn.commit()
        conn.close()
    
    return userRecordToObj(adminRecord)

# delete user with username
# return True if user was deleted
# return False if user could not be deleted
def deleteUser(username):
    sql = """
        DELETE FROM Users
        WHERE username=?
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql, (username,))
        isDeleted = True
    except:
        isDeleted = False
    finally:
        conn.commit()
        conn.close()
    
    return isDeleted