import sqlite3

from src.database import db
from src.exceptions.operation import OperationNotFound


class OperationService:
    def __init__(self):
        self.connection = db.connection

    def create_operation(self, data: dict) -> int:
        """Создание операции в БД"""

        values = [value for value in data.values()]
        keys = [key for key in data.keys()]

        query = f"INSERT INTO operation " + ','.join(keys) + " VALUES (?, ?, ?, ?, ?)"

        try:
            with self.connection as connection:
                cursor = connection.execute(query, values)
                connection.commit()
        except sqlite3.IntegrityError:
            raise OperationNotFound
        else:
            return cursor.lastrowid

    def read(self, category_id: dict) -> dict:
        """Чтение информации об операции в БД"""
        query = f"SELECT id, type, date, amount, description FROM operation WHERE category_id = ?"
        params = (category_id, )
        with self.connection as connection:
            cursor = connection.execute(query, params)
            category = cursor.fetchone()
            return dict(category)

