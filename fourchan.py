import asyncio

import aiohttp
import requests
from typing import NamedTuple

JSON_API = 'https://a.4cdn.org'
OP = 0

class ChanPost:
    def _setup(self):
        self.time = 0
        self.unique_posters = 0
        self.no = 0

    def __init__(self, post_json):
        self._setup()

        self.time = post_json['time']
        self.no = post_json['no']
        if 'unique_ips' in post_json:
            self.unique_posters = post_json['unique_ips']

class ChanThread:
    def __init__(self, thread_json):
        self.id = thread_json['no']  

def get_thread(board, thread_no):
    thread = requests.get(f'{JSON_API}/{board}/thread/{thread_no}.json').json()
    return [ ChanPost(post) for post in thread['posts'] ]

def get_catalog(board):
    catalog = requests.get(f'{JSON_API}/{board}/catalog.json').json()
    return [ ChanThread(thread) for page in catalog for thread in page['threads'] ] 

class FourChanAPI():
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_thread(self, board, thread_no):
        async with self.session.get(f'{JSON_API}/{board}/thread/{thread_no}.json') as resp:
            thread = await resp.json()
            return [ ChanPost(post) for post in thread['posts'] ]

    async def get_catalog(self, board):
        async with self.session.get(f'{JSON_API}/{board}/catalog.json') as resp:
            catalog = await resp.json()
            return [ ChanThread(thread) for page in catalog for thread in page['threads'] ] 

    async def close():
        await self.session.close()
