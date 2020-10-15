from miio.chuangmi_plug import ChuangmiPlug
from logger import Logger
from .device import Device


class ChuangMiPlug(Device):
    def __init__(self, info):
        super().__init__(info)
        self.device = ChuangmiPlug(ip=self.ip, token=self.token)

    def switch(self):
        x = self.device.status()  # 给出设备的状态
        on = x.power
        success = False
        if on:
            result = self.device.off()
            success = result[0].upper() == 'OK'
        else:
            result = self.device.on()
            success = result[0].upper() == 'OK'
        if success:
            Logger.v('插座切换状态成功')
        else:
            Logger.e('插座切换状态失败', result)
        return success

    def turnOn(self, on):
        x = self.device.status()  # 给出设备的状态
        if x.power == on:
            Logger.v('插座已经处于此状态啦,无需操作!')
            return True
        else:
            success = False
            if on:
                result = self.device.on()
                success = result[0].upper() == 'OK'
            else:
                result = self.device.off()
                success = result[0].upper() == 'OK'
            if success:
                Logger.v('插座' + ('打开' if on else '关闭')+'成功')
            else:
                Logger.e('插座' + ('打开' if on else '关闭')+'失败', result)
            return success
