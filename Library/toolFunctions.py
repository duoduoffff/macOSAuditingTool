#! /usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import re
import subprocess
import json as jsonparser
import os
from datetime import datetime, date

class envInspection:
    """docstring for envInspection."""

    def checkFor(arg):
        pass

class CmdErrorException (Exception):
    """docstring for GenericException."""

    def str(self):
        print("CmdErrorException!")

class ConfigurationException (Exception):
    """docstring for ConfigurationException."""

    def str(self):
        print("ConfigurationException!")


class GenericTool:
    """docstring for GenericTool."""

    def runArbitraryCmd(string):
        print(string)
        string += "; exit 0"
        cmd = subprocess.check_output(string, stderr=subprocess.STDOUT, shell = True)
        return cmd.decode("utf-8")

    def getConfigs(document):
        f = open(document, "r")
        if f:
            json = jsonparser.loads(f.read())
            f.close()
        else:
            raise CmdErrorException()
        return json

    def getTime():
        return GenericTool.runArbitraryCmd('date')

    def getSingleDirStat(absp):
        cmd = 'du -shc ' + absp + "/*"
        return GenericTool.runArbitraryCmd(cmd)

    def getSingleFileStat(absPath): #completed
        return GenericTool.runArbitraryCmd('stat  -f \'accs:%Sa, modif:%Sm, inodechg:%Sc, birth:%SB\' -t \'%Y-%m-%d %H:%M:%S\' ' + absPath)

    def getiCloudSessionDetails():
        return GenericTool.runArbitraryCmd('defaults read MobileMeAccounts')

    def getSudoElevationLog(time):
        if not time:
            time = "1d"
        return GenericTool.runArbitraryCmd('log show --style syslog --predicate "process == \'sudo\'" --last ' + time + " | grep \"TTY\"")

    def getUserLogins(count, host, tty, user):
        str = 'last'
        if count:
            str = str + ' -n ' + count
        if host:
            str = str + ' -h ' + host
        if tty:
            str = str + ' -t ' + tty
        if user:
            str = str + " " + user
        return GenericTool.runArbitraryCmd(str)

    def getLocksUnlocks(time): #completed
        str = ('log show --style syslog --debug --info --predicate \'process=="loginwindow"\' ')
        if time:
            str = str + "--last " + time
        else:
            str = str + "--last " + "1d"
        str = str + (" | grep LWDefaultScreenLockUI | grep -E \'CORRECT|INCORRECT\'")
        return GenericTool.runArbitraryCmd(str)

    def getKeychainAccessLog(start, end): #completed
        str = ('log show ')
        if start:
            str = str + ' --start "' + start
        if end:
            str = str + '" --end "' + end + '"'
        str = str + ' --predicate "subsystem==\'com.apple.securityd\' AND message CONTAINS[cd] \'Keychain Access\'" --info --debug --signpost --style compact'
        return GenericTool.runArbitraryCmd(str)

    def extractUserCookies(): #completed
        cookieloc = GenericTool.getConfigs("Configs/loc.json")['cookieloc']
        wOtherSess = GenericTool.runArbitraryCmd('zsh ' + ' Library/extract.sh ' + cookieloc)
        return wOtherSess

    def extractBilibiliCookies(input): #completed
        pattern = re.compile(r'^a?p?i?\.bilibili.com.*$', re.MULTILINE)
        results = pattern.findall(input)
        ret = ""
        for i in results:
            ret += i
            ret += '\n'
        sess = open("Configs/cookie.txt", "w")
        sess.write(ret)
        sess.close()

    def getBilibiliLoginHist(): #completed
        GenericTool.extractBilibiliCookies(GenericTool.extractUserCookies())
        result = GenericTool.runArbitraryCmd('curl -sS --cookie ' + "Configs/cookie.txt" + " " + "https://api.bilibili.com/x/member/web/login/log")
        return result

    def getBilibiliPlayHist(endTime): #completed
        GenericTool.extractBilibiliCookies(GenericTool.extractUserCookies())
        recs = []
        ts = int(datetime.now().timestamp())

        while ts > endTime:
            obj = GenericTool.runArbitraryCmd('curl -sS --cookie ' + "Configs/cookie.txt" + " " + "https://api.bilibili.com/x/web-interface/history/cursor?max=999&view_at={0}&business=".format(str(ts)))
            arr = jsonparser.loads(obj)['data']['list']
            recs.append(arr)
            ts = arr[-1]['view_at']

        cached = []
        for hist in recs[0]: #我也不知道这里为什么要这样子反正就离谱
            if hist['view_at'] >= endTime:
                cached.append(hist)
        print(cached)
        return cached

    def getTPKexts(): #completed
        return GenericTool.runArbitraryCmd('kextstat | grep -v com.apple')

    def getBrewList(): #completed
        str = GenericTool.runArbitraryCmd('brew list')
        m = str.split('\n')[:-1]
        print(m)
        out = ""
        for i in m:
            out += i
            out += ", "
        return out[:-2]

    def getAppList(): #completed
        return GenericTool.runArbitraryCmd('pkgutil --pkgs')
