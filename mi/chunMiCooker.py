from miio.cooker import Cooker
from logger import Logger
from .device import Device


class ChunMiCooker(Device):
    def __init__(self, info):
        super().__init__(info)
        self.device = Cooker(ip=self.ip, token=self.token)

  