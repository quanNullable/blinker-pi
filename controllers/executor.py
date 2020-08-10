# -*- coding: utf-8 -*-
# 命令执行器 具体命令执行

import time, threading, shutil, subprocess, os
from comands import ALL_COMANDS
from tools.baiduVoice import say1
from config import getGeneralConfig
from logger import Logger

def executCommand(command):
    if command.Name == ALL_COMANDS[0].Name: 
        say1("我此次出现该异常的情况是不显示了。") 
        result = '执行成功'
    elif command.Name == ALL_COMANDS[1].Name: 
        say1(command.Parmas) 
        result = '执行成功'
    else:
        result = '暂未完成'
    Logger.v('命令<' + command.Name + '>执行结果<' + result + '>')
    return result


def sendResultLater(to, func, args=None):
    def getResultAndSend():
        try:
            result = func() if args is None else func(args)
            if not result is None:
                if len(result) < 50 and ('.png' in result
                                        or '.jpg' in result):  #如果是个图片 则发送图片
                    sendImageMsg(to.Id, result)
                    os.remove(result)
                else:
                    sendTextMsg(to.Id, result)
            else:
                Logger.v(func.__name__ + '未返回执行结果')
        except Exception as e:
            Logger.e(func.__name__ + '执行失败', e)
        #  print(func,' error',e)

    threading.Thread(target=getResultAndSend).start()
    return '已开始执行'


def _getJobInfoAndSend(to, jobName):
    try:
        filePath = getJobInfo(jobName)
        tempDir = 'temp/'
        images = ReportImage.excel2Image(filePath, tempDir, 50)
        for image in images:
            sendImageMsg(to.Id, image)
        shutil.rmtree(tempDir)
    except Exception as e:
        Logger.e('爬取拉勾数据失败', e)


def _getWechatUserInfoAndSend(userId):
    userInfo = getWechatUser(userId)
    if 'errcode' in userInfo:
        result = userInfo['errmsg']
        Logger.e('从微信获取用户信息失败', result)
    else:
        updateUserByDict(userInfo)
        result = '姓名:'+userInfo['nickname']+'\n'+\
                 '性别:'+('男' if userInfo['sex'] == 1 else '女')+'\n'+\
                 '省份:'+userInfo['province']+'\n'+\
                 '城市:'+userInfo['city']+'\n'+\
                 '头像:'+userInfo['headimgurl']+'\n'+\
                 '时间:'+time.strftime("%Y年%m月%d日",time.localtime(userInfo['subscribe_time']))+'\n'
    return result


def _sendMsgToAll(commander, msg):
    users = getUsers()
    result = ''
    if len(users) > 0:
        for user in users:
            sendTextMsg(user.Id, msg)
        result = '已发送<' + msg + '>至{}位用户'.format(len(users))
    else:
        result = '没有可用用户'
    sendTextMsg(commander.Id, result)


def _executeShell(user, command):
    status, output = subprocess.getstatusoutput(command)
    result = ('执行成功:\n' if status == 0 else '执行失败:\n') + output
    sendTextMsg(user.Id, result)


def _runTaskRightNow(user, funcName):
    func = getattr(task, funcName,None)
    if func is None:
        sendTextMsg(user.Id, '未找到指定任务')
    else:
        if callable(func):
            Logger.v('开始执行' + funcName)
            func(True)
        else:
            Logger.e(func + '无法执行','not callable')

#截图发送日志
def _getSysLogByImage(name=None):
    if name is None:
       name = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    logPath = getGeneralConfig()['log_path']
    logName = logPath + name + '.log'
    result = ''
    if os.path.exists(logName):
        try:
            logImg = 'temp/log.png'
            result = Text2Image.textFile2Image(logName, logImg)
        except Exception as e:
            Logger.e('读取日志文件' + logName + '失败', e)
            result = '读取日志失败'
    else:
        result = '日志不存在'
    return result

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

def getCommandsHelp(user):
    def formatCommands(commands):
        descs = []
        for comand in commands:
            desc = '命令:'+comand.Name+'\n'+\
            '作用:'+comand.Func+'\n'+\
            '用法:'+comand.Usage+'\n'
            descs.append(desc)
        return '\n'.join(descs)  
    commandList = list(filter(lambda com:com.Permission <= user.Level, ALL_COMANDS))
    commandsCount = len(commandList)
    maxCount = 20
    if commandsCount == 0:
        return '暂无可用命令'
    elif commandsCount > maxCount:#拆分
        def splitList(orgList, length):
            listGroups = zip(*(iter(orgList),) *length)
            newList = [list(i) for i in listGroups]
            count = len(orgList) % length
            newList.append(orgList[-count:]) if count !=0 else newList
            return newList
        commandSplitList = splitList(commandList,maxCount)
        for spList in commandSplitList:
            sendTextMsg(user.Id,formatCommands(spList))
        return ''
    else:
        return formatCommands(commandList)
                                                
def callXiaoAi(text):
    voice('小爱同学')
    time.sleep(1)
    voice(text)
