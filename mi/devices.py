import subprocess
from .myDevices import getDeviceByKey
from logger import Logger

def _discoveryDeviceIps():
    status, output = subprocess.getstatusoutput('mirobo discover --handshake 1')
    ips = []
    if status == 0:
       items = output.split('miio.miioprotocol:  IP'.strip())
       for item in items:
           if '(ID:' in item:
               ip = item.split('(ID:')[0].strip()
               ips.append(ip)
    Logger.v('共发现{}个可操作的米家设备:'.format(len(ips))+str(ips))
    return ips

def _getDevicesByIps(ips):
    devices = []
    if len(ips) != 0:
        for ip in ips:
           result = getDeviceByKey(ip,'ip')
           if len(result) != 0:
               devices += result
    return devices

def getAvailableDevices():
   return _getDevicesByIps(_discoveryDeviceIps())


def _discoveryDevices():
    import miio
    d = miio.discovery.Discovery()
    a =  d.discover_mdns()
    print(a)

if __name__ == '__main__':
    print(_discoveryDevices())