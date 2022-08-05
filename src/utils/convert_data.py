from dataset import *


def data_to_dict(data: MainData) -> dict:
    return data.__dict__


def dict_to_main_data(data: dict) -> MainData:
    return MainData(**data)



if __name__ == '__main__':
    from parser import TitleParser
    parser = TitleParser()
    raw = "[Lilith-Raws] 在地下城寻求邂逅是否搞错了什么 / Danmachi S04 - 01 [Baha][WEB-DL][1080p][AVC AAC][CHT][MP4]"
    data = parser.analyse(raw)
    print(data)
    dict = data_to_dict(data)
    print(dict)
    data2 = dict_to_main_data(dict)
    print(data2)