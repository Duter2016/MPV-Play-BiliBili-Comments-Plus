-- assert lua script
-- ===================|
-- note to escape path for winodws (c:\\users\\user\\...)

-- 【 备用】：
    -- 在lua中运行 python 脚本，不带lua传递参数videourl
    --mp.commandv("run", "python3", py_path_cid)

local utils = require 'mp.utils'

-- Log function: log to both terminal and MPV OSD (On-Screen Display)
function log(string,secs)
	secs = secs or 2.5
	mp.msg.warn(string)
	mp.osd_message(string,secs)
end


-- get cid by read file "bilicid"
function ingest(file)
	-- 【第一步】运行 "GetBiliDanmuCID.py"
	-- 【(方法 1)】
	-- 通过mpv自带参数从“mpv <video url>“提取url
	local videourl = mp.get_property('playlist/0/filename')
	  --以下命令也可以通过mpv自带参数从“mpv <video url>“提取url
	--local videourl = mp.get_property('stream-open-filename')
	print('Video URl:', videourl)

	local python_path = 'python' -- path to python bin
	-- get script directory 
	local directory = mp.get_script_directory()
	local py_path_cid = ''..directory..'/GetBiliDanmuCID.py'
	-- under windows platform, convert path format
	if string.find(directory, "\\")
	then
		string.gsub(directory, "/", "\\")
		py_path_cid = ''..directory..'\\GetBiliDanmuCID.py'
	end

	-- 在lua中运行 python 脚本，带lua传递参数videourl
	local argurl = { 'python', py_path_cid, videourl,}
	--log('即将运行GetBiliDanmuCID.py')
	-- run python to get comments
	mp.command_native_async({
		name = 'subprocess',
		playback_only = false,
		capture_stdout = true,
		args = argurl,
		capture_stdout = true
	})

	-- 等待3秒钟，生成bilicid文件，再继续运行
	function sleep(n)
	   os.execute("sleep " .. n)
	end
	sleep(3)

	-- 【(方法 2)】
	-- 使用此方法，不用设置等待，但需“GetBiliDanmuCID.py“采用读取剪切板
	--os.execute('python ~/.config/mpv/scripts/bilibiliAssert/GetBiliDanmuCID.py')


    -- 【第二步】定义从“bilicid”文件读取cid功能
    local f = io.open(file, "r")
    if f then
        local lines = f:read("*all")
        f:close()
        return(lines)
    else
        print("未获取bili视频弹幕cid")
    end
end


-- download/load function
function assprocess()
	-- 【第三步】执行“ingest(file)”读取cid
	-- get bilicid file directory 
	local directory = mp.get_script_directory()
	local py_path_bilicid = ''..directory..'/bilicid'
	-- under windows platform, convert path format
	if string.find(directory, "\\")
	then
		string.gsub(directory, "/", "\\")
		py_path_bilicid = ''..directory..'\\bilicid'
	end
	-- start execute the function to read file "bilicid"
	bilicidnum=ingest(py_path_bilicid)
	--print(bilicidnum)

	-- get video cid
	local cid = bilicidnum
	-- get video cid from mpv by using "play-with-mpv"
	--local cid = mp.get_opt('cid')
	if (cid == nil)
	then
		return
	end
	
	-- 【第四步】进行弹幕xml 2 ass转码
	local python_path = 'python' -- path to python bin

	-- get script directory 
	local directory = mp.get_script_directory()
	local py_path = ''..directory..'/Danmu2Ass.py'

	-- under windows platform, convert path format
	if string.find(directory, "\\")
	then
		string.gsub(directory, "/", "\\")
		py_path = ''..directory..'\\Danmu2Ass.py'
	end
	
	-- choose to use python or .exe
	local arg = { 'python', py_path, '-d', directory, 
	-- 设置屏幕分辨率 （默认 1920x1080)
	'-s', '1920x1080',
	-- 设置字体大小    (默认 37.0)
	'-fs',  '50.0',
	-- 设置弹幕不透明度 (默认 0.95)
	'-a', '0.70',
	-- 滚动弹幕显示的持续时间 (默认 10秒)
	'-dm', '10.0',
	-- 静止弹幕显示的持续时间 (默认 5秒)
	'-ds', '5.0',
	-- 保留底部多少高度的空白区域 (默认　０, 取值0.0-1.0)
	'-p', '0',
	'-r',
	cid,
}
	-- local arg = { ''..directory..'\\Danmu2Ass.exe', '-d', directory, cid}
	log('弹幕正在上膛')
	-- run python to get comments
	mp.command_native_async({
		name = 'subprocess',
		playback_only = false,
		capture_stdout = true,
		args = arg,
		capture_stdout = true
	},function(res, val, err)
		if err == nil
		then
			log('开火')
			mp.set_property_native("options/sub-file-paths", directory)
			mp.set_property('sub-auto', 'all')
			mp.command('sub-reload')
			mp.commandv('rescan_external_files','reselect')
		else
			log(err)
		end
	end)

end

-- 设置按快捷键“b”重新载入弹幕
mp.add_key_binding('b', 'reLoadDanmaku', assprocess)
mp.register_event("start-file", assprocess)