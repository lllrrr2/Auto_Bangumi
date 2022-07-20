import re
from pathlib import PurePath, PureWindowsPath

from core.download_client import DownloadClient
from parser import TitleParser


class CollectionOrganize:
    def __init__(self, client: DownloadClient):
        self._client = client
        self._parser = TitleParser()

    def get_contents_path(self, _hash):
        recent_info, _ = self._client.get_collection_info()
        contents_path = []
        for info in recent_info:
            contents_path.append(info.content_path)
        return contents_path

    def gen_new_path(self, _path):
        path_parts = _path.split("/")
        folder_name = path_parts[1] if path_parts[0] == "/" else path_parts[0]
        try:
            download_path = path_parts[1]
        except IndexError:
            download_path = ""
        return folder_name, download_path

    def repath_collection(self, old_path, new_path, _hash):
        self._client.move_torrent(_hash, new_path)