from network import RequestContent


class BangumiParser:
    def __init__(self):
        self.search_url = lambda e: \
            f"https://api.bgm.tv/search/subject/{e}?type=2&responseGroup=small"
        self.info_url = lambda e: \
            f"https://api.bgm.tv/subject/{e}"
        self._request = RequestContent()

    def search(self, _title) -> list or None:
        search_url = self.search_url(_title)
        contents = self._request.get_json(search_url)["list"]
        if contents.__len__() == 0:
            return None
        return contents

    def analyse_bgm_content(self, contents: list):
        for content in contents:
            return None



if __name__ == '__main__':
    BGM = BangumiParser()
    print(BGM.search("辉夜大小姐"))