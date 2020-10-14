from .devices import getAvailableDevices
from logger import Logger


def getAllDevices():
    devices = getAvailableDevices()
    Logger.v('获取到如下可操作设备:')
    for device in devices:
       Logger.v(str(device))
    return devices


def controllDevices(name):
    deviceList = list(
        filter(lambda device: name in device.name, getAllDevices()))
    if len(deviceList) == 0:
        Logger.e('控制米家设备失败', '未找到要控制的设备')
        return False
    else:
        result = []
        for device in deviceList:
            result.append(_controllDevice(device))
        return result


def _controllDevice(device):
    Logger.v('尝试控制设备:' + str(device))
    try:
      result = device.switch()
      Logger.v('控制设备结果:' + ('成功' if result else '失败'))
    except Exception as e:
      Logger.e('控制设备失败',e)

def test():
   return controllDevices('灯')


if __name__ == '__main__':
    print(getAllDevices())
