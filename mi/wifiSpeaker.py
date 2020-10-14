from miio.wifispeaker import WifiSpeaker
from logger import Logger
from .device import Device


class MiWifiSpeaker(Device):
    def __init__(self, info):
        super().__init__(info)
        self.device = WifiSpeaker(ip=self.ip, token=self.token)

  