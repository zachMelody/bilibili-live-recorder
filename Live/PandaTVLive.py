from .BaseLive import BaseLive
import time
import json


class PandaTVLive(BaseLive):
    def __init__(self, room_id):
        super().__init__()
        self.room_id = room_id
        self.site_name = 'Panda'
        self.site_domain = 'www.panda.tv'

    def get_room_info(self):
        url = 'http://www.panda.tv/api_room_v2'
        data = self.common_request('GET', url, {
            'roomid': self.room_id,
            '__plat': 'pc_web',
            '_': int(time.time())
        }).json()
        if data['errno'] == 0:
            return {
                'hostname': data['data']['hostinfo']['name'],
                'roomname': data['data']['roominfo']['name'],
                'site_name': self.site_name,
                'site_domain': self.site_domain,
                'status': data['data']['videoinfo']['status'] == '2'
            }

    def get_live_urls(self):
        url = 'http://www.panda.tv/api_room_v2'
        real_url = 'http://pl%s.live.panda.tv/live_panda/%s.flv?sign=%s&ts=%s&rid=%s'
        data = self.common_request('GET', url, {
            'roomid': self.room_id,
            '__plat': 'pc_web',
            '_': int(time.time())
        }).json()['data']
        room_key = data["videoinfo"]["room_key"]
        plflag = data['videoinfo']['plflag'].split('_')
        data2 = json.loads(data["videoinfo"]["plflag_list"])
        rid = data2["auth"]["rid"]
        sign = data2["auth"]["sign"]
        ts = data2["auth"]["time"]
        return [real_url % (plflag[1], room_key, sign, ts, rid)]
