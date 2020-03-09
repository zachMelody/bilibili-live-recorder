import time
import requests
import config


def get_current_time(time_format):
    current_struct_time = time.localtime(time.time())
    current_time = time.strftime(time_format, current_struct_time)
    return current_time


def generate_filename(room_id):
    data = dict()
    data['c_time'] = get_current_time('%Y%m%d_%H%M')
    data['room_id'] = room_id
    return '_'.join(data.values()) + '.flv'


def print_log(room_id='None', content='None'):
    brackets = '[{}]'
    time_part = brackets.format(get_current_time('%Y-%m-%d %H:%M:%S'))
    room_part = brackets.format('直播间: ' + room_id)
    print(time_part, room_part, content)


if __name__ == '__main__':
    print(generate_filename('1075'))
    print_log(content='开始录制')