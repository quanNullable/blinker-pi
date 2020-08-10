from Blinker import Blinker, BlinkerButton, BlinkerNumber
from Blinker.BlinkerDebug import *
import controllers.controller as controllers
from config import getGeneralConfig

#BLINKER_DEBUG.debugAll()

Blinker.mode("BLINKER_WIFI")
Blinker.begin(getGeneralConfig()['blinker_id'])

buttonSpeak = BlinkerButton("btn-speak")

def speak_callback(state):
    BLINKER_LOG('get button state: ', state)
    result = controllers.handText("说话:你好啊")
    buttonSpeak.print(state)
    Blinker.print(result)

def data_callback(data):
    BLINKER_LOG("Blinker readString: ", data)
    result = controllers.handText(data)
    Blinker.print(result)

buttonSpeak.attach(speak_callback)
Blinker.attachData(data_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()