from pydantic import BaseModel


class SetConf(BaseModel):
    rss_link: str
    host_ip: str
    host_port: int
    host_username: str
    host_password: str
    download_path: str
    sleep_time: int
    loop_frequency: int
    rename_method: str
    remove_bad_torrent: bool


class ChangeRule(BaseModel):
    official_title: str
    must_contain: str
    not_contain: str
    season: int
    on_air_year: int


class AddRule(BaseModel):
    title: str
    season: int


class RssLink(BaseModel):
    rss_link: str
