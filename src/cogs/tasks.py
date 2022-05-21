from discord.ext import tasks
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import date, timedelta
from discord.utils import get
import random
from cogs.functions.db_functions import disconnect

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")



reminder_funny_text = ["The force wishes me to remind you of your goals, here they are.", "Did you think I'd let you forget about your goals? NOT A CHANCE", "How's it going mate?", "*Mighty presense decscends from sky to deliver a reminder to you*", "Ay bro, it's been some time, keep working at it", "Gravity Destroyers 2022 checking in with you"]
reminder_for_one_achieved = ["You've made the first step, now it's time for the second one <:lezgooo:925286931221344256>", "Hard work, smart work let's go <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>", "You got this baby, second goal achieve coming soon <:stronk_doge:925285801921769513>", "*Mighty presense decscends from sky to deliver a reminder to you*"]
reminder_for_two_achieved = ["Two goals achieved mate, the thirds gonna be a special one ;)", "Someones going for their 3rd goal this year <:lezgooo:925286931221344256>", "Third times a charm"]
reminder_for_three_plus_achieved = ["This mans on a roll, keep it going bro", "Did you think I'd let you forget about your goals? NOT A CHANCE. You've come THIS far, next goal let's go", "Accountability session king achiever howsit going?", "Sup warrior, time to check in :sunglasses:"]

