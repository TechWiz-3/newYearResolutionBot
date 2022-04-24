from dotenv import load_dotenv
import mysql.connector
from os import getenv

# Login to mysql server: mysql -u root -p
# Create database: CREATE DATABASE your_db_name;
# Create a user if required
# Set permissions if required
# `use db`

# load relevant variables
load_dotenv()
DB_HOST = getenv("M_HOST")
DB_USER = getenv("M_USER")
DB_PASSWORD = getenv("M_PASSWORD")
DB_NAME = getenv("M_DB")
PORT = getenv("M_PORT")

# connect to the database
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=PORT
        )
# define the cursor
cursor = db.cursor(buffered=True)

# create the goals table
# CREATE TABLE goal (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), goal TINYTEXT, status BOOL, user_id VARCHAR(50), server_id VARCHAR(50))

# create the reminder intervals table
# CREATE TABLE reminder (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), days SMALLINT UNSIGNED, user_id VARCHAR(50))

# create the next-date table
# CREATE TABLE next_reminder (id INT AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), next_date DATE, user_id VARCHAR(50))

# create the server configuration table
# CREATE TABLE config (id INT AUTO_INCREMENT PRIMARY KEY, server_id VARCHAR(50), reminder_channel_id VARCHAR(50))

