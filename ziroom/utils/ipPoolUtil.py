# -*- coding: utf-8 -*
import requests


def getRandomIp():
    r = requests.get(
        "http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=077b741438554715a67b1776d9d2d14a&count=30&expiryDate=0&format=1&newLine=2").json()
    if r.get("code") == "0":
        for url in r.get("code"):
            port = url.get("port")
            ip = url.get("ip")
            print(ip + ":" + port);
    else:
        print(r)


def getIpFormSelfServer():
    r = requests.get("http://47.104.142.33:5010/get/")
    host = r.text
   # host = host.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=host)}
    res = requests.get('http://www.ziroom.com', proxies=proxies, timeout=0.5, verify=False)
    if res.status_code == 200:
        print("获取的免费代理:" + r.text)
        return "http://"+r.text
    else:
        requests.get("http://47.104.142.33:5010/delete?proxy=" + r.text)
        print("移除无效host:" + r.text)
        getIpFormSelfServer()
