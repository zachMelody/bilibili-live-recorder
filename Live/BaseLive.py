import requests


class BaseLive:
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.115 Safari/537.36 '
        }
        self.session = requests.session()
        self.site_name = ''
        self.site_domain = ''

    def common_request(self, method, url, params=None, data=None):
        connection = None
        if method == 'GET':
            connection = self.session.get(url, headers=self.headers, params=params, verify=False)
        if method == 'POST':
            connection = self.session.post(url, headers=self.headers, params=params, data=data, verify=False)
        return connection

    def get_room_info(self):
        pass

    def get_live_urls(self):
        pass
