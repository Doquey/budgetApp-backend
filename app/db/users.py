from app.services.env_vars import POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_DATABASE
import psycopg2
from .src import DataBase
from dataclasses import dataclass
from app.db.Models import User
from typing import Any


@dataclass
class ConnectionInfo():
    database: str
    user: str
    password: str
    host: str
    port: str


class Users(DataBase):
    def __init__(self, info: ConnectionInfo):
        self.db_credentials = info
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            database=self.db_credentials.database,
            user=self.db_credentials.user,
            password=self.db_credentials.password,
            host=self.db_credentials.host,
            port=self.db_credentials.port
        )

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def put_item(self, item: dict, table_name: str):
        cursor = self.conn.cursor()
        columns = ', '.join(item.keys())
        placeholders = ', '.join(['%s'] * len(item))

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            cursor.execute(query, tuple(item.values()))
            self.conn.commit()
        except Exception as e:
            # Roll back the transaction in case of error
            self.conn.rollback()
            raise e  # Re-raise the exception to propagate it
        finally:
            cursor.close()

    def update_item(self, identification: Any, item: dict, table_name: str):
        pass

    def delete_item(self, identification: Any, table_name: str):
        pass

    def get_item(self, username: str, table_name: str) -> dict:
        cursor = self.conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE username=%s"
        try:
            cursor.execute(query, (username,))
            query_result = cursor.fetchone()
            user = {
                "username": query_result[0], "password": query_result[1], "phone": query_result[2], "email": query_result[3], "name": query_result[4]}
            return user if user else {}
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def get_all(self, table_name: str) -> list[dict]:
        pass


conn_info = ConnectionInfo(POSTGRES_DATABASE, POSTGRES_USER,
                           POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT)

users_db = Users(conn_info)

users_db.connect()
