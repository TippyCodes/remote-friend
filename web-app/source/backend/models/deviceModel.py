import env as Env

import sqlite3
from dataclasses import dataclass

# #########################################################
# #########################################################
# 
# Model: deviceModel
# 
# the device model defines device related data and the interface for
# the Devices database table.
# 
# the Handler linked to this model is the deviceHandler. any
# access to this model should be via the Handler
# 
# #########################################################


# 
# Section: data definitions
# 

@dataclass
class Device:
    name:str

class Columns:
    ID      = 0
    NAME    = 1

# return a Device object representation of a device record
# id is excluded as it is unecessary
def deviceRecordToObj(deviceRecord):
    try:
        deviceObj = Device(
            deviceRecord[Columns.NAME])
    except:
        deviceObj = None
    
    return deviceObj

# return a dictionary representation of a Device object
# password is intentionaly excluded for protection
def deviceObjToDict(deviceObj):
    try:
        deviceDict = {
            'name': deviceObj.name,
        }
    except:
        deviceDict = None
    
    return deviceDict


# 
# Section: define Devices table
# 

def createDevicesTable():
    sql = """
        CREATE TABLE IF NOT EXISTS Devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

            name        TEXT UNIQUE     NOT NULL
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
        DROP TABLE IF EXISTS Devices
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql)
    finally:
        conn.commit()
        conn.close()


# 
# Section: Devices Table CRUD
# 

# create device with name
# return the new device as a Device object
# reutrn None if device could not be created
def createDevice(name):
    sql = """
        INSERT INTO Devices (name)
        VALUES (?)
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql, (name,))
    except:
        conn.commit()
        conn.close()
        newDeviceObj = None
    else:
        conn.commit()
        conn.close()
        newDeviceObj = getDevice(name)

    return newDeviceObj

# retrive device by name
# return device as Device object
# reutrn None if no device was retrieved
def getDevice(name):
    sql = """
        SELECT *
        FROM Devices
        WHERE name=?
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql, (name,))
        deviceRecord = curs.fetchone()
    except:
        deviceRecord = None
    finally:
        conn.commit()
        conn.close()
    
    return deviceRecordToObj(deviceRecord)

# delete device with name
# return True if device was deleted
# return False if device could not be deleted
def deleteUser(name):
    sql = """
        DELETE FROM Devices
        WHERE name=?
    """
    conn = sqlite3.connect(Env.DB)
    try:
        curs = conn.cursor()
        curs.execute(sql, (name,))
        isDeleted = True
    except:
        isDeleted = False
    finally:
        conn.commit()
        conn.close()
    
    return isDeleted