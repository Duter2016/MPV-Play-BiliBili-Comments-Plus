#!/usr/bin/env python3
# 获取B站视频弹幕cid

import re
import requests
import pyperclip
import os
import argparse    # 从lua传入视频网址参数模块
#import browsercookie    # 使用cookie

"""
# 获取cookie，前提是需要浏览器登陆过
#find_cookie = browsercookie.chrome()
#find_cookie = browsercookie.chromium()
find_cookie = browsercookie.firefox()
#for cookie in find_cookie:
#    print(cookie)
"""

headers = {
    "authority": "api.bilibili.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "accept": "application/json, text/plain, */*",
}


# 读取从main.lua传输bilibili网址“videourl参数”(对应方法 1)
# 注意取消“import argparse”注释
parser = argparse.ArgumentParser()    # 创建解析对象
parser.add_argument('videourl', metavar=('VIDEOURL'), nargs='+', help=('Video url to grab cid'))    # 向该对象中添加你要关注的命令行参数和选项，B站视频url地址
args = parser.parse_args()    # 调用parse_args()方法进行解析
findvideourl = args.videourl    # 获得videourl在main.lua中参数值
getvideourl = findvideourl[0]
geturlgroup=['"',getvideourl,'"']


# 从剪切板读取bilibili网址(对应方法 2)
#urlfromclip = pyperclip.paste()    # 从剪切板读取bilibili网址
#geturlgroup=['"',urlfromclip,'"']


# 转化提取的bilibili网址为提取cid API可用的字符串
geturl=''.join(geturlgroup)    # 组合为可用的网址字符串
print(geturl)    # 测试网址正确性
url = str(geturl)


def get_real_url(url):
    r = requests.head(url, cookies=find_cookie, headers=headers)    # 不使用cookie
#    r = requests.head(url, cookies=find_cookie, headers=headers)    # 使用cookie
    return r.headers['Location']


# 截取BV或av号
def get_avbvid(url):
    if "b23.tv" in url:    # 哔哩哔哩短链
        url = get_real_url(url)
    url = url.strip("/")
    m_obj = re.search(r'[?&]p=(\d+)', url)    # 合集多p视频旧格式
    p = 0
    if m_obj:
        p = int(m_obj.group(1))
    strbv = "/BV"    # 适配bv视频API
    s_posbv = url.rfind(strbv) + 1
    s_posbvend = s_posbv + 12
    strav = "/av"    # 适配av视频API
    r_posav = url.rfind(strav) + 1
    r_posavend = r_posav + 11
    #s_pos = url.rfind("/") + 1
    #r_pos = url.rfind("?")
    avbvid = None
    if r_posav == 0:
        avbvid = url[s_posbv:s_posbvend]
    else:
        avbvid = url[r_posav:r_posavend]
    #if r_pos == -1:
    #    avbvid = url[s_pos:]
    #else:
    #    avbvid = url[s_pos:r_pos]
    if avbvid.startswith("av"):
        return "aid", avbvid[2:], p
    elif avbvid.startswith("BV"):
        return "bvid", avbvid, p
    else:
        return None
    #print(url.strip().split('/'))
    #print(s_posbv)
    #print(s_posbvend)
    #print(r_posav)
    #print(r_posavend)
    #print(s_pos)
    #print(r_pos)
    #print(avbvid)


# 定义获取弹幕cid
def get_cid(url, all_cid=False):
    if get_avbvid(url) != None:
        # 如果成功获取到BV或av号，爬取cid号
        t, avbvid, p = get_avbvid(url)
        #print(t, avbvid, p)
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
    else:
        # 如果不能获取到BV或av号，返回空值
        return None


# 如果获取到弹幕cid，将弹幕cid写入文件bilicid
if get_cid(url) != None:
    title, cid = get_cid(url)
    print(title, cid)
    cid_str = str(cid)
    print("弹幕CID:",str(cid))
    file = open("/home/dh/.config/mpv/scripts/bilibiliAssert/bilicid", 'w')
    file.write(cid_str)
    file.close()
    print("已生成弹幕cid文件bilicid")
else:
    # 如果获取不到弹幕cid，删除旧文件bilicid
    if(os.path.isfile("/home/dh/.config/mpv/scripts/bilibiliAssert/bilicid")):
        os.remove("/home/dh/.config/mpv/scripts/bilibiliAssert/bilicid")
        print("无用弹幕cid文件bilicid已删除")
    else:
        print("不存在无用弹幕cid文件bilicid")
    # 如果获取不到弹幕cid，删除旧弹幕文件bilibili.ass
    if(os.path.isfile("/home/dh/.config/mpv/scripts/bilibiliAssert/bilibili.ass")):
        os.remove("/home/dh/.config/mpv/scripts/bilibiliAssert/bilibili.ass")
        print("无用弹幕文件bilibili.ass已删除")
    else:
        print("不存在无用弹幕bilibili.ass")


