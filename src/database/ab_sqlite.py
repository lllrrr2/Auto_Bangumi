from dataset import MainData
from conf import settings

import sqlite3


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(settings.db_path)
        self.cursor = self.conn.cursor()

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
                added BOOLEAN,
                eps_collect BOOLEAN,
                ep_offset INTEGER  
            );
        """)
        self.conn.commit()
        self.conn.close()

    @staticmethod
    def load_db() -> [MainData]:
        conn = sqlite3.connect(settings.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM main_data")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def save_db(data: [MainData]):
        conn = sqlite3.connect(settings.db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS main_data (id TEXT, title TEXT, season TEXT, group TEXT, dpi TEXT, eps_complete TEXT, added TEXT)")
        for d in data:
            cursor.execute("INSERT INTO main_data VALUES (?, ?, ?, ?, ?, ?, ?)", (d.id, d.title, d.season, d.group, d.dpi, d.eps_complete, d.added))
        conn.commit()
        conn.close()

    @staticmethod
    def search_title(title) -> MainData:
        conn = sqlite3.connect(settings.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM main_data WHERE title = ?", (title,))
        data = cursor.fetchone()
        conn.close()
        return MainData(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    @staticmethod
    def search_id(uuid):
        conn = sqlite3.connect(settings.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM main_data WHERE id = ?", (uuid,))
        data = cursor.fetchone()
        conn.close()
        return MainData(data[0], data[1], data[2], data[3], data[4], data[5], data[6])


if __name__ == '__main__':
    db = DataBase()
    db.create_db()