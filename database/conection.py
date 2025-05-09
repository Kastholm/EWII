import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("DB_PW")


def conn_to_db():
    try:
        conn = mysql.connector.connect(
            host="mac123.mysql.pythonanywhere-services.com",
            user="mac123",
            password=password,
            database="mac123$ewii_customer_data"
        )
        if conn.is_connected():
            print('Connection to DB Established')
            return conn
    except:
        print('Connection to DB Failed')