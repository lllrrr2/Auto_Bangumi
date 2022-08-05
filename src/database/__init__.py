import os

from utils import json_config
from conf import settings
from .ab_sqlite import DataBase
from .ab_json import DataJson

data = DataJson()

if not os.path.exists(settings.data_config):
    json_config.save(settings.data_config, {
        "rss_link": settings.config.rss_link
    })
elif json_config.load(settings.data_config)["rss_link"] != settings.config.rss_link:
    data.save()
    data.update()
    json_config.save(settings.data_config, {
        "rss_link": settings.config.rss_link
    })
else:
    data.update()


