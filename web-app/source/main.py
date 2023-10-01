import env as Env

import server as Server


def startup():
    print('Hello World!')


def run():
    Server.run()

# 
# Section: MAIN
# 

if __name__=='__main__':
    startup()
    run()