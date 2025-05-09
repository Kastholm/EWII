import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("DB_PW")


def conn_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="ewii_customer_data"
        )
        if conn.is_connected():
            print('Connection to DB Established')
            return conn
    except:
        print('Connection to DB Failed')