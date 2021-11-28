import time
import requests
import config
import os

inform_url = 'https://sctapi.ftqq.com/' + config.send_key + '.send'


def get_current_time(time_format):
    current_struct_time = time.localtime(time.time())
    current_time = time.strftime(time_format, current_struct_time)
    return current_time


def generate_filename(room_id):
    data = dict()
    data['c_time'] = get_current_time('%Y%m%d_%H%M')
    data['room_id'] = room_id
    return '_'.join(data.values()) + '.flv'


def inform(room_id, desp=''):
    if config.enable_inform:
        param = {
            'title': '直播间：{} 开始直播啦！'.format(room_id),
            'desp': desp,
        }
        resp = requests.get(url=inform_url, params=param, verify=False, proxies={"http": None, "https": None})
        print_log(room_id=room_id, content='通知完成！') if resp.status_code == 200 else None
    else:
        pass


def print_log(room_id='None', content='None'):
    brackets = '[{}]'
    time_part = brackets.format(get_current_time('%Y-%m-%d %H:%M:%S'))
    room_part = brackets.format('直播间: ' + room_id)
    print(time_part, room_part, content)


def checkRecordDirExisted():
    dirs = os.path.join(os.getcwd(), 'files')
    if not os.path.exists(dirs):
        os.mkdir(dirs)


if __name__ == '__main__':
    print(generate_filename('1075'))
    print_log(content='开始录制')
