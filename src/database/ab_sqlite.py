import os.path

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
        self.connect_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS BANGUMI (
                id INTEGER PRIMARY KEY,
                official_title TEXT,
                title_zh TEXT,
                title_jp TEXT,
                title_en TEXT,
                year INTEGER,
                season INTEGER,
                cover_url TEXT,
                sub_group TEXT,
                resolution TEXT,
                source TEXT,
                sub_language TEXT,
                contain TEXT,
                not_contain TEXT,
                refresh INTEGER,
                eps_collect INTEGER,
                ep_offset INTEGER  
            );
        """)
        self.conn.commit()
        self.conn.close()

    def connect_db(self):
        self.conn = sqlite3.connect(settings.db_path)
        self.cursor = self.conn.cursor()

    def init_db(self):
        if os.path.exists(settings.db_path):
            logger.info(f"{settings.db_path} already exists.")
        else:
            self.create_db()
            logger.info(f"Database created.")

    def insert_data(self, data: MainData):
        self.connect_db()
        self.cursor.execute("""
            INSERT INTO BANGUMI (
                official_title,
                title_zh,
                title_jp,
                title_en,
                year,
                season,
                cover_url,
                sub_group,
                resolution,
                source,
                sub_language,
                contain,
                not_contain,
                added,
                eps_collect,
                ep_offset
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.official_title,
            data.title_zh,
            data.title_jp,
            data.title_en,
            data.year,
            data.season,
            data.cover_url,
            data.sub_group,
            data.resolution,
            data.source,
            data.sub_language,
            data.contain,
            data.not_contain,
            1 if data.added else 0,
            1 if data.eps_collect else 0,
            data.ep_offset
        ))
        self.conn.commit()

    def insert_datas(self, datas: list):
        self.connect_db()
        for data in datas:
            self.insert_data(data)
        self.conn.close()

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
                official_title=data[1],
                title_zh=data[2],
                title_jp=data[3],
                title_en=data[4],
                year=data[5],
                season=data[6],
                cover_url=data[7],
                sub_group=data[9],
                resolution=data[9],
                source=data[10],
                sub_language=data[11],
                contain=data[12],
                not_contain=data[13],
                added=data[14],
                eps_collect=data[15],
                ep_offset=data[16]
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
        self.commit()

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
    data = MainData(id=None, official_title='Lycoris Recoil', title_zh='', title_jp='', title_en='Lycoris Recoil', year=2015, season=1, cover_url='cover_url', sub_group='NC-Raws', resolution='1920x1080', source=None, sub_language=None, contain='Lycoris Recoil', not_contain=['720', '\\d+-\\d+'], ep_offset=0, added=False, eps_collect=False)
    db.insert_data(data)
