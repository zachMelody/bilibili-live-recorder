import base64
import json
from .BaseLive import BaseLive


class ZhanqiLive(BaseLive):
    def __init__(self, room_id):
        super().__init__()
        self.room_id = room_id
        self.site_name = 'Zhanqi'
        self.site_domain = 'www.zhanqi.tv'

    def get_room_info(self):
        url = 'https://www.zhanqi.tv/api/static/v2.1/room/domain/%s.json' % self.room_id
        data = self.common_request('GET', url).json()
        if data.get('code') == 0:
            data = data['data']
            return {
                'hostname': data['nickname'],
                'roomname': data['title'],
                'site_name': self.site_name,
                'site_domain': self.site_domain,
                'status': data['status'] == '4'
            }

    def get_live_urls(self):
        url = 'https://www.zhanqi.tv/api/static/v2.1/room/domain/%s.json' % self.room_id
        data = self.common_request('GET', url).json()
        video_levels = data['data']['flashvars']['VideoLevels']
        m3u8 = json.loads(base64.b64decode(video_levels)).get('streamUrl')
        return [m3u8]
