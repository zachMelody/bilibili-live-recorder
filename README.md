# bilibili_live_recorder
下载 bilibili 直播 视频流  

forked from [zachMelody/bilibili-live-recorder](https://github.com/zachMelody/bilibili-live-recorder)

## Usage:

### 单直播间模式：
<code>python run.py [room_id]</code>  
- room_id: 直播间id

### 多直播间模式：
1. 打开 <code>config.py</code> 
1. 修改 <code>rooms</code> (list)
    - 例如 rooms = ['1075', '547028', '8694442']
## Example：
<code>python run.py 1075</code>