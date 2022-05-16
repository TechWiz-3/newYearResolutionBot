import mysql.connector as connector
import os
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")

    
def connect():
    db = connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=PORT,
        pool_size=32,
        pool_name="resolutionpool"
    )
    cursor = db.cursor(buffered=True)

    return cursor, db
    
def disconnect(cursor,db):
    cursor.close()
    db.close()
    return True