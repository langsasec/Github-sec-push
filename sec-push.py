# -*- coding: UTF-8 -*-
# @Time:  20:45
# @Author: 浪飒
# @File: sec-push.py.py
# @Software: PyCharm

import json
import random
import time
from urllib.parse import quote
import requests


# 获取github信息,注意key为数组
def get_info(key):
    results = []
    req = f"https://api.github.com/search/repositories?q={key}&sort=updated"
    res = requests.get(req).content.decode("utf-8")
    dict_data = json.loads(res)  # json转成python字典
    time.sleep(5)  # 请求延迟
    for j in dict_data['items']:
        name = j['name']  # 获取到仓库名
        html_url = j['html_url']  # 获取到仓库链接
        desc = j['description']  # 获取到仓库描述
        results.append({"项目名称": name, "项目地址": html_url, "项目描述": desc})
        # 推送20条
        if results.__len__() > 20:
            break
    # 过滤项目
    black_list = ["反中共", "大陆修宪"]
    n_results = []
    for item in results:
        if black_list[0] in str(item.values()):
            continue
        elif black_list[1] in str(item.values()):
            continue
        else:
            n_results.append(item)
    results = n_results
    message = ''
    message1 = ''
    flag = 0
    for i in results:
        if i["项目描述"] is None:
            result = "【项目名称】:" + str(i["项目名称"]) + "\\n" + "【项目地址】:" + str(i["项目地址"]) + "\\n\\n"
        elif len(i["项目描述"]) > 50:
            result = "【项目名称】:" + str(i["项目名称"]) + "\\n" + "【项目地址】:" + str(i["项目地址"]) + "\\n" + "【项目描述】:" + i["项目描述"][:50] + "\\n\\n"
        else:
            result = "【项目名称】:" + str(i["项目名称"]) + "\\n" + "【项目地址】:" + str(i["项目地址"]) + "\\n" + "【项目描述】:" + i["项目描述"] + "\\n\\n"
        # 将20条分两次发
        flag = flag + 1
        if flag > 10:
            message1 = message1 + result
        else:
            message = message + result
    msg = [message, message1]
    return msg


# API推送
def push(message, token):
    # 发送post请求
    api = f"https://api.bot.wgpsec.org/push/{token}"
    headers = {
        'Connection': 'keep-alive',
        "Content-Length": '12802',
        "Accept": "*/*",
        'Cache-Control': 'max-age=0',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": "Windows",
        "Upgrade-Insecure-Requests": '1',
        "Origin": 'https://api.bot.wgpsec.org',
        "Content-Type": 'application/x-www-form-urlencoded',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    res = requests.post(url=api, data=message, headers=headers).content.decode("utf-8")
    # 获取响应内容
    print(res)


if __name__ == '__main__':
    keyword = ["CVE-2022", "CVE-2023", "渗透测试", "信息安全", "免杀", "域渗透", "Bypass Antivirus", "Exploit", "Hackone", "钓鱼",
               "社会工程学",
               "社工", "提权", "SQL注入", "POC", "蜜罐", "HVV", "白帽", "APT", "代码审计",
               "漏洞利用", "红队", "Red Team", "蓝队", "Blue Team", "红蓝对抗", "CTF", "计算机取证", "密码学", "Computer Forensics",
               "应急响应", "Emergency response", "Penetration", "Pentest", "内网渗透", "网络攻防",
               "网络安全", "主机安全", "信息收集", "溯源", "工控安全", "Industrial Control Safety", "云安全", "安全加固", "基线核查", "漏洞挖掘",
               "edusrc", "等级保护"]
    # API token
    token1 = ""
    token2 = ""
    while True:
        # 定时早晨时间9:59:59
        h1 = 10
        m1 = 0
        s1 = 0
        # 定时夜晚时间 19:59:59
        h2 = 20
        m2 = 0
        s2 = 0
        # 获取当前时间
        time_now_h = time.localtime()[3]
        time_now_m = time.localtime()[4]
        time_now_s = time.localtime()[5]
        if time_now_h == h1 and time_now_m == m1 and time_now_s >= s1:  # 早晨
            print('推送时间到了')
            # 随机选择关键字推送
            random_msg = get_info(keyword[random.randrange(0, len(keyword))])
            push("txt=" + quote(random_msg[0]), token1)
            time.sleep(2)
            push("txt=" + quote(random_msg[1]), token1)
            # 推送cve2022
            cve_msg = get_info(["CVE-2022"])
            push("txt=" + quote(cve_msg[0]), token2)
            time.sleep(2)
            push("txt=" + quote(cve_msg[1]), token2)
            # 打印推送时间
            info = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 早晨定时发送推送成功"
            print(info)
            time.sleep(60)  # 防止1秒内执行多次
        if time_now_h == h2 and time_now_m == m2 and time_now_s >= s2:  # 夜晚
            print('推送时间到了')
            # 随机选择关键字推送
            random_msg = get_info(keyword[random.randrange(0, len(keyword))])
            push("txt=" + quote(random_msg[0]), token1)
            time.sleep(2)
            push("txt=" + quote(random_msg[1]), token1)
            # 推送cve2023
            cve_msg = get_info(["CVE-2023"])
            push("txt=" + quote(cve_msg[0]), token2)
            time.sleep(2)
            push("txt=" + quote(cve_msg[1]), token2)
            # 打印推送时间
            info = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 夜晚定时发送推送成功"
            print(info)
            time.sleep(60)  # 防止1秒内执行多次
