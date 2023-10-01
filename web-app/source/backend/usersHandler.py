import backend.models.userModel as UserModel
import backend.utilities as Utils

from flask import Blueprint, request


# 
# Section: Users table functions
# 

def adminUserExists():
    if not UserModel.getFristAdminUser():
        return False
    
    return True

def initUsers():
    UserModel.createUsersTable()

    if not adminUserExists():
        UserModel.createUser('admin', 'admin', UserModel.Privilege.ADMIN)

def wipeUsers():
    UserModel.dropUsersTable()
    initUsers()


# 
# Section: User Methods
# 

def validate(username, password):
    user = UserModel.getUser(username)
    if not user:
        return False # user does not exist
    
    if user.password != password:
        return False # the password is incorrect

    return user

def isPrivileged(username):
    user = UserModel.getUser(username)
    if not user:
        return False # user does not exist
    
    return user.privilege == UserModel.Privilege.ADMIN

def canDelete(username, adminUsername, adminPassword):
    if username == adminUsername:
        return False # admin cannot delete themselves
    
    if (not validate(adminUsername, adminPassword) or
        not isPrivileged(adminUsername)):
        return False # user does not have access to deleting UserModel
    
    return True

def login(username, password):
    user = validate(username, password)
    if not user:
        return Utils.APIResponse(False, 'Incorrect username or password.')

    msgRsp = Utils.APIResponse(True, 'Login successful.')
    msgRsp.user = UserModel.userObjToDict(user)

    return msgRsp

def register(username, password1, password2, privilege):
    if password1 != password2:
        return Utils.APIResponse(False, 'Passwords do not match.')

    newUser = UserModel.createUser(username, password1, privilege)
    if not newUser:
        return Utils.APIResponse(False, 'User could not be registered.')
    
    msgRsp = Utils.APIResponse(True, 'User successfully registered.')
    msgRsp.newUser = UserModel.userObjToDict(newUser)

    return msgRsp

def delete(username, adminUsername, adminPassword):
    if not canDelete(username, adminUsername, adminPassword):
        return Utils.APIResponse(False, 'Access denied.')

    if not UserModel.deleteUser(username):
        return Utils.APIResponse(False, 'User could not be deleted.')

    return Utils.APIResponse(True, 'User successfully deleted.')

# 
# Section: User server API
# 

users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/login', methods=['POST'])
def routeLogin():
    try:
        payload = request.json
        username = payload["username"]
        password = payload["password"]
    except:
        return { 'message': 'Invalid request.' }, 400
    
    return vars(login(username, password))