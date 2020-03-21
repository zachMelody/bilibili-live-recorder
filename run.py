#!/usr/bin/env python3
import random
from Live import BiliBiliLive
import os
import sys
import requests
import time
import config
import utils
import re
import multiprocessing
import urllib3
import env_lang
urllib3.disable_warnings()


class BiliBiliLiveRecorder(BiliBiliLive):
    def __init__(self, room_id, check_interval=5*60):
        super().__init__(room_id)
        self.inform = utils.inform
        self.print = utils.print_log
        self.check_interval = check_interval

    def check(self, interval):
        while True:
            room_info = self.get_room_info()
            try:
                if room_info['status']:
                    self.inform(room_id=self.room_id,
                                desp=room_info['roomname'])
                    self.print(self.room_id, room_info['roomname'])
                    break
                else:
                    self.print(self.room_id, env_lang.get("msg.waiting"))
            except Exception as e:
                self.print(self.room_id, 'Error:' + str(e))
            time.sleep(interval*(1+random.random()))
        return self.get_live_urls()

    def record(self, record_url, output_filename):
        self.print(self.room_id, env_lang.get("msg.recording") + self.room_id)
        try:
            headers = dict()
            headers['Accept-Encoding'] = 'identity'
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
            headers['Referer'] = re.findall(
                r'(https://.*\/).*\.flv', record_url)[0]
            resp = requests.get(record_url, stream=True, headers=headers)
            with open(output_filename, "wb") as f:
                for chunk in resp.iter_content(chunk_size=512):
                    f.write(chunk) if chunk else None
        except Exception as e:
            self.print(self.room_id, 'Error while recording:' + str(e))

    def run(self):
        while True:
            try:
                urls = self.check(interval=config.check_interval)
                filename = utils.generate_filename(self.room_id)
                c_directory = os.path.join(os.getcwd(), 'files')
                if not os.path.exists(c_directory):
                    os.makedirs(c_directory)
                c_filename = os.path.join(c_directory, filename)
                self.record(urls[0], c_filename)
                self.print(self.room_id, env_lang.get("msg.finish"))
            except Exception as e:
                self.print(
                    self.room_id, 'Error while checking or recording:' + str(e))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_id = [str(sys.argv[1])]
    elif len(sys.argv) == 1:
        input_id = config.rooms  # input_id = '917766' '1075'
    else:
        raise ZeroDivisionError(env_lang.get("parameter_error"))

    mp = multiprocessing.Process
    tasks = [mp(target=BiliBiliLiveRecorder(room_id).run)
             for room_id in input_id]
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()
