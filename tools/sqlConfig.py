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

db = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=PORT
)

cursor = db.cursor(buffered=True)

# create the goals table
cursor.execute("CREATE TABLE 2022_Goals (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), goals TINYTEXT, status BOOL, userId VARCHAR(50), serverId VARCHAR(50))")

# create the reminder intervals table
cursor.execute("CREATE TABLE reminders (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), days SMALLINT UNSIGNED, userId VARCHAR(50))")

# create the next-date table
cursor.execute("CREATE TABLE nextDateReminder (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), next_date DATE, userId VARCHAR(50))")

# create the server configuration table
cursor.execute("CREATE TABLE config (id INT AUTO_INCREMENT PRIMARY KEY, server_id VARCHAR(50), reminder_channel_id VARCHAR(50))")


# commit changes
db.commit()