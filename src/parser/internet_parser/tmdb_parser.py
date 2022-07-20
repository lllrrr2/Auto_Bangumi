import re
import time

from network import RequestContent
from conf import settings
from dataset import TMDBInfo

TMDB_API_URl = "https://api.themoviedb.org/3/"
API_KEY = f"api_key={settings.tmdb_api}"


class TMDBParser:
    def __init__(self):
        self._request = RequestContent()

    @staticmethod
    def gen_search_url(title) -> str:
        return TMDB_API_URl+"search/tv?"+API_KEY+f"&page=1&query={title}&include_adult=false"

    @staticmethod
    def gen_info_url(id) -> str:
        return TMDB_API_URl+f"tv/{id}?"+API_KEY+"&language=zh-CN"

    def is_animation(self, tv_id) -> bool:
        url_info = self.gen_info_url(tv_id)
        type_id = self._request.get_json(url_info)["genres"]
        for type in type_id:
            if type.get("id") == 16:
                return True
        return False

    @staticmethod
    def get_season(seasons: list) -> int:
        for season in seasons:
            if re.search(r"第 \d 季", season.get("season")) is not None:
                date = season.get("air_date").split("-")
                [year, _ , _] = date
                now_year = time.localtime().tm_year
                if int(year) == now_year:
                    return int(re.findall(r"\d", season.get("season"))[0])

    def tmdb_search(self, title) -> TMDBInfo:
        url = self.gen_search_url(title)
        contents = self._request.get_json(url).get("results")
        if contents.__len__() == 0:
            url = self.gen_search_url(title.replace(" ", ""))
            contents = self._request.get_json(url).get("results")
        # 判断动画
        for content in contents:
            id = content["id"]
            if self.is_animation(id):
                break
        url_info = self.gen_info_url(id)
        info_content = self._request.get_json(url_info)
        # 关闭链接
        self._request.close_session()
        season = [{"season": s.get("name"), "air_date": s.get("air_date")} for s in info_content.get("seasons")]
        last_season = self.get_season(season)
        title_jp = info_content.get("original_name")
        title_zh = info_content.get("name")
        year_number = info_content.get("first_air_date").split("-")[0]
        return TMDBInfo(id, title_jp, title_zh, season, last_season, year_number)


if __name__ == "__main__":
    test = "辉夜大小姐"
    info = TMDBParser().tmdb_search(test)
    print(f"{info.title_zh}({info.year_number})")
