import mysql.connector


class Database:

    def __init__(self):

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="openmarket"
        )

        self.cursor = self.connection.cursor(buffered=True)

    def execute(self, query, values=None):

        self.cursor.execute(query, values or ())

        self.connection.commit()

    def query(self, query, values=None):

        self.cursor.execute(query, values or ())

        return self.cursor.fetchall()

    def query_one(self, query, values=None):

        self.cursor.execute(query, values or ())

        return self.cursor.fetchone()