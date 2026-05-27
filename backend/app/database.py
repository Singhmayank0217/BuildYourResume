import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings

import json

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(settings.DATABASE_URL)
            return self.connection
        except Exception as e:
            print(f"Database connection error: {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            print(f"Query execution error: {e}")
            raise

    def execute_insert(self, query, params=None):
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params or ())
            self.connection.commit()
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            self.connection.rollback()
            print(f"Insert execution error: {e}")
            raise

    def execute_update(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Exception as e:
            self.connection.rollback()
            print(f"Update execution error: {e}")
            raise

db = Database()
