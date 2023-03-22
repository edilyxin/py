#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os, platform
import shutil
from datetime import datetime, timezone, timedelta
import get_ip_utils

# 需要获取ip的网址
sites = ["github.global.ssl.fastly.net", "assets-cdn.github.com", "github.com"]

addr2ip = {}
hostLocation = r'./hosts'
global systemHostLocation
systemHostLocation = ''


def initParams():
    global systemHostLocation
    match platform.system():
        case "Windows":
            systemHostLocation = 'C:\\Windows\\System32\\drivers\\etc\\'
        case "Linux":
            systemHostLocation = '/etc/'
        case "Darwin":  # Mac Os
            systemHostLocation = '/etc/'
        case _:
            raise RuntimeError("Unknown operating system")
    # prepare file
    shutil.copy(systemHostLocation + 'hosts', hostLocation)  # 获取系统的 hosts 文件最新副本
    print(systemHostLocation)
    print(hostLocation)
    print('init finish')


def changeHostFile():
    # 删除 旧 bak 文件
    if os.path.exists(systemHostLocation + 'hosts.bak'):
        os.remove(systemHostLocation + 'hosts.bak')
    os.renames(systemHostLocation + 'hosts', systemHostLocation + 'hosts.bak')
    shutil.move('./hosts', systemHostLocation + 'hosts')  # 生成的最新 hosts 文件放到系统文件夹中,让其生效
    match platform.system():
        case "Windows":
            os.system("ipconfig /flushdns")
        case "Linux":
            pass
        case "Java":
            pass
        case "Darwin":  # Mac Os
            os.system("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder")
        case _:
            raise RuntimeError("Unknown operating system")


def dropDuplication(line):
    flag = False
    if "#*******" in line:
        return True
    for site in sites:
        if site in line:
            flag = flag or True
        else:
            flag = flag or False
    return flag


# 更新host, 并刷新本地DNS
def updateHost():
    # today = datetime.date.today()
    # rs = DNS.dnslookup('github.global.ssl.fastly.net', qtype='A')
    # print(rs)

    update_time = (
        datetime.utcnow()
        .astimezone(timezone(timedelta(hours=8)))
        .replace(microsecond=0)
        .isoformat()
    )
    try:
        for site in sites:
            # trueIp is list
            trueIp = get_ip_utils.getIpFromIp138(site)
            if len(trueIp) > 0:
                addr2ip[site] = trueIp
                print(site + "\t" + ','.join(trueIp))
            # if platform.system() == 'Windows':
            #     systemHostLocation = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
            #     shutil.copyfile(systemHostLocation, hostLocation)
            with open(hostLocation, "r", encoding='utf8') as f1:
                f1_lines = f1.readlines()
                with open("tempHost", "w", encoding='utf8') as f2:
                    for line in f1_lines:  # 为了防止 host 越写用越长，需要删除之前更新的含有github相关内容
                        if dropDuplication(line) is False:
                            f2.write(line)
                    f2.write("#**********github " + update_time + " update **********\n")
                    for key in addr2ip:
                        if len(addr2ip[key]) >= 1:  # 解决一个site有多个ip的情况
                            for lineStr in addr2ip[key]:
                                f2.write(lineStr + "\t" + key + "\n")
                    f2.write("#******* github hosts update end **********\n")
        os.remove(hostLocation)
        os.rename("temphost", hostLocation)
        print('file update finish')
    except Exception as e:
        print("runtime err :" + str(e))
    else:
        changeHostFile()


if __name__ == "__main__":
    initParams()
    updateHost()
    print('update success')

# Todo 根据不同的系统自动跟新host文件，需要搞明白什么是nds污染
