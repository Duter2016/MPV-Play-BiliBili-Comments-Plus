# MPV-Play-BiliBili-Comments-Plus

只需要你有一个你要播放的B站视频地址即可！其他一概不要！

使用mpv自动下载弹幕并加载，不依赖Play-With-MPV，自动解析弹幕cid，并使用danmaku2ass下载xml弹幕文件、转为ass格式。

脚本修改自[MPV-Play-BiliBili-Comments](https://github.com/itKelis/MPV-Play-BiliBili-Comments)，并参考[《B站视频弹幕解析》](https://juejin.cn/post/7137928570080329741)。

## 1.加载原理

（1）当你复制视频地址后，插件启动GetBiliDanmuCID.py自动读取剪切板中视频地址，识别为B站视频后，自动提取视频弹幕cid；

（2）视频弹幕cid传递给插件，插件再启动Danmu2Ass.py自动完成下载xml字幕文件，并转换为.ass文件存放到指定目录；

（3）转换完成后，插件自动加载指定目录下的ass文件至播放视频。

## 2.linux系统下安装方法如下：

先安装一个python模块pyperclip（其他模块基本都是内置的，无需另外安装）：

`pip3 install pyperclip`

在[MPV-Play-BiliBili-Comments-Plus](https://github.com/Duter2016/MPV-Play-BiliBili-Comments-Plus)下载`scripts/bilibiliAssert`下面的三个脚本文件到mpv的配置目录`/home/<username>/.config/mpv/scripts/bilibiliAssert`，然后修改如下文件：

将`～/.config/mpv/scripts/bilibiliAssert/GetBiliDanmuCID.py`中如下代码中`dh`替换为你的`<pc username>`

`"/home/dh/.config/mpv/scripts/bilibiliAssert/bilicid"`

然后，命令别名 alias：

打开用户配置文件 `~/.bash_profile` ， 在文件最后添加如下 alias（注意是英文半角单引号，mpvb名字可以自定义）：

```
# 添加qt6的qdbus的PATH，否则klipper的qdbus通信失败
export PATH=$PATH:/usr/lib/qt6/bin

# mpv带弹幕播放在线视频
alias mpvb='mpv $(qdbus org.kde.klipper /klipper org.kde.klipper.klipper.getClipboardContents)'
```
上面剪贴板参数根据你使用的剪贴板工具，自己修改为以下可参考的对应参数：

* Plasma KDE桌面默认剪切板工具为`$(qdbus org.kde.klipper /klipper org.kde.klipper.klipper.getClipboardContents)`
* Parcellite 为 `$(parcellite --clipboard)`
* xclip 为 `$(xclip --clipboard)`
* xsel 为 `$(xsel --clipboard)`

保存后回到命令行执行以下命令使其生效：

`source ~/.bash_profile`

## 3.使用方法：

这里我们假设已经在网页复制了B站视频网址到剪贴板中，则在终端执行如下命令就可以立即播放了：

`mpvb`

或者用mpv原始的命令也可以：

`mpv <url>`

mpv播放后将会自动加载弹幕，按下按键`b`会重新载入弹幕,弹幕以字幕方式加载，如需隐藏按下`v`即可。如果希望更改快捷键，在main.lua中最后一行修改想要的快捷键。

## 4.为uosc添加memo菜单：

编辑`/home/<username>/.config/mpv/input.conf`文件，添加如下一行代码即可（点击左下角三道线即是）：

```
# script-binding reLoadDanmaku #! ReLoadDanmaku
```

## 5.已适配的B站网址格式：

> B站未再改变api接口前，如下格式是能正常解析的。

① 目前通用BV格式链接的视频，如：
```
https://www.bilibili.com/video/BV1ep4y177Qc/
https://www.bilibili.com/video/BV1ep4y177Qc/?spm_id_from=444.64.list.card_archive.click
https://www.bilibili.com/video/BV1ep4y177Qc?spm_id_from=444.64.list.card_archive.click
```
② 通过其他脚本获取BV格式转换获取的av格式链接的视频，如：
```
# 下面两个链接未同一个视频，链接做了转换
https://www.bilibili.com/video/BV1aM4y1c7bd/?spm_id_from=333.788&vd_source=af7cd9d6b2b43f4c2a37b41932d74844
https://www.bilibili.com/video/av934915881?
```
目前B站默认不显示av格式链接，虽然 b 站现在已经全面使用 BV 号来表示一个视频，但是 av 号依旧可以使用的，也许未来 av 可能会失效。

③ 暂不支持电视连续剧、番剧类ep（ep_id）、ss（season_id）视频播放，如：

mpv播放器原始不支持播放电视连续剧、番剧类ep（ep_id）、ss（season_id）视频链接的，如`https://www.bilibili.com/bangumi/play/ep409505?from_spmid=666.25.episode.0`或`https://www.bilibili.com/bangumi/play/ss21424?spm_id_from=..0.0`。

虽然电视连续剧、番剧类ep（ep_id）、ss（season_id）视频能通过api接口获取到其BV和av格式id，然后转换为相应链接。但是通过mpv播放时会被强制跳转到原ep、ss格式链接，从而播放失败。**虽然播放失败，但mpv可以通过本项目脚本用bv、av格式链接正确获取单集的弹幕cid**。如下列转换：

```
# ep链接转av
https://www.bilibili.com/bangumi/play/ep409505?from_spmid=666.25.episode.0
https://www.bilibili.com/video/av503892452

# ss链接转av
https://www.bilibili.com/bangumi/play/ss21424?spm_id_from=..0.0
https://www.bilibili.com/video/av336719734
```
ep（ep_id）、ss（season_id）视频链接的api提供的是整个剧集或番剧的全部信息（包括全部剧集的aid、bvid、cid），通过脚本提取cid,还需要另写py脚本，mpv不能播放视频也不用写了。api信息链接实例如下：
```
https://api.bilibili.com/pgc/view/web/season?ep_id=308352
https://api.bilibili.com/pgc/view/web/season?season_id=40260
https://api.bilibili.com/x/web-interface/view?bvid=BV1aM4y1c7bd
https://api.bilibili.com/x/web-interface/view?aid=934915881
```
参考：[《b站视频api归档》](https://www.hecady.com/b%E7%AB%99%E8%A7%86%E9%A2%91api%E5%BD%92%E6%A1%A3/)

④ 备用选择：播放连续剧、番剧类ep（ep_id）、ss（season_id）视频

安装调用MPV的[revda](https://github.com/THMonster/Revda)

revda也是调用的mpv,并且支持弹幕。只需要获取视频播放地址的代码就可以，当想要打开bilibili视频时，它支持av号、bv号、ep号、ss号，多p视频如果想通过av、bv号或者ss、ep号打开，请在编号后加上:n（n为视频p数）打开，例如：你想打开av123456的第三p，请输入av123456:3，bv号与ss号同理。。比如三国演义的播放地址为“`https://www.bilibili.com/bangumi/play/ep327612?from_spmid=666.25.episode.0&from_outer_spmid=..0.0`”，那么播放播放第三集代码就是“ep327612:3”。

详细使用方法见[Revda wiki](https://github.com/THMonster/Revda/wiki/1-%E5%9F%BA%E7%A1%80%E7%94%A8%E6%B3%95)

另外，安装revda时，同时安装了cli程序dmlive,这样也可以直接使用-u参数、后接https链接可播放该链接所指向的直播间或视频（**带B站弹幕，支持ss、ep号**）：

`dmlive -u <url>`

### 6.有问题可反馈
