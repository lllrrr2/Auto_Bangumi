import time

import requests
import socket
import socks
import logging

from bs4 import BeautifulSoup

from conf import settings

logger = logging.getLogger(__name__)


class RequestURL:
    def __init__(self):
        self.session = requests.session()
        if settings.config.http_proxy is not None:
            self.session.proxies = {
                "https": settings.http_proxy,
                "http": settings.http_proxy,
            }
        elif settings.config.socks is not None:
            socks_info = settings.socks.split(",")
            socks.set_default_proxy(socks.SOCKS5, addr=socks_info[0], port=int(socks_info[1]), rdns=True,
                                    username=socks_info[2], password=socks_info[3])
            socket.socket = socks.socksocket
        self.header = {
            "user-agent": "Mozilla/5.0",
            "Accept": "application/xml"
        }

    def get_url(self, url):
        times = 0
        while times < 5:
            try:
                req = self.session.get(url=url, headers=self.header)
                return req
            except Exception as e:
                logger.debug(f"URL: {url}")
                logger.debug(e)
                logger.warning("ERROR with DNS/Connection.")
                time.sleep(5)
                times += 1

    def get_content(self, url, content="xml"):
        if content == "xml":
            return BeautifulSoup(self.get_url(url).text, content)
        elif content == "json":
            return self.get_url(url).json()

    def close(self):
        self.session.close()
