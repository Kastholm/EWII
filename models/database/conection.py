import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("DB_PW")
USER = os.getenv("USER")
HOST = os.getenv("HOST")
DB = os.getenv("DB")


def conn_to_db():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=password,
            database=DB
        )
        if conn.is_connected():
            print('Connection to DB Established')
            return conn
    except:
        print('Connection to DB Failed')