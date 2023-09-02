#!/usr/bin/env python3

import re
import requests
import pyperclip

headers = {
    "authority": "api.bilibili.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "accept": "application/json, text/plain, */*",
}


def get_real_url(url):
    r = requests.head(url, headers=headers)
    return r.headers['Location']


def get_avbvid(url):
    if "b23.tv" in url:
        url = get_real_url(url)
    url = url.strip("/")
    m_obj = re.search("[?&]p=(\d+)", url)
    p = 0
    if m_obj:
        p = int(m_obj.group(1))
    s_pos = url.rfind("/") + 1
    r_pos = url.rfind("?")
    avbvid = None
    if r_pos == -1:
        avbvid = url[s_pos:]
    else:
        avbvid = url[s_pos:r_pos]
    if avbvid.startswith("av"):
        return "aid", avbvid[2:], p
    else:
        return "bvid", avbvid, p


def get_cid(url, all_cid=False):
    t, avbvid, p = get_avbvid(url)
    res = requests.get(
        f"https://api.bilibili.com/x/web-interface/view?{t}={avbvid}", headers=headers)
    res.encoding = "u8"
    data = res.json()['data']
    cids = {row["page"]: (row['part'], row["cid"]) for row in data["pages"]}
    if all_cid:
        return cids
    elif p == 0:
        return data["title"], data["cid"]
    else:
        return cids[p]


urlfromclip = pyperclip.paste()    # 从剪切板读取bilibili网址
geturlgroup=['"',urlfromclip,'"']
geturl=''.join(geturlgroup)    # 组合为可用的网址字符串
print(geturl)    # 测试网址正确性
url = str(geturl)
title, cid = get_cid(url)
print(title, cid)
cid_str = str(cid)
print("弹幕CID:",str(cid))


file = open("/home/dh/.config/mpv/scripts/bilibiliAssert/bilicid", 'w')
file.write(str(cid))
file.close()


dl_getcid = get_cid(url, all_cid=False)
dl_getcid