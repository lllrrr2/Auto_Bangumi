import logging

from parser.analyser import RawParser, DownloadParser
from parser.internet_parser import TMDBParser, BangumiParser
from dataset import MainData
from conf import settings

logger = logging.getLogger(__name__)


class TitleParser:
    def __init__(self):
        self._raw_parser = RawParser()
        self._download_parser = DownloadParser()
        self._tmdb_parser = TMDBParser()

    def raw_parser(self, raw: str):
        return self._raw_parser.analyse(raw)

    def download_parser(self, download_raw, folder_name, season, suffix, method=settings.config.rename_method):
        return self._download_parser.download_rename(download_raw, folder_name, season, suffix, method)

    def tmdb_parser(self, title: str, season: int):
        try:
            tmdb_info = self._tmdb_parser.tmdb_search(title, season)
            logger.debug(f"TMDB Matched, title is {tmdb_info.title_zh}")
            return tmdb_info
        except Exception as e:
            logger.warning("Not Matched with TMDB")
            return None

    def analyse(self, raw: str) -> MainData:
        try:
            episode = self.raw_parser(raw)
            title_search = episode.title_zh if episode.title_zh != "" else episode.title_en
            year = 2022
            if settings.config.enable_tmdb:
                tmdb_info = self.tmdb_parser(title_search, episode.season)
                if tmdb_info is not None:
                    episode.title_zh = tmdb_info.title_zh
                    episode.title_jp = tmdb_info.title_jp
                    episode.season = tmdb_info.last_season if tmdb_info.last_season is not int else episode.season
                    year = tmdb_info.year_number

            data = MainData(
                official_title=episode.title_zh if settings.config.language == "zh" else episode.title_en,
                title_zh=episode.title_zh,
                title_jp=episode.title_jp,
                title_en=episode.title_en,
                year=year,
                season=episode.season,
                cover_url="cover_url",
                sub_group=episode.group,
                resolution=episode.resolution,
                source=episode.source,
                sub_language=episode.sub,
                contain=episode.title_en if episode.title_en else episode.title_zh,
                not_contain=settings.config.not_contain,
                ep_offset=0,
                added=False,
                eps_collect=True if settings.config.eps_complete and episode.episode > 1 else False,
                changed=False,
            )
            logger.debug(f"RAW:{raw} >> {episode.title_en}")
            return data
        except Exception as e:
            logger.debug(e)


if __name__ == '__main__':
    T = TitleParser()
    settings.config.enable_tmdb = True
    raw = "[Lilith-Raws] 在地下城寻求邂逅是否搞错了什么 / Danmachi S04 - 01 [Baha][WEB-DL][1080p][AVC AAC][CHT][MP4]"
    data = T.analyse(raw)
    print(data)
