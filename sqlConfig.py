from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")
DEV_GUILD_ID = 864438892736282625
PROD_GUILD_ID = 867597533458202644

db = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=PORT
)

cursor = db.cursor(buffered=True)

cursor.execute("CREATE TABLE 2022_Goals (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), goals VARCHAR(255), status BOOL, userId BIGINT(255) UNSIGNED)")
cursor.execute("CREATE TABLE reminders (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), days SMALLINT UNSIGNED)")
cursor.execute("CREATE TABLE nextDateReminder (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), next_date SMALLINT UNSIGNED)")

db.commit()