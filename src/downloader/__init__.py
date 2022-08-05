from conf import settings


def getClient():
    host = settings.config.host_ip
    username = settings.config.user_name
    password = settings.config.password
    # TODO 多下载器支持
    # 从 settings 里读取下载器名称，然后返回对应 Client
    from downloader.qb_downloader import QbDownloader
    return QbDownloader(host, username, password)