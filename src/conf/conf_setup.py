import os
import logging

from dataset import Config
from utils import json_config, get_project_root

from __version__ import __version__
from conf.const import ENV_TO_ATTR

ABS_PATH = get_project_root()
logger = logging.getLogger(__name__)

class ConfigSetup:
    def __init__(self):
        if __version__ == "DEV_VERSION":
            dir_path = ABS_PATH
        else:
            dir_path = "/"
        self.config_path = os.path.join(dir_path, "config", "config.json")
        self.log_path = os.path.join(dir_path, "config", "log.log")
        self.data_path = os.path.join(dir_path, "data", "data.json")
        self.data_config = os.path.join(dir_path, "data", "data_config.json")
        self.version = __version__
        self.config = Config()

    def load_from_env(self):
        # load config from env using ENV_TO_ATTR
        for env_key, attr_key in ENV_TO_ATTR.items():
            if isinstance(attr_key, tuple):
                attr_key, convert_func = attr_key
            else:
                convert_func = lambda e: e
            if env_key in os.environ:
                setattr(self.config, attr_key, convert_func(os.environ[env_key]))

    def create_config(self):
        if not os.path.exists(self.config_path):
            self.save_config(self.config)

    def save_config(self, settings: Config):
        json_config.save(self.config_path, settings.__dict__)
        logger.info(f"Config saved.")

    def update(self):
        config_json = json_config.load(self.config_path)
        self.config = Config(**config_json)

    def init(self, path: str):
        config_json = json_config.load(path)
        self.config = Config(**config_json)
