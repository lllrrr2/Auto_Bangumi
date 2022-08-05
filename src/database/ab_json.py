import logging
import os.path

from dataset import MainData
from utils import json_config, convert_data
from conf import settings


logger = logging.getLogger(__name__)


class DataJson:
    def __init__(self):
        self.data_path = settings.data_path
        self.bangumi_data: list[MainData] = []

    def save(self):
        json_config.save(self.data_path, [convert_data.data_to_dict(data) for data in self.bangumi_data])
        logger.info(f"Data saved.")

    def append(self, data: MainData):
        self.bangumi_data.append(data)

    def update(self) -> [MainData]:
        data_list = json_config.load(self.data_path)
        self.bangumi_data = [convert_data.dict_to_main_data(data) for data in data_list]
        logger.info(f"Data updated.")