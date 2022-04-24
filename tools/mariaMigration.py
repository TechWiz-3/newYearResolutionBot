# Connect to old database
# Connect to new database
# Go to goals table
# Run through entries, extract data and enter it into new db
# Repeat with other tables
# Maybe i should make a db migration tool

from dotenv import load_dotenv
import mysql.connector
from os import getenv

# load relevant variables
load_dotenv()
DB_HOST = getenv("M_HOST")
DB_USER = getenv("M_USER")
DB_PASSWORD = getenv("M_PASSWORD")
DB_NAME = getenv("M_DB")
PORT = getenv("M_PORT")

OLD_HOST = getenv("MYSQLHOST")
OLD_USER = getenv("MYSQLUSER")
OLD_PASSWORD = getenv("MYSQLPASSWORD")
OLD_NAME = getenv("MYSQLDATABASE")
OLD_PORT = getenv("MYSQLPORT")


# connect to the database
new_db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=PORT
        )

old_db = mysql.connector.connect(
    host=OLD_HOST,
    user=OLD_USER,
    password=OLD_PASSWORD,
    database=OLD_NAME,
    port=OLD_PORT
        )

# define the cursor
new_cursor = new_db.cursor(buffered=True)
old_cursor = old_db.cursor(buffered=True)

get_old_goals = "SELECT id, user, goals, status, userId, serverId FROM 2022_Goals"
old_cursor.execute(get_old_goals)
for goal_entry in old_cursor:
    add_goal_entry = "INSERT INTO goal (id, user, goal, status, user_id, server_id) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        new_cursor.execute(add_goal_entry, goal_entry)
    except Exception as error:
        print(error)

get_old_reminders = "SELECT id, user, days, userId FROM reminders"
old_cursor.execute(get_old_reminders)
for reminder_entry in old_cursor:
    add_reminder_entry = "INSERT INTO reminder (id, user, days, user_id) VALUES (%s, %s, %s, %s)"
    try:
        new_cursor.execute(add_reminder_entry, reminder_entry)
    except Exception as error:
        print(error)

get_old_dates = "SELECT id, user, next_date, userId FROM nextDateReminder"
old_cursor.execute(get_old_dates)
for date_entry in old_cursor:
    add_date_entry = "INSERT INTO next_reminder (id, user, next_date, user_id) VALUES (%s, %s, %s, %s)"
    try:
        new_cursor.execute(add_date_entry, date_entry)
    except Exception as error:
        print(error)

get_old_config = "SELECT id, server_id, reminder_channel_id FROM config"
old_cursor.execute(get_old_config)
for config_entry in old_cursor:
    add_config_entry = "INSERT INTO config (id, server_id, reminder_channel_id) VALUES (%s, %s, %s)"
    try:
        new_cursor.execute(add_config_entry, config_entry)
    except Exception as error:
        print(error)

new_db.commit()