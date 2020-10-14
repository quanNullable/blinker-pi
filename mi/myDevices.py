import json
from logger import Logger
from .device import Device
from .chuangMiCamera import ChuangMiCamera
from .chuangMiPlug import ChuangMiPlug
from .chunMiCooker import ChunMiCooker
from .chuangMiRemote import ChunMiRemoteController
from .wifiSpeaker import MiWifiSpeaker

PATH = './mi/devices.json'

global MY_DEVICES
MY_DEVICES = []


#加载我所有的米家设备:从米家APP接口所获得的,只有did、token（暂时）、name（暂时）、pid、mac（暂时）、model是可信的
def loadAllDevices():
    global MY_DEVICES
    f = open(
        PATH, encoding='utf-8'
    )  #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    devices = json.load(f)
    for device in devices:
        formatDevice = None
        model = device.get('model')
        if 'chuangmi.plug' in model:  #插座
            formatDevice = ChuangMiPlug(device)
        elif 'chuangmi.camera' in model:  #摄像机
            formatDevice = ChuangMiCamera(device)
        elif 'chunmi.cooker' in model:  #电饭煲
            formatDevice = ChunMiCooker(device)
        elif 'chuangmi.remote' in model:  #遥控器
            formatDevice = ChunMiRemoteController(device)
        elif 'xiaomi.wifispeaker' in model:  #音箱
            formatDevice = MiWifiSpeaker(device)
        else:
            formatDevice = Device(device)
        MY_DEVICES.append(formatDevice)
    Logger.v('共获取到{}个本地存储的米家设备'.format(len(MY_DEVICES)))
    return MY_DEVICES


#根据指定类型的关键字查找设备,可能会有多个
def getDeviceByKey(value, key='name'):
    devices = []
    global MY_DEVICES
    if len(MY_DEVICES) == 0:
        loadAllDevices()
    for device in MY_DEVICES:
        result = getattr(device, key)
        if not result is None:
            if type(result) is str:
                if value in result:
                    devices.append(device)
            elif type(result) is int:
                if value == result:
                    devices.append(device)
    return devices


if __name__ == '__main__':
    print(getDeviceByKey(2038, 'pd_id'))
