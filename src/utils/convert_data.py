from dataset import *


def convert_main_data(data: MainData) -> dict:
    return {
        "id": data.id,
        "official_title": data.official_title,
        "title_zh": data.title_zh,
        "title_jp": data.title_jp,
        "title_en": data.title_en,
        "year": data.year,
        "season": data.season,
        "cover_url": data.cover_url,
        "sub_group": data.sub_group,
        "resolution": data.resolution,
        "source": data.source,
        "contain": data.contain,
        "not_contain": data.not_contain,
        "added": data.added,
        "eps_collect": data.eps_collect,
        "ep_offset": data.ep_offset
    }


def convert_config(config: SetConf) -> dict:
    return {}
