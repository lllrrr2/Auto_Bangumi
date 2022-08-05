from dataclasses import dataclass


@dataclass
class Config:
    host_ip: str = "localhost:8080"
    rss_link: str = None
    user_name: str = "admin"
    password: str = "adminadmin"
    download_path: str = "/downloads/Bangumi"
    sleep_time: int = 7200
    times: int = 20
    rename_method: str = "pn"
    enable_group_tag: bool = False
    not_contain = ["720", "\\d+-\\d+"]
    debug_mode: bool = False
    remove_bad_torrent: bool = False
    dev_debug: bool = False
    eps_complete: bool = False
    webui_port: int = 7892
    language: str = "zh"
    tmdb_api = "32b19d6a05b512190a056fa4e747cbbc"
    enable_tmdb: bool = False
    refresh_rss: bool = False
    http_proxy: str = None
    socks: str = None
    enable_rename: bool = False
    enable_rss_collector: bool = False
    notification_url: str = None
