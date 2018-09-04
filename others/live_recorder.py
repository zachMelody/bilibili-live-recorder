from pprint import pprint
import os
import ffmpy
import requests_html
import urllib3
import arrow
from Live import BilibiliLive

urllib3.disable_warnings()


class BilibiliLiveRecorder:
    def __init__(self, cid, output_name='opt.mp4'):
        self.cid = cid
        self.api_url = 'http://api.live.bilibili.com/api/playurl?device=phone&platform=ios&scale=3&build=10000&' \
                       'cid={}&otype=json&platform=h5'.format(cid)
        self.output_dir = os.path.join(os.getcwd(), 'files')
        self._s = requests_html.HTMLSession()

    def get_live_url(self):
        resp = self._s.get(self.api_url, verify=False)
        try:
            live_url = resp.json()['data']
            print(live_url)
        except Exception as e:
            raise ZeroDivisionError('无法获取直播流地址')
        return live_url

    def download(self, download_url, time):
        output_name = self.cid + '_' + str(time) + '.mp4'
        output = os.path.join(self.output_dir, output_name)

        ffmpeg_cmd = ffmpy.FFmpeg(
            r'C:\Program Files (x86)\ffmpeg-4.0.2\bin\ffmpeg.exe',
            '-t 0:01:15',
            inputs={download_url: None},
            outputs={output: None}
        )

        print('Start downloading and merging with ffmpeg...')
        print(ffmpeg_cmd.cmd)

        ffmpeg_cmd.run()


# bili = BilibiliLiveRecorder('3683436')
# time = 1
# while True:
#     bili.download(download_url=bili.get_live_url(), time=time)
#     print('Current Time: ' + str(time))
#     time += 1

if __name__ == '__main__':
    # bili = BilibiliLiveRecorder('1075')
    # url = bili.get_live_url()

    urls = BilibiliLive.BiliBiliLive('917766').get_live_urls()
    url = urls[0]
    url.replace('\&', '\"\&\"')
    print(url)
    url = 'https://js.live-play.acgvideo.com/live-js/119215/live_275085_7352366.flv?wsSecret=427f1f841effa597c884449de4ef536f&wsTime=1535892593'
    # -*- coding: utf-8 -*-
    import subprocess
    import time, signal

    # def exit():
    #     global child
    #     print('You choose to stop me.')
    #     child.send_signal(1)
    #
    #
    # signal.signal(signal.SIGINT, exit)
    # signal.signal(signal.SIGBREAK, exit)
    # signal.signal(signal.SIGTERM, exit)

    strcmd = "ffmpeg -y -i {} D:\1075\wis.flv".format(url)
    print(strcmd)
    child = subprocess.Popen(['ffmpeg', '-y', '-i', url, r'D:\1075\wis1.flv'], shell=True)
    child.wait()

