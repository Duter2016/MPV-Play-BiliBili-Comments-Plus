-- bilibiliAssert: 播放 B 站视频时自动加载弹幕字幕
-- 依赖同目录 GetBiliDanmuCID.py、Danmu2Ass.py

local function log(msg, secs)
	mp.msg.warn(msg)
	mp.osd_message(msg, secs or 2.5)
end

local function run(args)
	return mp.command_native({
		name = 'subprocess',
		playback_only = false,
		capture_stdout = true,
		capture_stderr = true,
		args = args,
	})
end

local function assprocess()
	local d = mp.get_script_directory()
	local url = mp.get_property('playlist/0/filename') or ''
	if not (url:find('bilibili%.com') or url:find('b23%.tv')) then return end

	-- 1. 取弹幕 cid（同步执行，失败就不用旧 cid）
	local r1 = run({ 'python', d .. '/GetBiliDanmuCID.py', url })
	local f = io.open(d .. '/bilicid', 'r')
	local cid = f and f:read('*all') or nil
	if f then f:close() end
	if r1.status ~= 0 or not cid or cid == '' then
		log('取弹幕 cid 失败: ' .. tostring(r1.stderr), 8)
		return
	end

	-- 2. 转成 ass
	log('弹幕正在上膛')
	local r2 = run({ 'python', d .. '/Danmu2Ass.py', '-d', d,
		'-s', '1920x1080',
		'-fs', '50.0',
		'-a', '0.70',
		'-dm', '10.0',
		'-ds', '5.0',
		'-p', '0',
		'-r', cid })
	if r2.status ~= 0 then
		log('弹幕转换失败: ' .. tostring(r2.stderr), 8)
		return
	end

	-- 3. 直接加载，不依赖文件名匹配
	mp.commandv('sub-add', d .. '/bilibili.ass', 'select')
	log('开火')
end

mp.add_key_binding('b', 'reLoadDanmaku', assprocess)
mp.register_event('start-file', assprocess)
