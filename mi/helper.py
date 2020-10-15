from .devices import getAvailableDevices
from logger import Logger


def getAllDevices():
    devices = getAvailableDevices()
    Logger.v('获取到如下可操作设备:')
    for device in devices:
       Logger.v(str(device))
    return devices


def switchDevices(name):
    deviceList = list(
        filter(lambda device: name in device.name, getAllDevices()))
    if len(deviceList) == 0:
        Logger.e('控制米家设备失败', '未找到要控制的设备')
        return False
    else:
        result = []
        for device in deviceList:
            Logger.v('尝试切换设备状态:' + str(device))
            try:
                result1 = device.switch()
                Logger.v('切换设备状态结果:' + ('成功' if result1 else '失败'))
            except Exception as e:
                Logger.e('切换设备状态失败',e)
            result.append(result1)
        return result

def turnOnDevices(name,on):
    deviceList = list(
        filter(lambda device: name in device.name, getAllDevices()))
    if len(deviceList) == 0:
        Logger.e('控制米家设备失败', '未找到要控制的设备')
        return False
    else:
        result = []
        desc = '打开' if on else '关闭'
        for device in deviceList:
            Logger.v('尝试'+desc+'设备:' + str(device))
            try:
                result1 = device.turnOn(on)
                Logger.v(desc+'设备结果:' + ('成功' if result1 else '失败'))
            except Exception as e:
                Logger.e(desc+'设备失败',e)
            result.append(result1)
        return result

def test():
   return turnOnDevices('灯',False)


if __name__ == '__main__':
    print(getAllDevices())
