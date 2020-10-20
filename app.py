from Blinker import Blinker, BlinkerButton
from Blinker.BlinkerDebug import *
import controllers.controller as controllers
from config import getGeneralConfig
from tools.baiduVoice import say1

#BLINKER_DEBUG.debugAll()

Blinker.mode("BLINKER_WIFI")
Blinker.begin(getGeneralConfig()['blinker_id'])

buttonSpeak = BlinkerButton("btn-speak")
buttonRestart = BlinkerButton("btn-restart")

def speak_callback(state):
    result = controllers.handText("说话:你好啊")
    buttonSpeak.print(state)
    Blinker.print(result)

def restart_callback(state):
    say1("正在重启树莓派!") 
    result = controllers.handText("执行代码:cd /home/pi/Codes/WeChat/PiController && sudo git pull && sudo /home/pi/Codes/AutoRun/startPiController.sh")
    buttonRestart.print(state)
    Blinker.print(result)
    

def data_callback(data):
    if isinstance(data, str):
        result = controllers.handText(data)
    elif isinstance(data, dict):
        result = str(data)
    else:
        result = "无法识别命令"
    Blinker.print(result)

buttonSpeak.attach(speak_callback)
buttonRestart.attach(restart_callback)
Blinker.attachData(data_callback)
say1("Blinker控制器已启动!") 

if __name__ == '__main__':

    while True:
        Blinker.run()