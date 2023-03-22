import requests
import time
from bs4 import BeautifulSoup
import re
import json

# import DNS  https://www.cnblogs.com/willison/p/13830967.html


def getIpFromIpaddress(site):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'www.ipaddress.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://www.ipaddress.com/',
        'Connection': 'keep-alive'
    }
    url = "https://ipaddress.com/site/" + site
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", res.text)
        result = soup.find_all('div', class_="comma-separated")
        for c in result:
            if len(ip) != 0:
                trueip = ip[0]
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
    return trueip


def getIpFromIp138(site):
    # 从 site.ip138.com 查询ip
    # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'site.ip138.com',
        'Connection': 'keep-alive',
        'Referer': 'https://site.ip138.com/%s/' % (site),
    }
    url = (
        "https://site.ip138.com/domain/read.do?domain="
        + site.lower()
        + "&time="
        + str(time.time())
    )
    trueip = []
    try:
        res = requests.get(url, headers=headers, timeout=5, data={})
        if res.status_code == 200:
            soup = json.loads(res.text)
            ips = soup['data']  # type: ignore
            for ip in ips:
                trueip.append(ip['ip'])
            return trueip
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
        raise e
    return trueip


def getIpFromChinaz(site):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
        'Host': 'ip.tool.chinaz.com',
    }
    url = "http://ip.tool.chinaz.com/" + site
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all('span', class_="Whwtdhalf w15-0")
        for c in result:
            ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", c.text)
            if len(ip) != 0:
                trueip = ip[0]
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
    return trueip


def getIpFromWhatismyipaddress(site):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
        'Host': 'ip.tool.chinaz.com',
    }
    url = "https://whatismyipaddress.com//hostname-ip"
    data = {"DOMAINNAME": site, "Lookup IP Address": "Lookup IP Address"}
    trueip = None
    try:
        res = requests.post(url, headers=headers, data=data, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all('span', class_="Whwtdhalf w15-0")
        for c in result:
            ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", c.text)
            if len(ip) != 0:
                trueip = ip[0]
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
    return trueip


def getIpFromipapi(site):
    '''
    return trueip: None or ip
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
        'Host': 'ip-api.com',
    }
    url = "http://ip-api.com/json/%s?lang=zh-CN" % (site)
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res = json.loads(res.text)
        if res["status"] == "success":
            trueip = res["query"]
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
    return trueip


# def getTrueIp(site):
#     url = site
#     trueip = None
#     try:
#         res = DNS.dnslookup(url, qtype='A')  # convenience routine to return just answer data for any query type
#         if len(res) != 0:
#             trueip = res
#     except Exception as e:
#         print("query ip error is " + str(e))
#     return trueip


print(getIpFromIpaddress('github.global.ssl.fastly.net'))
