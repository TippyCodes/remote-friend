import backend.models.deviceModel as DeviceModel
import backend.utilities as Utils

from flask import Blueprint, request


# 
# Section: Users table functions
# 

def initDevices():
    DeviceModel.createDevicesTable()

def wipeDevices():
    DeviceModel.dropUsersTable()
    initDevices()


# 
# Section: Device Methods
# 

def greeting(deviceName):
    device = DeviceModel.getDevice(deviceName)
    if not device:
        return Utils.APIResponse(True, 'Hello {}. Nice to meet you.'.format(deviceName))
    else:
        return Utils.APIResponse(True, 'Hello, welcome back.')

def register(deviceName):
    newDevice = DeviceModel.createDevice(deviceName)
    if not newDevice:
        return Utils.APIResponse(False, 'Sorry {}. You could not be registered.'.format(deviceName))
    
    msgRsp = Utils.APIResponse(True, 'Welcome Friend! You have been successfuly registered.')
    msgRsp.newDevice = DeviceModel.deviceObjToDict(newDevice)

    return msgRsp


# 
# Section: Device server API
# 

devices_bp = Blueprint('devices_bp', __name__)


@devices_bp.route('/greeting', methods=['GET'])
def routeGreeting():
    try:
        deviceName = request.args.get('name')
    except:
        return { 'message': 'Invalid request.' }, 400
    
    return vars(greeting(deviceName))


@devices_bp.route('/register', methods=['POST'])
def routeRegister():
    try:
        payload = request.json
        deviceName = payload["name"]
    except:
        return { 'message': 'Invalid request.'}, 400
    
    return vars(register(deviceName))