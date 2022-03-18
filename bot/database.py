import sqlite3
from sqlite3 import Error
from typing import Tuple


class User(object):
    def __init__(
            self,
            user_id: int,
            **kwargs):
        self.user_id = user_id
        self.rus_path_wav = kwargs.get('rus_voice', None)
        self.rus_path_emb = kwargs.get('rus_emb', None)
        self.eng_path_wav = kwargs.get('eng_voice', None)
        self.eng_path_emb = kwargs.get('eng_emb', None)

    def tupled_data(self):
        return (
            self.rus_path_wav,
            self.rus_path_emb,
            self.eng_path_wav,
            self.eng_path_emb
        )


class DB:
    def __init__(self, dbname="cloner_db.sqlite") -> None:
        self.dbname = dbname
        try:
            self.conn = sqlite3.connect(dbname)
        except Error as e:
            print(e)

    def setup_users(self) -> None:
        stmt = """
        CREATE TABLE IF NOT EXISTS users (
        user_id integer PRIMARY KEY,
        rus_path_voice text,
        rus_path_emb text,
        eng_path_voice text,
        eng_path_emb text)
        """
        self.conn.execute(stmt)
        self.conn.commit()

    def add_user(self, user: User) -> None:
        stmt = """
        INSERT INTO users (
        user_id,
        rus_path_voice,
        rus_path_emb,
        eng_path_voice,
        eng_path_emb) 
        VALUES (?,?,?,?,?)
        """
        args = (user.user_id,) + user.tupled_data()
        self.conn.execute(stmt, args)
        self.conn.commit()

    def update_user(self, user_id: int, path: Tuple) -> None:
        stmt = f"""
        UPDATE users
        SET {path[0]} = ?
        WHERE user_id = ?
        """
        args = (path[1], user_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_user(self, user_id: int):
        stmt = """
        SELECT * 
        FROM users 
        WHERE user_id = ?
        """
        cursor = self.conn.execute(stmt, (user_id,))
        row = cursor.fetchone()
        return row


