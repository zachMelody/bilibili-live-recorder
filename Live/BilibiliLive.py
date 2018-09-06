from .BaseLive import BaseLive


class BiliBiliLive(BaseLive):
    def __init__(self, room_id):
        super().__init__()
        self.room_id = room_id
        self.site_name = 'BiliBili'
        self.site_domain = 'live.bilibili.com'

    def get_room_info(self):
        data = {}
        room_info_url = 'https://api.live.bilibili.com/room/v1/Room/get_info'
        user_info_url = 'https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room'
        response = self.common_request('GET', room_info_url, {'room_id': self.room_id}).json()
        if response['msg'] == 'ok':
            data['roomname'] = response['data']['title']
            data['site_name'] = self.site_name
            data['site_domain'] = self.site_domain
            data['status'] = response['data']['live_status'] == 1
        self.room_id = response['data']['room_id']  # 解析完整 room_id
        response = self.common_request('GET', user_info_url, {'roomid': self.room_id}).json()
        data['hostname'] = response['data']['info']['uname']
        return data

    def get_live_urls(self):
        live_urls = []
        url = 'https://api.live.bilibili.com/api/playurl'
        durls = self.common_request('GET', url, {
            'cid': self.room_id,
            'otype': 'json',
            'quality': 0,
            'platform': 'web'
        }).json()
        for durl in durls['durl']:
            live_urls.append(durl['url'])
        return live_urls
