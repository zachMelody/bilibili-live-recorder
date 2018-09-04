from Live import BiliBiliLive
import os, sys
import requests
import time
import config


class BiliBiliLiveRecorder(BiliBiliLive):
    def __init__(self, room_id):
        super().__init__(room_id)
        self.inform_url = config.inform_url

    def check(self, interval):
        while True:
            room_info = self.get_room_info()
            if room_info['status']:
                self.inform(desp=room_info['roomname'])
                break
            else:
                print('等待开播')
            time.sleep(interval)
        return self.get_live_urls()

    @staticmethod
    def record(record_url, output_filename):
        print('√ 正在录制...')
        resp = requests.get(record_url, stream=True)
        with open(output_filename, "wb") as f:
            for chunk in resp.iter_content(chunk_size=512):
                f.write(chunk) if chunk else None

    def inform(self, desp=''):
        param = {
            'text': '直播间：{} 开始直播啦！'.format(self.room_id),
            'desp': desp,
        }
        resp = requests.get(url=self.inform_url, params=param)
        print('通知完成！') if resp.status_code == 200 else None


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2:
        input_id = str(sys.argv[1])
    elif len(sys.argv) == 1:
        input_id = '8051233'
    else:
        raise ZeroDivisionError('请检查输入的命令是否正确 例如：python3 run.py 10086')

    recorder = BiliBiliLiveRecorder(input_id)
    urls = recorder.check(interval=5*60)
    filename = os.path.join(os.getcwd(), 'files', 'opt.flv')
    recorder.record(urls[0], filename)
