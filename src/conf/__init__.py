import os

from conf.conf_setup import ConfigSetup
from conf.const import BCOLORS
from conf.parse import parse


settings = ConfigSetup()
if not os.path.exists(settings.config_path):
    settings.create_config()
    from conf.log import setup_logger
else:
    settings.update()
    from conf.log import setup_logger





