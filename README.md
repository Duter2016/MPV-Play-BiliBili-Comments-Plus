# MPV-Play-BiliBili-Comments-Plus

使用mpv自动下载弹幕并加载，不依赖Play-With-MPV，自动解析弹幕cid

脚本修改自[MPV-Play-BiliBili-Comments](https://github.com/itKelis/MPV-Play-BiliBili-Comments)，并参考[《B站视频弹幕解析》](https://juejin.cn/post/7137928570080329741)。

## linux系统下安装方法如下：

先安装一个python模块pyperclip（其他模块基本都是内置的，无需另外安装）：

`pip3 install pyperclip`

在[MPV-Play-BiliBili-Comments-Plus](https://github.com/Duter2016/MPV-Play-BiliBili-Comments-Plus)下载`scripts/bilibiliAssert`下面的三个脚本文件到mpv的配置目录`/home/<username>/.config/mpv/scripts/bilibiliAssert`，然后修改如下两个文件：

（1）将`～/.config/mpv/scripts/bilibiliAssert/main.lua`中如下代码中`dh`替换为你的`<pc username>`

`bilicidnum=ingest("/home/dh/.config/mpv/scripts/bilibiliAssert/bilicid")`

（2）将`～/.config/mpv/scripts/bilibiliAssert/GetBiliDanmuCID.py`中如下代码中`dh`替换为你的`<pc username>`

`file = open("/home/dh/.config/mpv/scripts/bilibiliAssert/bilicid", 'w')`

然后，命令别名 alias：

打开用户配置文件 `~/.bash_profile` ， 在文件最后添加如下 alias（注意是英文半角单引号，mpvb名字可以自定义）：

```
# mpv带弹幕播放在线视频
alias mpvb='python /home/dh/.config/mpv/scripts/bilibiliAssert/GetBiliDanmuCID.py && mpv $(qdbus org.kde.klipper /klipper org.kde.klipper.klipper.getClipboardContents)'
```
上面剪贴板参数根据你使用的剪贴板工具，自己修改为以下可参考的对应参数：

* Plasma KDE桌面默认剪切板工具为`$(qdbus org.kde.klipper /klipper org.kde.klipper.klipper.getClipboardContents)`
* Parcellite 为 `$(parcellite --clipboard)`
* xclip 为 `$(xclip --clipboard)`
* xsel 为 `$(xsel --clipboard)`

保存后回到命令行执行以下命令使其生效：

`source ~/.bash_profile`

## 使用方法：

这里我们假设已经在网页复制了B站视频网址到剪贴板中，则在终端执行如下命令就可以立即播放了：

`mpvb`

mpv播放后将会自动加载弹幕，按下按键`b`会重新载入弹幕,弹幕以字幕方式加载，如需隐藏按下`v`即可。如果希望更改快捷键，在main.lua中最后一行修改想要的快捷键。

## 一个问题

想把GetBiliDanmuCID.py脚本加载进main.lua中加载，但是尝试多种方式都不加载GetBiliDanmuCID.py。有尝试成功的，欢迎修改。
