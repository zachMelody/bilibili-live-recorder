from Live import BiliBiliLive
import os
import requests

id = '251568'
bili = BiliBiliLive(id)
urls = bili.get_live_urls()
room_info = bili.get_room_info()
if room_info['status']:
    resp = requests.get(urls[0], stream=True)
else:
    raise ZeroDivisionError('该房间还未开始直播')

filename = os.path.join(os.getcwd(), 'files', 'opt.flv')
with open(filename, "wb") as f:
    for chunk in resp.iter_content(chunk_size=512): # 500KB # file_name = 'files/opt_test_{}.flv'.format(str(flag))
        f.write(chunk) if chunk else None