@tasks.loop(minutes = 2.0)
async def reminder_function(bot):
    db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=PORT,
    pool_name="taskspool",
    pool_size=32
        )
    cursor = db.cursor(buffered=True)
    print("I'm running")
    goals = ""
    find_channel_id = 0
    reminder_channel_found = False
    reminder_channel_id_final = 0
    global_server_id = 0
    reminder_channel_object = None
    sql = "SELECT user_id, days FROM reminder"  # select the username and their selected reminder interval
    cursor.execute(sql)  # execute sql query
    results = cursor.fetchall()
    for (user_id, howOften) in results:  # loop through the results of the sql query
        sql = "SELECT user_id, next_date FROM next_reminder WHERE user_id = %s"
        value = (user_id,)
        second_cursor = db.cursor(buffered=True)
        second_cursor.execute(sql, value)
        second_results = second_cursor.fetchall()
        second_cursor.close()
        for date_entry in second_results:
            user_id_for_third_query, unpackedDate = date_entry
            slash_emoji = get(bot.emojis, name="aslash")
            green_tick_emoji = get(bot.emojis, name="epicTick")
            if unpackedDate == date.today():
                get_goal_entry = "SELECT user, goal, status, user_id, server_id FROM goal WHERE user_id = %s"  # request for the users goals in the goals table
                user_request = (user_id_for_third_query,)
                third_cursor = db.cursor(buffered=True)
                third_cursor.execute(get_goal_entry, user_request)  # execute sql query
                third_results = third_cursor.fetchall()
                third_cursor.close()
                status_counter = 0
                for (
                    fullEntry
                ) in third_results:  # loop the the results of the latest query
                    user,goal,status,idByMember,serverByMember = fullEntry #assign the variables returned
                    find_channel_id = int(serverByMember) # variable used for finding the channel, it is the server id
                    global_server_id = int(serverByMember) # used for getting the server object later on
                    try:
                        member_object = bot.get_user(int(idByMember))
                    except:
                        member_object = f'User mention failed <@{user_id_for_third_query}> i.e {user}'
                        print('Issue occured, none was returned as member_object as shown here', member_object)
                    if status == 1:
                        goals += f'{green_tick_emoji} `{goal}`\n'
                        status_counter +=1
                    elif status == 0:
                        goals += f'{slash_emoji} `{goal}`\n'
                third_cursor = db.cursor(buffered=True) 
                get_reminder_channel = "SELECT reminder_channel_id FROM config WHERE server_id = %s"
                values = (find_channel_id,)
                third_cursor.execute(get_reminder_channel, values)
                for unpacked_channel in third_cursor:
                    # unpack the channel id
                    reminder_channel_id_final, = unpacked_channel
                    reminder_channel_id_final = int(reminder_channel_id_final)
                    reminder_channel_found = True
                print("Reminder Channel Found:", reminder_channel_found)
                server = bot.get_guild(global_server_id)
                try:
                    reminder_channel_object = server.get_channel(reminder_channel_id_final)
                except:
                    print('MAY DAY MAY DAY, SOS, was unable to get reminder channel object')
                # print users goals to remind them
                if status_counter == 0:
                    send_funny_text = random.choice(reminder_funny_text)
                    try:
                        await reminder_channel_object.send(f"{member_object.mention}\n**{send_funny_text}**\n\n{goals}")  # print the users goals
                    except:
                        await reminder_channel_object.send(
                            f"{member_object}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                elif status_counter == 1:
                    send_funny_text = random.choice(reminder_for_one_achieved)
                    try:
                        await reminder_channel_object.send(
                            f"{member_object.mention}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                    except:
                        await reminder_channel_object.send(
                            f"{member_object}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                elif status_counter == 2:
                    send_funny_text = random.choice(reminder_for_two_achieved)
                    try:
                        await reminder_channel_object.send(
                            f"{member_object.mention}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                    except:
                        await reminder_channel_object.send(
                            f"{member_object}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                elif status_counter > 2:
                    send_funny_text = random.choice(reminder_for_three_plus_achieved)
                    try:
                        await reminder_channel_object.send(
                            f"{member_object.mention}\n**{send_funny_text}**\n\n{goals}"
                            ) # print the users goals
                    except:
                        await reminder_channel_object.send(
                            f"{member_object}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                goals = "" # reset goals variable
                update_sql = "UPDATE next_reminder SET next_date = %s WHERE user_id = %s"
                next_date = date.today() + timedelta(days=howOften)
                values_for_changing_date = (next_date, user_id_for_third_query)
                fourth_cursor = db.cursor(buffered=True)
                fourth_cursor.execute(update_sql, values_for_changing_date)
                fourth_cursor.close()
                db.commit()

            elif unpackedDate < date.today(): #if the table is outdated
                print("Date smaller than current date triggered for", user_id_for_third_query)
                get_goal_entry = "SELECT goal, status, user_id, server_id FROM goal WHERE user_id = %s"  # request for the users goals in the goals table
                user_request = (user_id_for_third_query,)
                third_cursor = db.cursor(buffered=True)
                third_cursor.execute(get_goal_entry, user_request)  # execute sql query
                third_results = third_cursor.fetchall()
                status_counter = 0
                for (
                    fullEntry
                ) in third_results:  # loop the the results of the latest query
                    goal,status,idByMember,serverByMember = fullEntry #assign the variables returned
                    find_channel_id = int(serverByMember) # variable used for finding the channel, it is the server id
                    global_server_id = int(serverByMember) # used for getting the server object later on
                    try:
                        member_object = bot.get_user(int(idByMember))
                    except:
                        member_object = f'User mention failed {user_id_for_third_query}'
                        print('Issue occured, none was returned as member_object as shown here', member_object)
                    if status == 1:
                        goals += f'{green_tick_emoji} `{goal}`\n'
                        status_counter +=1
                    elif status == 0:
                        goals += f'{slash_emoji} `{goal}`\n'
                get_reminder_channel = "SELECT reminder_channel_id FROM config WHERE server_id = %s"
                values = (find_channel_id,)
                third_cursor.execute(get_reminder_channel, values)
                third_results_again = third_cursor.fetchall()
                third_cursor.close()
                for unpacked_channel in third_results_again:
                    # unpack the channel id
                    reminder_channel_id_final, = unpacked_channel
                    reminder_channel_id_final = int(reminder_channel_id_final)
                    reminder_channel_found = True
                print("Reminder Channel Found:", reminder_channel_found)
                server = bot.get_guild(global_server_id)
                try:
                    reminder_channel_object = server.get_channel(reminder_channel_id_final)
                except:
                    print('MAY DAY MAY DAY, SOS, was unable to get reminder channel object')
                # print users goals to remind them
                if status_counter == 0:
                    send_funny_text = random.choice(reminder_funny_text)
                    try:
                        await reminder_channel_object.send(f"{member_object.mention}\n**{send_funny_text}**\n\n{goals}")  # print the users goals
                    except:
                        await reminder_channel_object.send(
                            f"{member_object}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                elif status_counter == 1:
                    send_funny_text = random.choice(reminder_for_one_achieved)
                    try:
                        await reminder_channel_object.send(
                            f"{member_object.mention}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                    except:
                        await reminder_channel_object.send(
                            f"{member_object}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                elif status_counter == 2:
                    send_funny_text = random.choice(reminder_for_two_achieved)
                    try:
                        await reminder_channel_object.send(
                            f"{member_object.mention}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                    except:
                        await reminder_channel_object.send(
                            f"{member_object}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                elif status_counter > 2:
                    send_funny_text = random.choice(reminder_for_three_plus_achieved)
                    try:
                        await reminder_channel_object.send(
                            f"{member_object.mention}\n**{send_funny_text}**\n\n{goals}"
                            ) # print the users goals
                    except:
                        await reminder_channel_object.send(
                            f"{member_object}\n**{send_funny_text}**\n\n{goals}"
                            )  # print the users goals
                goals = "" # reset goals variable
                update_sql = "UPDATE next_reminder SET next_date = %s WHERE user_id = %s"
                next_date = date.today() + timedelta(days=howOften)
                values_for_changing_date = (next_date, user_id_for_third_query)
                fourth_cursor = db.cursor(buffered=True)
                fourth_cursor.execute(update_sql, values_for_changing_date)
                fourth_cursor.close()
                db.commit()
    disconnect(cursor,db)