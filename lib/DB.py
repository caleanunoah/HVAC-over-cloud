import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DB:
    # TODO Implement Error handling [https://peps.python.org/pep-0249/#exceptions]
    def __init__(self):
        self.query_data = []

    def connect(self):
        self.cnx = mysql.connector.connect(user=os.getenv("USER"),
                                   password=os.getenv("PASS"),
                                   host=os.getenv("ENDPOINT"),
                                   database=os.getenv("NAME"))
        self.cursor = self.cnx.cursor()
        return self.cursor

    def query(self, query):
        self.cursor.execute(query)

        for row in self.cursor:
            #print(row)
            self.query_data.append(row)

        return self.query_data

    def close(self):
        self.cnx.close()


if __name__ == "__main__":
    db = DB()
    db.connect()
    print(db.query("SELECT * FROM users;"))
    db.close()
