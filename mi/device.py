# -*- coding: utf-8 -*-
from baseObject import BaseObject
from logger import Logger
from miio.device import Device as MiDevice


class Device(BaseObject):
    def __init__(self, info):
        self.ip = info.get('localip')
        self.token = info.get('token')
        self.name = info.get('name')
        self.did = info.get('did')
        self.model = info.get('model')
        if not self.ip is '':
            self.device = MiDevice(ip=self.ip, token=self.token)

    #切换设备状态:开着就关了,关着就打开
    def switch(self):
        Logger.e('切换设备状态失败', '暂不支持:' + self.device.info())
        return False

    #设置设备状态:打开或关闭
    def turnOn(self, on):
        Logger.e('开关设备失败', '暂不支持:' + self.device.info())
        return False
