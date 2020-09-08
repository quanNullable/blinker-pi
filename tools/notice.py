from Blinker import Blinker, BlinkerButton, BlinkerNumber

def sendTextMsg(text):
    Blinker.notify("!" + text)


def sendImageMsg(image):
    Blinker.push(image)


def sendSms(text):
    Blinker.sms(text)