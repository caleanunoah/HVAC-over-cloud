import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DB:
    # TODO Implement Error handling [https://peps.python.org/pep-0249/#exceptions]
    def __init__(self):
        self.query_data = []
        self.queries = {
            "USE": "USE Operator_sites;",
            "SENSOR INSERT": "INSERT INTO sensors VALUES ('12345678-91011-4447-bd53-17f3781c97a1', '0', '2023-04-11 2:34:57', 'ac780a17-b3b1-4442-b0e6-f6cdb00fb7fd');",
            "MODIFY": "",
            "SITE SELECT": "SELECT * FROM site;",
            "BUILDINGS SELECT": "SELECT * FROM buildings;",
            "RLDS SELECT": "SELECT * FROM RLDS;",
            "SENSOR SELECT": "SELECT * FROM sensors;",
            "COMMIT": "COMMIT;",
        }

    def connect(self):
        self.cnx = mysql.connector.connect(user=os.getenv("USER"),
                                   password=os.getenv("PASS"),
                                   host=os.getenv("ENDPOINT"),
                                   database=os.getenv("NAME"))
        self.cursor = self.cnx.cursor()
        return self.cursor

    def query(self, query):
        self.res = []
        self.cursor.execute(query)

        for row in self.cursor:
            #print(row)
            self.res.append(row)

        return self.res

    def close(self):
        self.cnx.close()


if __name__ == "__main__":
    db = DB()
    db.connect()
    print(db.query("SELECT * FROM users;"))

    print(db.query(db.queries['SENSOR SELECT']))

    #print(db.query(db.queries['SENSOR INSERT']))
    #db.query(db.queries['COMMIT'])

    db.close()
