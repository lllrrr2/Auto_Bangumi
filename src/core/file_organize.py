from origanize import *
from download_client import DownloadClient
from conf import settings


class FileOrganize:
    def __init__(self, client: DownloadClient):
        self._client = client
        self._renamer = Renamer(client)
        self._repather = Repath(client)

    def run(self):
        if settings.renamer:
            collection_hashes = self._renamer.run()
        if settings.repather:
            self._repather.run()