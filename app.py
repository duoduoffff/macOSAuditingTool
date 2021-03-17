#! /usr/bin/python3
# -*- coding: utf-8 -*-

from Library import toolFunctions as functions
from datetime import date, timedelta
import fe
import argparse
import subprocess


helptext = "Command line tool to audit your macOS device, printing results on paper for archiving."
version = "0.9"

print('调试信息')
print('======================')

def yesterday():
    yesterday = date.today() - timedelta(days=1)
    return str(yesterday.strftime("%Y-%m-%d"))

today = str(date.today().strftime("%Y-%m-%d"))

parser = argparse.ArgumentParser(description = helptext)
parser.add_argument("-v", "--version", help = "Show program version.", action = "store_true")
parser.add_argument("-p", "--print", help = "Print on paper. If there\'s no such argument, print to stdout.", action = "store_true")
parser.add_argument("-s", "--keychain-start", help = "Specify keychain log start time. '2021-03-14' for instance.", default = yesterday())
parser.add_argument("-e", "--keychain-end", help = "Specify keychain log end time. '2021-03-15 for instance.'", default = today)
parser.add_argument("-b", "--bili-hist-amount", help = "Specify the range of bilibili history logs you would like to see. Defaults to yesterday. Supply format: '2021-03-14', for instance.", nargs = "?", default = yesterday())
parser.add_argument("-u", "--login-hist-amount", help = "Specify how many lines of login history you would like to see. Defaults to output everything.")
parser.add_argument("-r", "--login-hist-user", help = "Specify which user of login history you would like to see. Defaults to the current user acct.", nargs = "?")
parser.add_argument("-n", "--sudo-hist-amount", help = "Specify how long sudo history you would like to see. Defaults to 1d.", nargs = "?", default = "1d")
parser.add_argument("-l", "--lock-hist-amount", help = "Specify how long lock and unlock history you would like to see. Defaults to 1d.", nargs = "?", default = "1d")

arguments = parser.parse_args()

if arguments.version:
    print(version)

def prepareContent(start, end, bilihistamt, loginhistamt, loginhistuser, sudohistamt, lockhistamt):
    time = fe.printTime()
    keyDirs = functions.GenericTool.getConfigs("./Configs/loc.json")['locations']
    keyFiles = functions.GenericTool.getConfigs("./Configs/loc.json")['keyfiles']


    finalctt = ""

    finalctt += "macOS 审计日结系统\n"
    finalctt += "==================================\n"
    finalctt += "打印时间：{0}\n".format(time)
    finalctt += fe.getKeyLocationsInfo(keyDirs)
    finalctt += fe.getFileStats(keyFiles)
    finalctt += fe.getiCloudState()
    finalctt += fe.getLocksUnlocksStt(lockhistamt)
    finalctt += fe.getElevationStt(sudohistamt)
    finalctt += fe.getLoginLog(loginhistamt, loginhistuser)
    finalctt += fe.getKeychainAccessStt(start, end)
    finalctt += fe.bilibiliLoginHist()
    finalctt += fe.bilibiliPlayHist(bilihistamt)
    finalctt += fe.getTPExt()
    finalctt += fe.getBrewListStt()
    finalctt += fe.getAppListStt()

    finalctt += "\n已到底部\n"
    finalctt += "打印时间：{0}\n".format(time)

    return finalctt

final = prepareContent(arguments.keychain_start, arguments.keychain_end, arguments.bili_hist_amount, arguments.login_hist_amount, arguments.login_hist_user, arguments.sudo_hist_amount, arguments.lock_hist_amount)


def printOnPaper(content):
    lpr = subprocess.Popen('/usr/bin/lpr', stdin=subprocess.PIPE)
    lpr.stdin.write(str.encode(content))

if arguments.print:
    printOnPaper(final)
else:
    print(final)
