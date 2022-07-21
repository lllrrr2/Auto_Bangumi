from dataset import MainData
from conf import settings

import logging
import sqlite3

logger = logging.getLogger(__name__)


class DataBase:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def create_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS BANGUMI (
                id INTEGER PRIMARY KEY,
                title_zh TEXT,
                title_jp TEXT,
                title_en TEXT,
                year INTEGER,
                season INTEGER,
                cover_url TEXT,
                sub_group TEXT,
                resolution TEXT,
                source TEXT,
                contain TEXT,
                not_contain TEXT,
                added INTEGER,
                eps_collect INTEGER,
                ep_offset INTEGER  
            );
        """)
        self.conn.commit()
        self.conn.close()

    def connect_db(self):
        self.conn = sqlite3.connect(settings.db_path)
        self.cursor = self.conn.cursor()

    def insert_data(self, data: MainData):
        self.connect_db()
        self.cursor.execute("""
            INSERT INTO BANGUMI (
                title_zh,
                title_jp,
                title_en,
                year,
                season,
                cover_url,
                sub_group,
                resolution,
                source,
                contain,
                not_contain,
                added,
                eps_collect,
                ep_offset
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.title_zh,
            data.title_jp,
            data.title_en,
            data.year,
            data.season,
            data.cover_url,
            data.sub_group,
            data.resolution,
            data.source,
            data.contain,
            data.not_contain,
            1 if data.added else 0,
            1 if data.eps_collect else 0,
            data.ep_offset
        ))

    def insert_datas(self, datas: list):
        self.connect_db()
        for data in datas:
            self.insert_data(data)

    def get_all_datas(self) -> [MainData]:
        self.connect_db()
        self.cursor.execute("""
            SELECT * FROM BANGUMI
        """)
        datas = self.cursor.fetchall()
        self.conn.close()
        data_list = []
        for data in datas:
            data_list.append(MainData(
                id=data[0],
                title_zh=data[1],
                title_jp=data[2],
                title_en=data[3],
                year=data[4],
                season=data[5],
                cover_url=data[6],
                sub_group=data[7],
                resolution=data[8],
                source=data[9],
                contain=data[10],
                not_contain=data[11],
                added=data[12],
                eps_collect=data[13],
                ep_offset=data[14]
            ))
        return data_list

    def update_data(self, data: MainData):
        self.connect_db()
        self.cursor.execute("""
            UPDATE BANGUMI SET
                title_zh = ?,
                title_jp = ?,
                title_en = ?,
                year = ?,
                season = ?,
                cover_url = ?,
                sub_group = ?,
                resolution = ?,
                source = ?,
                contain = ?,
                not_contain = ?,
                added = ?,
                eps_collect = ?,
                ep_offset = ?
            WHERE id = ?
        """, (
            data.title_zh,
            data.title_jp,
            data.title_en,
            data.year,
            data.season,
            data.cover_url,
            data.sub_group,
            data.resolution,
            data.source,
            data.contain,
            data.not_contain,
            1 if data.added else 0,
            1 if data.eps_collect else 0,
            data.ep_offset,
            data.id
        ))
        logger.info(f"Update column: {data.id} success.")

    def delete_column(self, _id: int):
        self.connect_db()
        self.cursor.execute("""
               DELETE FROM BANGUMI WHERE id = ?
           """, (_id,))
        logger.info(f"Delete column: {_id} success.")

    def select_contain_datas(self) -> list:
        self.connect_db()
        db_list = self.cursor.execute("""SELECT contain FROM BANGUMI""")
        return [data[0] for data in db_list]

    def commit(self):
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    db = DataBase()
    # db.delete_column(1)
    # data = MainData(None, "测试", "测试", "Test", 2020, 1, "Lilith", "测试", "测试", "测试", "测试", "测试", True, False, 0)
    # for data in db.get_all_datas():
    #     print(data.title_zh)
    # db.commit()

    print(db.select_contain_datas())
