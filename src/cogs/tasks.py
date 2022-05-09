from discord.ext import tasks
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import date, timedelta
from discord.utils import get
import discord
import random

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")

db = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=PORT
)

cursor = db.cursor(buffered=True)
second_cursor = db.cursor(buffered=True)
third_cursor = db.cursor(buffered=True)
fourth_cursor = db.cursor(buffered=True)
fifth_cursor = db.cursor(buffered=True)

reminder_funny_text = ["The force wishes me to remind you of your goals, here they are.", "Did you think I'd let you forget about your goals? NOT A CHANCE", "How's it going mate?", "*Mighty presense decscends from sky to deliver a reminder to you*", "Ay bro, it's been some time, keep working at it", "Gravity Destroyers 2022 checking in with you"]
reminder_for_one_achieved = ["You've made the first step, now it's time for the second one <:lezgooo:925286931221344256>", "Hard work, smart work let's go <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>", "You got this baby, second goal achieve coming soon <:stronk_doge:925285801921769513>", "*Mighty presense decscends from sky to deliver a reminder to you*"]
reminder_for_two_achieved = ["Two goals achieved mate, the thirds gonna be a special one ;)", "Someones going for their 3rd goal this year <:lezgooo:925286931221344256>", "Third times a charm"]
reminder_for_three_plus_achieved = ["This mans on a roll, keep it going bro", "Did you think I'd let you forget about your goals? NOT A CHANCE. You've come THIS far, next goal let's go", "Accountability session king achiever howsit going?", "Sup warrior, time to check in :sunglasses:"]

@tasks.loop(minutes = 2.0)
async def reminder_function(bot):
    print("I'm running")
    goals = ""
    find_channel_id = 0
    reminder_channel_found = False
    reminder_channel_id_final = 0
    global_server_id = 0
    reminderChannelObject = None
    sql = "SELECT user_id, days FROM reminder"  # select the username and their selected reminder interval
    cursor.execute(sql)  # execute sql query
    for (user_id, howOften) in cursor:  # loop through the results of the sql query
        sql = "SELECT user_id, next_date FROM next_reminder WHERE user_id = %s"
        value = (user_id,)
        second_cursor.execute(sql, value)
        for dateEntry in second_cursor:
            user_id_for_third_query, unpackedDate = dateEntry
            slashEmoji = get(bot.emojis, name="aslash")
            greenTickEmoji = get(bot.emojis, name="epicTick")
            if unpackedDate == date.today():
                get_goal_entry = "SELECT user, goals, status, user_id, server_id FROM goal WHERE user_id = %s"  # request for the users goals in the goals table
                userRequest = (user_id_for_third_query,)
                third_cursor.execute(get_goal_entry, userRequest)  # execute sql query
                statusCounter = 0
                for (
                    fullEntry
                ) in third_cursor:  # loop the the results of the latest query
                    user,goal,status,idByMember,serverByMember = fullEntry #assign the variables returned
                    find_channel_id = int(serverByMember) # variable used for finding the channel, it is the server id
                    global_server_id = int(serverByMember) # used for getting the server object later on
                    try:
                        memberObject = bot.get_user(int(idByMember))
                    except:
                        memberObject = f'User mention failed <@{user_id_for_third_query}> i.e {user}'
                        print('Issue occured, none was returned as memberObject as shown here', memberObject)
                    if status == 1:
                        goals += f'{greenTickEmoji} `{goal}`\n'
                        statusCounter +=1
                    elif status == 0:
                        goals += f'{slashEmoji} `{goal}`\n'
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
                    reminderChannelObject = server.get_channel(reminder_channel_id_final)
                except:
                    print('MAY DAY MAY DAY, SOS, was unable to get reminder channel object')
                # print users goals to remind them
                if statusCounter == 0:
                    sendFunnyText = random.choice(reminder_funny_text)
                    try:
                        await reminderChannelObject.send(f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}")  # print the users goals
                    except:
                        await reminderChannelObject.send(
                            f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                elif statusCounter == 1:
                    sendFunnyText = random.choice(reminder_for_one_achieved)
                    try:
                        await reminderChannelObject.send(
                            f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                    except:
                        await reminderChannelObject.send(
                            f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                elif statusCounter == 2:
                    sendFunnyText = random.choice(reminder_for_two_achieved)
                    try:
                        await reminderChannelObject.send(
                            f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                    except:
                        await reminderChannelObject.send(
                            f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                elif statusCounter > 2:
                    sendFunnyText = random.choice(reminder_for_three_plus_achieved)
                    try:
                        await reminderChannelObject.send(
                            f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                            ) # print the users goals
                    except:
                        await reminderChannelObject.send(
                            f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                goals = "" # reset goals variable
                updateSql = "UPDATE next_reminder SET next_date = %s WHERE user_id = %s"
                nextDate = date.today() + timedelta(days=howOften)
                valuesForChangingDate = (nextDate, user_id_for_third_query)
                fourth_cursor.execute(updateSql, valuesForChangingDate)
                db.commit()

            elif unpackedDate < date.today(): #if the table is outdated
                print("Date smaller than current date triggered for", user_id_for_third_query)
                get_goal_entry = "SELECT goal, status, user_id, server_id FROM goal WHERE user_id = %s"  # request for the users goals in the goals table
                userRequest = (user_id_for_third_query,)
                third_cursor.execute(get_goal_entry, userRequest)  # execute sql query
                statusCounter = 0
                for (
                    fullEntry
                ) in third_cursor:  # loop the the results of the latest query
                    goal,status,idByMember,serverByMember = fullEntry #assign the variables returned
                    find_channel_id = int(serverByMember) # variable used for finding the channel, it is the server id
                    global_server_id = int(serverByMember) # used for getting the server object later on
                    try:
                        memberObject = bot.get_user(int(idByMember))
                    except:
                        memberObject = f'User mention failed {user_id_for_third_query}'
                        print('Issue occured, none was returned as memberObject as shown here', memberObject)
                    if status == 1:
                        goals += f'{greenTickEmoji} `{goal}`\n'
                        statusCounter +=1
                    elif status == 0:
                        goals += f'{slashEmoji} `{goal}`\n'
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
                    reminderChannelObject = server.get_channel(reminder_channel_id_final)
                except:
                    print('MAY DAY MAY DAY, SOS, was unable to get reminder channel object')
                # print users goals to remind them
                if statusCounter == 0:
                    sendFunnyText = random.choice(reminder_funny_text)
                    try:
                        await reminderChannelObject.send(f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}")  # print the users goals
                    except:
                        await reminderChannelObject.send(
                            f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                elif statusCounter == 1:
                    sendFunnyText = random.choice(reminder_for_one_achieved)
                    try:
                        await reminderChannelObject.send(
                            f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                    except:
                        await reminderChannelObject.send(
                            f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                elif statusCounter == 2:
                    sendFunnyText = random.choice(reminder_for_two_achieved)
                    try:
                        await reminderChannelObject.send(
                            f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                    except:
                        await reminderChannelObject.send(
                            f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                elif statusCounter > 2:
                    sendFunnyText = random.choice(reminder_for_three_plus_achieved)
                    try:
                        await reminderChannelObject.send(
                            f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                            ) # print the users goals
                    except:
                        await reminderChannelObject.send(
                            f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                            )  # print the users goals
                goals = "" # reset goals variable
                updateSql = "UPDATE next_reminder SET next_date = %s WHERE user_id = %s"
                nextDate = date.today() + timedelta(days=howOften)
                valuesForChangingDate = (nextDate, user_id_for_third_query)
                fourth_cursor.execute(updateSql, valuesForChangingDate)
                db.commit()