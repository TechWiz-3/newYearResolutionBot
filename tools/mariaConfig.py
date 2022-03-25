from dotenv import load_dotenv
import mysql.connector
from os import getenv

# Login to mysql server: mysql -u root -p
# Create database: CREATE DATABASE your_db_name;
# Create a user if required
# Set permissions if required

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

