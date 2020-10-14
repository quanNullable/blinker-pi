from miio.chuangmi_ir import ChuangmiIr
from logger import Logger
from .device import Device


class ChunMiRemoteController(Device):
    def __init__(self, info):
        super().__init__(info)
        self.device = ChuangmiIr(ip=self.ip, token=self.token)

  