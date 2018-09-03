
# -*- encoding: utf-8 -*-
# Author: Epix
import re

BASE_CID_URL = 'http://live.bilibili.com/api/player?id=cid:{}'
BASE_ROOM_URL = 'http://live.bilibili.com/{}'
BASE_PLAYER_URL = 'http://live.bilibili.com/api/playurl?player=1&cid={}&quality=0'
VIDEO_URL_CHOICE = 'durl/url'
ROOM_ID_RE = re.compile(r'ROOMID\s=\s(\d+)')
CMT_PORT = 788
PROTOCOL_VERSION = 1
ARIA2C_RPC_URL = 'http://127.0.0.1:6800/rpc'
BASE_FILENAME = '{}_{}.flv'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'