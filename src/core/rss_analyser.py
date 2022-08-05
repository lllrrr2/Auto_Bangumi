import re
import logging

from core import DownloadClient
from network import RequestContent
from parser import TitleParser
from dataset import MainData

from conf import settings


logger = logging.getLogger(__name__)


class RSSAnalyser:
    def __init__(self):
        self._title_analyser = TitleParser()
        self._request = RequestContent()

    def rss_to_datas(self, _datas: list[MainData]) -> list[MainData]:
        rss_torrents = self._request.get_torrents(settings.config.rss_link)
        self._request.close_session()
        already_exist = [data.contain for data in _datas]
        new_bangumi_info = []
        for torrent in rss_torrents:
            raw_title = torrent.name
            extra_add = True
            if already_exist is not []:
                for contain in already_exist:
                    if re.search(contain, raw_title) is not None:
                        logger.debug(f"Had added {contain} before")
                        extra_add = False
                        break
            if extra_add:
                new_data = self._title_analyser.analyse(raw_title)
                if new_data is not None and new_data.contain not in already_exist:
                    already_exist.append(new_data.contain)
                    new_bangumi_info.append(new_data)
                    _datas.append(new_data)
        return new_bangumi_info

    def rss_to_data(self, url) -> MainData:
        rss_torrents = self._request.get_torrents(url)
        self._request.close_session()
        data = self._title_analyser.analyse(rss_torrents[0].name)
        return data

    def run(self, _datas: list[MainData], download_client: DownloadClient):
        logger.info("Start collecting RSS info.")
        try:
            new_bangumi_info = self.rss_to_datas(_datas)
            download_client.add_rules(new_bangumi_info, rss_link=settings.config.rss_link)
        except Exception as e:
            logger.debug(e)
        logger.info("Finished")


if __name__ == "__main__":
    rss = RSSAnalyser()
    datas = rss.rss_to_datas([])
    for data in datas:
        print(data)
