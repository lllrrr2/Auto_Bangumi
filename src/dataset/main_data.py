from dataclasses import dataclass


# main data
@dataclass
class MainData:
    # main data
    official_title: str
    title_zh: str or None
    title_jp: str or None
    title_en: str or None
    year: int
    season: int
    cover_url: str
    # extra info
    sub_group: str or None
    resolution: str or None
    source: str or None
    sub_language: str or None
    # downloader info
    contain: str
    not_contain: str
    # rename info
    ep_offset: int
    # trigger info
    added: bool
    eps_collect: bool
    changed: bool



# Parser
@dataclass
class TMDBInfo:
    id: int
    title_jp: str
    title_zh: str
    season: list
    last_season: int
    year_number: int
    poster_path: str


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
    not_contain: str
    season: int
    folder_name: str
    path: str


@dataclass
class RePathInfo:
    path: str
    hashes: list

# Torrent
@dataclass
class TorrentInfo:
    name: str
    torrent_link: str

