#! /usr/bin/python3
# -*- coding: utf-8 -*-

from Library import toolFunctions as functions
import json
from datetime import datetime, date, timedelta

def printTime():
    return functions.GenericTool.getTime()

def getKeyLocationsInfo(array):
    ret = "离线目录信息"
    ret += "\n====================\n\n"
    for i in array:
        ret += i
        ret += "\n--------------------\n"
        ret += functions.GenericTool.getSingleDirStat(i)
        ret += '\n'

    ret += "\n\n"
    return ret

def getFileStats(array):
    ret = "关键文件信息"
    ret += "\n====================\n"
    for i in array:
        ret += i
        ret += "\n--------------------\n"
        ret += functions.GenericTool.getSingleFileStat(i)

    ret += "\n"
    return ret

def getiCloudState():
    ret = "iCloud 静态信息"
    ret += "\n====================\n"
    ret += functions.GenericTool.getiCloudSessionDetails()

    ret += "\n"
    return ret

def getLocksUnlocksStt(time):
    ret = "设备锁定解锁日志" + "（" + time + " 以内）"
    ret += "\n====================\n"
    ret += functions.GenericTool.getLocksUnlocks(time)

    ret += "\n"
    return ret

def getElevationStt(time):
    ret = "权限提升日志" + "（" + time + " 以内）"
    ret += "\n====================\n"
    ret += functions.GenericTool.getSudoElevationLog(time)

    ret += "\n"
    return ret

def getLoginLog(count, host=None, tty=None, user=None):
    ret = "用户登录日志" + "（前 " + str(count) + " 条）"
    ret += "\n====================\n"
    ret += functions.GenericTool.getUserLogins(count, host, tty, user)

    ret += "\n"
    return ret

def getKeychainAccessStt(start, end):
    ret = "钥匙串访问日志" + "（ " + start + " ~ " + end +"）"
    ret += "\n====================\n"
    ret += functions.GenericTool.getKeychainAccessLog(start, end)

    ret += "\n"
    return ret

def bilibiliLoginHist():
    ret = "biliblil 登录日志（最近一周）\n\n"
    ret += "时间        IP 地址     结果   类型   运营商"
    ret +="\n=======================================\n"
    jsonret = json.loads(functions.GenericTool.getBilibiliLoginHist())
    if jsonret:
        for object in jsonret['data']['list']:
            ret += object['time_at']
            ret += "   "
            ret += object['ip']
            ret += "   "
            if object['status'] == True:
                ret += "成功"
            else:
                ret += "失败"
            ret += "   "
            ret += str(object['type'])
            ret += "   "
            ret += object['geo']
            ret += "\n"
    else:
        ret += "后台无数据或数据加载异常，请重试"
    ret += "\n已到尾部\n"
    return ret

def bilibiliPlayHist(endTime):
    endTime = int(datetime.strptime(endTime, "%Y-%m-%d").timestamp())
    ret = "biliblil 播放日志（截止时间：{0}）\n\n".format(endTime)
    ret += "AV 号        视频分段     分段编号   类型   播放时间"
    ret +="\n==============================================\n"
    jsonret = functions.GenericTool.getBilibiliPlayHist(endTime)
    if jsonret:
        for article in jsonret:
            ret += str(article['history']['oid'])
            ret += "     "
            ret += str(article['history']['page'])
            ret += "     "
            ret += str(article['history']['cid'])
            ret += "     "
            ret += str(article['history']['business'])
            ret += "     "
            ret += str(article['view_at'])
            ret += "\n"
    else:
        ret += "后台无数据或数据加载异常，请重试"
    ret += "\n已到尾部\n"
    return ret

def getTPExt():
    ret = "第三方内核扩展信息"
    ret += "\n====================\n"
    ret += functions.GenericTool.getTPKexts()
    ret += "\n"
    return ret

def getBrewListStt():
    ret = "开源软件包信息"
    ret += "\n====================\n"
    ret += functions.GenericTool.getBrewList()
    ret += "\n"
    return ret

def getAppListStt():
    ret = "应用软件列表"
    ret += "\n====================\n"
    ret += functions.GenericTool.getAppList()
    ret += "\n"
    return ret
