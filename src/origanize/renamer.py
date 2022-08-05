import logging
import os.path
import re
import os.path
from pathlib import PurePath, PureWindowsPath


from conf import settings
from core import DownloadClient
from parser import TitleParser

logger = logging.getLogger(__name__)
MEDIA_SUFFIX = ["mp4", "mkv"]


class Renamer:
    def __init__(self):
        self._renamer = TitleParser()

    @staticmethod
    def print_result(torrent_count, rename_count):
        if rename_count != 0:
            logger.info(f"Finished checking {torrent_count} files' name, renamed {rename_count} files.")
        logger.debug(f"Checked {torrent_count} files")

    @staticmethod
    def split_path(path: str):
        suffix = os.path.splitext(path)[-1]
        path = path.replace(settings.config.download_path, "")
        path_parts = PurePath(path).parts \
            if PurePath(path).name != path \
            else PureWindowsPath(path).parts
        path_name = path_parts[-1]
        if re.search(r"S\d{1,2}|[Ss]eason", path_parts[-2]) is not None:
            season = int(re.search(r"\d{1,2}", path_parts[-2]).group())
        else:
            season = 1
            logger.warning(f"No season info.")
        folder_name = path_parts[1] if path_parts[0] == "/" else path_parts[0]
        try:
            download_path = path_parts[1]
        except IndexError:
            download_path = ""
        return path_name, season, folder_name, suffix, download_path

    def rename_torrent(self,
                       info,
                       download_client: DownloadClient,
                       rename_count: int
                       ):
        name = info.name
        torrent_hash = info.hash
        path_name, season, folder_name, suffix, _ = self.split_path(info.content_path)
        try:
            new_name = self._renamer.download_parser(name, folder_name, season, suffix, settings.config.method)
            if path_name != new_name:
                download_client.rename_torrent_file(torrent_hash, path_name, new_name)
                rename_count += 1
        except Exception as e:
            self.rename_collection(torrent_hash, folder_name, season, info.content_path, download_client)

    def rename_collection(self, _hash, folder_name, season, content_path, download_client: DownloadClient):
        contents = download_client.get_torrent_info(_hash)
        for content in contents:
            suffix = os.path.splitext(content.name)[-1]
            if suffix in MEDIA_SUFFIX:
                try:
                    new_name = self._renamer.download_parser(
                        content.name,
                        folder_name,
                        season,
                        suffix,
                        settings.config.method
                    )
                    if new_name != content.name:
                        download_client.rename_torrent_file(_hash,
                                                            os.path.join(content_path,content.name),
                                                            os.path.join(content_path,new_name)
                                                            )
                except Exception as e:
                    logger.debug(e)
                    logger.warning(f"{content.name} rename failed")
                    if settings.config.remove_bad_torrent:
                        download_client.delete_torrent(_hash)

    def run(self, download_client: DownloadClient):
        recent_info = download_client.get_torrents_info()
        torrent_count = recent_info.__len__()
        rename_count = 0
        failed_hashes = []
        for info in recent_info:
            self.rename_torrent(info, download_client, rename_count, failed_hashes)
        self.print_result(torrent_count, rename_count)
        return failed_hashes


if __name__ == "__main__":
    client = DownloadClient()
    hash = "7c344a0e767e3f8b9c6e9867e97f24174f8f237d"
    info = client.get_torrent_info(hash)
    print(info)
