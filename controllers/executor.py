# -*- coding: utf-8 -*-
# 命令执行器 具体命令执行

import time, threading, shutil, subprocess, os
from comands import ALL_COMANDS
from tools.baiduVoice import say1
from config import getGeneralConfig
from logger import Logger
from tools.notice import sendTextMsg,sendImageMsg
from mi.helper import test

def executCommand(command):
    if command.Name == ALL_COMANDS[0].Name: 
        say1("我此次出现该异常的情况是不显示了。") 
        result = '执行成功'
    elif command.Name == ALL_COMANDS[1].Name: 
        say1(command.Parmas) 
        result = '执行成功'
    elif command.Name == ALL_COMANDS[2].Name: 
        threading.Thread(
            target=_executeShell,
            args=(command.Parmas,)).start()
        result = '已开始执行'
    else:
        result = test()
    Logger.v('命令<' + command.Name + '>执行结果<' + str(result) + '>')
    return result


def sendResultLater(func, args=None):
    def getResultAndSend():
        try:
            result = func() if args is None else func(args)
            if not result is None:
                if len(result) < 50 and ('.png' in result
                                        or '.jpg' in result):  #如果是个图片 则发送图片
                    sendImageMsg(result)
                    os.remove(result)
                else:
                    sendTextMsg(result)
            else:
                Logger.v(func.__name__ + '未返回执行结果')
        except Exception as e:
            Logger.e(func.__name__ + '执行失败', e)
        #  print(func,' error',e)

    threading.Thread(target=getResultAndSend).start()
    return '已开始执行'


def _executeShell(command):
    status, output = subprocess.getstatusoutput(command)
    result = ('执行成功:\n' if status == 0 else '执行失败:\n') + output
    sendTextMsg(result)


def _runTaskRightNow(funcName):
    func = getattr(task, funcName,None)
    if func is None:
        sendTextMsg('未找到指定任务')
    else:
        if callable(func):
            Logger.v('开始执行' + funcName)
            func(True)
        else:
            Logger.e(func + '无法执行','not callable')

#上传至cos后返回访问地址
def _getSysLogByCos(name=None):
    if name is None:
       name = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    logPath = getGeneralConfig()['log_path']
    logName = logPath + name + '.log'
    result = ''
    if os.path.exists(logName):
        try:
            result = uploadFile(logName)
        except Exception as e:
            Logger.e('上传日志文件' + logName + '失败', e)
            result = '读取日志失败'
    else:
        result = '日志不存在'
    return result

def getCommandsHelp():
    def formatCommands(commands):
        descs = []
        for comand in commands:
            desc = '命令:'+comand.Name+'\n'+\
            '作用:'+comand.Func+'\n'+\
            '用法:'+comand.Usage+'\n'
            descs.append(desc)
        return '\n'.join(descs)  
    commandsCount = len(ALL_COMANDS)
    if commandsCount == 0:
        return '暂无可用命令'
    else:
        return formatCommands(ALL_COMANDS)
