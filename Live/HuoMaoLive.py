from .BaseLive import BaseLive


class HuoMaoLive(BaseLive):
    def __init__(self, room_id):
        super().__init__()
        self.room_id = room_id
        self.site_name = 'HuoMao'
        self.site_domain = 'www.huomao.com'

    def get_room_info(self):
        dom = self.common_request('GET', 'https://' + self.site_domain + '/' + str(self.room_id)).text
        room_info = None
        for l in dom.split('\n'):
            if 'channelOneInfo' in l:
                room_info = eval(l[l.index('{'):-2].replace('\/', '/').replace('null', '""'))
        room_name = room_info['channel']
        host_name = room_info['nickname']
        video_id = room_info['stream']
        url = 'https://www.huomao.com/swf/live_data'
        data = self.common_request('POST', url, data={
            'VideoIDS': video_id,
            'streamtype': 'live',
            'cdns': 1
        }).json()
        status = (data['roomStatus'] == '1')
        return {
            'hostname': host_name,
            'roomname': room_name,
            'site_name': self.site_name,
            'site_domain': self.site_domain,
            'status': status
        }

    def get_live_urls(self):
        dom = self.common_request('GET', 'https://' + self.site_domain + '/' + str(self.room_id)).text
        room_info = None
        for l in dom.split('\n'):
            if 'channelOneInfo' in l:
                room_info = eval(l[l.index('{'):-2].replace('\/', '/').replace('null', '""'))
        video_id = room_info['stream']
        url = 'https://www.huomao.com/swf/live_data'
        data = self.common_request('POST', url, data={
            'VideoIDS': video_id,
            'streamtype': 'live',
            'cdns': 1
        }).json()
        return [data['streamList'][-1]['list'][0]['url']]
