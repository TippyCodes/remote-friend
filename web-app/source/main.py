import env as Env

import backend.usersHandler as Users
import backend.devicesHandler as Devices
import server as Server


def startup():
    print('Hello World!')
    Users.initUsers()
    Devices.initDevices()


def run():
    Server.run()

# 
# Section: MAIN
# 

if __name__=='__main__':
    startup()
    run()