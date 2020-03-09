# bilibili_live_recorder
下载 bilibili 直播 视频流  

forked from [zachMelody/bilibili-live-recorder](https://github.com/zachMelody/bilibili-live-recorder)

## Usage:

### cli 模式（仅支持单直播间）：
<code>python run.py [room_id]</code>  
- room_id: 直播间id

### config.py 模式（支持多直播间）：
1. 打开 <code>config.py</code> 
1. 修改 <code>rooms</code> (list)
    - 例如 rooms = ['1075', '547028', '8694442']
## Example：
<code>python run.py 1075</code>