import asyncio
import json
import logging
import random
import time
from json import JSONDecodeError
from struct import pack, unpack
from xml.etree import ElementTree
from xmlrpc.client import ServerProxy

import aiohttp

from others.settings import *


class BilibiliClient:
    def __init__(self, url_room_id):
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
        self.protocol_version = 1
        self.reader = None
        self.writer = None
        self.connected = False
        self.cmt_server = ''
        self.url_room_id = int(url_room_id)
        self.room_id = 0
        self.uid = 0
        self.living = False

    async def connect(self):
        url = BASE_ROOM_URL.format(self.url_room_id)
        logging.info('entering room: ' + url)
        # r = requests.get(url)
        # html = r.text
        # m = ROOM_ID_RE.findall(html)
        # room_id = m[0]
        # self.room_id = int(room_id)
        # r = requests.get(BASE_CID_URL.format(room_id))
        # xml_string = '<root>' + r.text + '</root>'
        # t = ElementTree.fromstring(xml_string)
        # self.cmt_server = t.findtext('server')
        # state = t.findtext('state')
        # if state == "LIVE":
        #     await self.go_living()
        with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                html = await r.text()
                m = ROOM_ID_RE.findall(html)
                room_id = m[0]
                self.room_id = int(room_id)
            async with s.get(BASE_CID_URL.format(room_id)) as r:
                xml_string = '<root>' + await r.text() + '</root>'
                t = ElementTree.fromstring(xml_string)
                self.cmt_server = t.findtext('server')
                state = t.findtext('state')
                if state == "LIVE":
                    await self.go_living()

        self.reader, self.writer = await asyncio.open_connection(self.cmt_server, CMT_PORT)
        logging.info('connecting cmt server')
        if await self.join_channel(self.room_id):
            self.connected = True
            logging.info('connected')
            asyncio.ensure_future(self.heartbeat_loop())
            asyncio.ensure_future(self.message_loop())

    async def go_living(self):
        if not self.living:
            logging.info('living')
            self.living = True
            await self.send_download()

    async def go_preparing(self):
        logging.info('preparing')
        self.living = False

    async def heartbeat_loop(self):
        while self.connected:
            await self.send_socket_data(2)
            logging.debug('sent heartbeat')
            await asyncio.sleep(30)

    async def join_channel(self, channel_id):
        self.uid = random.randrange(100000000000000, 300000000000000)
        body = '{"roomid":%s,"uid":%s}' % (channel_id, self.uid)
        await self.send_socket_data(7, body)
        return True

    async def send_socket_data(self, action, body='', magic=16, ver=1, param=1):
        body_byte = bytes(body, 'utf-8')
        length = len(body_byte) + 16
        send_bytes = pack('!IHHII', length, magic, ver, action, param)
        send_bytes = send_bytes + body_byte
        self.writer.write(send_bytes)
        await self.writer.drain()

    async def message_loop(self):
        while self.connected:
            receive_bytes = await self.reader.read(16)
            length, _, action, _ = unpack('!IIII', receive_bytes)
            body_bytes = await self.reader.read(length - 16)
            if action == 3:
                logging.debug('online count packet')
            elif action == 8:
                logging.info('joined')
            elif action == 5:
                try:
                    body_str = body_bytes.decode('utf-8')
                    await self.parse_msg(body_str)
                except JSONDecodeError as e:
                    logging.warning(e)
            else:
                logging.warning(action)

    async def parse_msg(self, messages):
        d = json.loads(messages)
        cmd = d['cmd']
        if cmd == 'LIVE':
            await self.go_living()
        elif cmd == 'PREPARING':
            await self.go_preparing()
        else:
            logging.debug(cmd)

    async def send_download(self):
        with aiohttp.ClientSession() as s:
            async with s.get(BASE_PLAYER_URL.format(self.room_id)) as r:
                xml_string = await r.text()
                t = ElementTree.fromstring(xml_string)
                video_url = t.find(VIDEO_URL_CHOICE).text
                logging.info(video_url)
                aria2c_server = ServerProxy(ARIA2C_RPC_URL)
                gid = aria2c_server.aria2.addUri([video_url], {
                    "out": BASE_FILENAME.format(self.room_id, time.strftime('%Y-%m-%d %H:%M:%S'))})
                logging.info('download request sent with #' + gid)