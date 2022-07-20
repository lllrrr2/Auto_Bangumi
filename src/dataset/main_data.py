from dataclasses import dataclass


# main data
@dataclass
class MainData:
    id: int or None
    # main data
    title_zh: str or None
    title_jp: str or None
    title_en: str or None
    year: int
    season: int
    cover_url: str
    # extra info
    sub_group: str
    resolution: str
    source: str
    # downloader info
    contain: str
    not_contain: str
    added: bool
    eps_collect: bool
    # rename info
    ep_offset: int


# Parser
@dataclass
class TMDBInfo:
    id: int
    title_jp: str
    title_zh: str
    season: dict
    last_season: int
    year_number: int


@dataclass
class BgmInfo:
    title_zh: str
    title_jp: str
    image_url: str


@dataclass
class Episode:
    title_en: str
    title_zh: str
    title_jp: str
    season: int
    season_raw: str
    episode: int
    sub: str
    group: str
    resolution: str
    source: str


# Repath
@dataclass
class RuleInfo:
    rule_name: str
    contain: str
    season: int
    folder_name: str
    new_path: str


@dataclass
class RePathInfo:
    path: str
    hashes: list

