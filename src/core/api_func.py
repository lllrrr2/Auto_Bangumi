import re

from core import FullSeasonGet, DownloadClient, RSSAnalyser
from utils import json_config, convert_data
from conf import settings
from dataset import *
from database import DataBase


from ab_decorator import api_failed


class APIProcess:
    def __init__(self):
        self._rss_analyser = RSSAnalyser()
        self._download_client = DownloadClient()
        self._full_season_get = FullSeasonGet()
        self._data_base = DataBase()

    def process_link(self, link):
        data = self._rss_analyser.rss_to_data(link)
        return data

    def get_all_rules(self) -> [dict]:
        datas = self._data_base.get_all_datas()
        return [convert_data.convert_main_data(data) for data in datas]

    @staticmethod
    def set_config(config: SetConf):
        json_config.save(settings.setting_path, convert_data.convert_config(config))
        return "Success"

    def change_rule(self, rule: ChangeRule):
        self._data_base.change_rule(rule.id, rule.title, rule.season)
        return "Success"

    @api_failed
    def download_collection(self, link):
        data = self.process_link(link)
        self._full_season_get.download_collection(data, link, self._download_client)
        return data

    @api_failed
    def add_subscribe(self, link):
        data = self.process_link(link)
        self._download_client.add_rss_feed(link, data.get("official_title"))
        self._download_client.set_rule(data, link)
        return data

    def reset_rule(self):
        self._data_base.reset_rule()
        return "Success"

    def remove_rule(self, id: int):
        self._data_base.delete_column(id)
        return "Success"

    @staticmethod
    def add_rule(title, season):
        data = json_config.load(settings.info_path)
        extra_data = {
            "official_title": title,
            "title_raw": title,
            "season": season,
            "season_raw": "",
            "dpi": "",
            "group": "",
            "eps_complete": False,
            "added": False,
        }
        data["bangumi_info"].append(extra_data)
        json_config.save(settings.info_path, data)
        return "Success"


if __name__ == '__main__':
    from conf import DEV_SETTINGS
    settings.init(DEV_SETTINGS)
    API = APIProcess()
    API.add_subscribe("http://dmhy.org/topics/rss/rss.xml?keyword=彻夜之歌+星空+简")