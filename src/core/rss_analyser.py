import re
import logging

from network import RequestContent
from parser import TitleParser
from dataset import MainData
from database import DataBase

from conf import settings
from core import DownloadClient

logger = logging.getLogger(__name__)


class RSSAnalyser:
    def __init__(self):
        self._title_analyser = TitleParser()
        self._request = RequestContent()
        self._database = DataBase()

    def rss_to_datas(self) -> [MainData]:
        rss_torrents = self._request.get_torrents(settings.rss_link)
        self._request.close_session()
        already_exist = self._database.select_contain_datas()
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
                data = self._title_analyser.return_data(raw_title)
                if data is not None and data.contain not in already_exist:
                    already_exist.append(data.contain)
                    new_bangumi_info.append(data)
        self._database.insert_datas(new_bangumi_info)
        return new_bangumi_info

    def rss_to_data(self, url) -> MainData:
        rss_torrents = self._request.get_torrents(url)
        self._request.close_session()
        data = self._title_analyser.return_data(rss_torrents[0].name)
        return data

    def run(self, download_client: DownloadClient):
        logger.info("Start collecting RSS info.")
        try:
            new_bangumi_info = self.rss_to_datas()
            download_client.add_rules(new_bangumi_info, rss_link=settings.rss_link)
        except Exception as e:
            logger.debug(e)
        logger.info("Finished")


if __name__ == "__main__":
    print(settings.rss_link)
    rss = RSSAnalyser()
    datas = rss.rss_to_datas()
    for data in datas:
        print(data)