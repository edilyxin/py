#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os, platform
import shutil
from datetime import datetime, timezone, timedelta
import get_ip_utils

# 需要获取ip的网址
sites = ["github.global.ssl.fastly.net", "assets-cdn.github.com", "github.com"]

addr2ip = {}
hostLocation = r"./hosts"
systemHostLocation = None


def changeHostFile():
    match platform.system():
        case "Windows":
            systemHostLocation = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
            os.remove(systemHostLocation + '.bak')
            os.renames(systemHostLocation, systemHostLocation + '.bak')
            shutil.copy(hostLocation, 'C:\\Windows\\System32\\drivers\\etc\\')
            os.system("ipconfig /flushdns")
        case "Linux":
            systemHostLocation = '/etc/hosts'
        case "Java":
            systemHostLocation = '/root/hosts'
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
    for site in sites:
        # trueIp is list
        trueIp = get_ip_utils.getIpFromIp138(site)
        if len(trueIp) > 0:
            addr2ip[site] = trueIp
            print(site + "\t" + ','.join(trueIp))
        if platform.system() == 'Windows':
            systemHostLocation = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
            shutil.copyfile(systemHostLocation, hostLocation)
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
    changeHostFile()


if __name__ == "__main__":
    updateHost()
    print('update success')

# Todo 根据不同的系统自动跟新host文件，需要搞明白什么是nds污染
