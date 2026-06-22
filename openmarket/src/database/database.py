import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "openmarket"
        }

    def execute(self, query, values=None):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()
        cursor.execute(query, values or ())
        connection.commit()
        cursor.close()
        connection.close()

    def query(self, query, values=None):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, values or ())
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def query_one(self, query, values=None):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, values or ())
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

db = Database()