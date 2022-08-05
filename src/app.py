import os
import time
import logging

from __version__ import __version__
from conf import setup_logger, settings
from utils import json_config
from database import data

from core import RSSAnalyser, DownloadClient, FullSeasonGet, FileManager, Renamer


logger = logging.getLogger(__name__)


def reset_log():
    try:
        os.remove(settings.config.log_path)
    except FileNotFoundError:
        pass


def save_data_file(bangumi_data):
    info_path = settings.config.info_path
    json_config.save(info_path, bangumi_data)
    logger.debug("Saved")


def show_info():
    logger.info("                _        ____                                    _ ")
    logger.info(r"     /\        | |      |  _ \                                  (_)")
    logger.info(r"    /  \  _   _| |_ ___ | |_) | __ _ _ __   __ _ _   _ _ __ ___  _ ")
    logger.info(r"   / /\ \| | | | __/ _ \|  _ < / _` | '_ \ / _` | | | | '_ ` _ \| |")
    logger.info(r"  / ____ \ |_| | || (_) | |_) | (_| | | | | (_| | |_| | | | | | | |")
    logger.info(r" /_/    \_\__,_|\__\___/|____/ \__,_|_| |_|\__, |\__,_|_| |_| |_|_|")
    logger.info(r"                                            __/ |                  ")
    logger.info(r"                                           |___/                   ")
    logger.info(f"Version {__version__}  Author: EstrellaXD Twitter: https://twitter.com/Estrella_Pan")
    logger.info("GitHub: https://github.com/EstrellaXD/Auto_Bangumi/")
    logger.info("Starting AutoBangumi...")


def main_process(download_client: DownloadClient):
    rename = Renamer(download_client)
    rss_analyser = RSSAnalyser()
    while True:
        times = 0
        if settings.config.enable_rss_collector:
            rss_analyser.run(data.bangumi_data, download_client)
        if settings.config.eps_complete:
            FullSeasonGet().eps_complete(data.bangumi_data, download_client)
        data.save()
        logger.info("Running....")
        while times < settings.config.times:
            if settings.config.enable_rename:
                rename.run()
            times += 1
            time.sleep(settings.config.sleep_time/settings.config.times)
        settings.update()


def run():
    # 初始化
    reset_log()
    settings.init()
    setup_logger()
    show_info()
    download_client = DownloadClient()
    download_client.init_downloader()
    if settings.rss_link is None:
        logger.error("Please add RIGHT RSS url.")
        quit()
    download_client.rss_feed()
    # 主程序循环
    main_process(download_client)


if __name__ == "__main__":
    run()
