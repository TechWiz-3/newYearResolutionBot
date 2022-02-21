# Created by #Zac the Wise#1381 with help from #iamkneel#2359

# Update created by Zac on 22/Feb

# made everything global slash commands

# Version 3.4.1

import asyncio
from optparse import Values
from discord.commands import Option
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import date, timedelta
from discord.utils import get
from discord.commands import permissions
import discord
import random

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")
DEV_GUILD_ID = 864438892736282625
PROD_GUILD_ID = 867597533458202644

"""
----Remember to commit any DB changes----

Global variables:
memberObject - for reminder function
"""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="goals!", intents=intents)

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
specific_goal_deleted = ["Can someone explain why?", "Who deletes their goals huh", "You just deleted a goal bruh, better make it up by adding two more", "Insane", "What is the meaning of life????? Humans make me doubt myself :rolling_eyes:"]
all_goals_deleted = ["WTH THIS PEEP IS CRAZY", "Dude is on a KILLING RAMPAGE", "Somebody get the police, dude just deleted all his goals", "If you don't got goals you can't achieve em"]
reminder_deleted = ["Oh no, why did you delete your reminder T_T", "He deleted his reminders :(", "Man doesn't want to be reminded anymore?? Is this real??"]
reminder_channel_success_response = ["THAT'S THE WAY TO GO", "yeah boi", "now, let's get this show started", "great start bois n gorls", "xD", "lez get it now"]

@bot.event
async def on_ready():
    await initialise_loop()
    await reminder_function.start()
    while True:
        # alternate between two bot statuses 
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you achieve your goals"))
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="get started | /help"))
        await asyncio.sleep(5)

@bot.event
async def on_guild_join(guild):
    server = bot.get_guild(864438892736282625)
    log = server.get_channel(866217361115316284)
    await log.send(f"New server joined\n{guild.id}\n{guild.member_count}\n{guild.name}")

@bot.slash_command()
async def help(ctx):
    """Helps you use the bots commands"""
    embed=discord.Embed(title="About Me", description="I'm a bot specifically created for Gravity Destroyers. My purpose is simple:\n<:agreentick:875244017833639956> Log users goals\n<:agreentick:875244017833639956> Remind users about their goals\n<:agreentick:875244017833639956> Help motivate and remind users to keep working at and achieve their goals :muscle:")
    embed.add_field(name="Config Reminder Channel Command", value=":warning: **Extremely important command.**\nWithout setting a channel, the reminder function won't work. To use this command, type `/config_reminder_channel` and enter the channel you in your server you wish to for goal reminders.", inline=False)
    embed.add_field(name="New Year Goal Command", value="To use this command, type `/new_year_goal` and click space, enter or tab, then type in your goal, type one goal at a time and keep it to raw text.", inline=False)
    embed.add_field(name="View Goals Command", value="To use this command, type `/view_goals`", inline=False)
    embed.add_field(name="View Ids Command", value="To use this command, type `/view_ids`. Each goal will be displayed with it's corresponding ID in bold.", inline=False)
    embed.add_field(name="Goal Achieved Command", value="To use this command, type `/goal_achieved` then press tab and enter the ID corresponding to the goal you wish to mark as achieved.", inline=False)
    embed.add_field(name="Remind Me Command", value="This command instructs the bot to remind you of your goals. To use it type `/remind_me` then press tab and enter how often you wish to be reminded of your goals in days.", inline=False)
    embed.add_field(name="Stop Reminding Commnad", value="This command stops the bot from reminding you about your goals, to use it type `/stop_reminding`", inline=False)
    embed.add_field(name="Clear Goals Command", value="Removes all logged goals and reminders OR a single goal and leaves reminders. To delete all goals, type `/clear_goals`. To delete a specific goal type `/clear_goals id` the ID should be that of the goal you wish to delete, to get the ID’s for your goals type `/view_ids`", inline=False)
    embed.add_field(name="Edit Goal Command", value="This command edits a goal based on it’s ID. To use this command type `/edit_goal id newgoal`", inline=False)
    embed.add_field(name = "Next Reminder Command", value = "Shows you when your next goal reminder is. To use this command type `/next_reminder`", inline =False)
    embed.add_field(name = "Change Reminder Interval Command", value = "Allows you to change how often you are reminded in days `/change_reminder_interval days`", inline=False)
    await ctx.respond(embed=embed)

@bot.event
async def on_application_command_error(ctx, error): # if slash command error occurs
    await ctx.send(f":weary: {error}") # send the error

@bot.slash_command(default_permissions = False)
@permissions.is_owner()
@permissions.permission(user_id = 760345587802964010)
async def config_reminder_channel(ctx, reminder_channel: Option(discord.TextChannel, "Reminder channel", required = True)):
    server_logged = False
    get_servers_config = "SELECT server_id FROM config WHERE server_id = %s" # checks if the server is in the config table
    values = (ctx.guild.id,)
    cursor.execute(get_servers_config, values)
    for entry in cursor:
        server_logged = True
    if server_logged == True:
        await ctx.respond("You server is already logged in my table, I'm updating the channel for you :)")
        insert_reminder_channel = "UPDATE config SET reminder_channel_id = %s WHERE server_id = %s"
        values = (str(reminder_channel.id), str(ctx.guild.id))
        cursor.execute(insert_reminder_channel, values)
        db.commit()
        await ctx.send(f"<:agreentick:875244017833639956> Sucess {random.choice(reminder_channel_success_response)}")
    elif server_logged == False:
        insert_reminder_channel = "INSERT INTO config (server_id, reminder_channel_id) VALUES (%s, %s)"
        values = (str(ctx.guild.id), str(reminder_channel.id))
        cursor.execute(insert_reminder_channel, values)
        db.commit()
        await ctx.respond(f"<:agreentick:875244017833639956> Sucess {random.choice(reminder_channel_success_response)}")

@bot.slash_command()
async def new_year_goal(ctx, *, goal: Option(str, "Type the name of the goal (one only)", required=True)):
    """Log a goal, one at a time"""
    person = str(ctx.author) # get name
    personId = str(ctx.author.id) # get id
    serverId = str(ctx.guild.id) # get server id and assign it as a string
    status = False # set status if achieved to false
    duplicate_existant = False
    # check if the new goal is a duplicate
    check_goals = "SELECT * FROM 2022_Goals WHERE user = %s AND goals = %s" # checks for a goal from the user
    values = (person, goal)
    cursor.execute(check_goals, values)
    for entry in cursor: # loop through the results if they exist
        duplicate_existant = True # confirm through this variable that another duplicate exists
        print(entry)
    if duplicate_existant == False:
        finalValues = (person, goal, status, personId, serverId)
        insertGoals = "INSERT INTO 2022_Goals (user, goals, status, userId, serverId) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insertGoals, finalValues) # execute
        db.commit()
        await ctx.respond(
            f"Yessir\nYour goal is `{goal}`\n**I've logged it for you, NOW LET'S GO GET IT <:lezgooo:923128327970099231>**\nOh and also, remember to do `/remind_me` to let me know how often to remind you about it!"
            )
    elif duplicate_existant == True:
        await ctx.respond("Wowa, steady on there. This goal is seems to be a duplicate of another, if you wish to remove a goal use the `/edit_goal` command.")

@bot.slash_command()
async def remind_me(ctx, *, days: Option(int, "Enter how often you'd like to be reminded in days", required=True)):  # time in days
    """Tells the bot to remind you about your goals every x days"""
    goalsSet = False # automatically assume that goals haven't been set
    checkGoals = "SELECT * FROM 2022_Goals WHERE user = %s" # check if goals have been set
    values = (str(ctx.author),) # get the users name
    cursor.execute(checkGoals, values) # execute
    for entry in cursor: # loop through results if there are any
        goalsSet = True # goals indeed have been set
    if goalsSet == True: # go ahead to next check
        reminderSetPreviously = False # assume that a reminder has not been set before
        getReminders = "SELECT days FROM reminders WHERE user = %s" # find reminders set previously
        values = (str(ctx.author),) # users name
        second_cursor.execute(getReminders, values) # execute
        for reminder in second_cursor: # loop through results if they exist
            reminderSetPreviously = True # reminder has been set prevously
        if reminderSetPreviously == True: # reminder has been set previously
            # tell them off
            await ctx.respond(
                "MATE, like BRUH lmao :joy:\nYou've already set a reminder, are you trying to break me?\nBut what you can do... is reset your reminder time with `/change_reminder_interval`. Also if you don't wish to be reminded type `/stop_reminding`"
                    )
        else: # if reminder hasn't been set previously
            # finally execute remind me command
            setReminder = "INSERT INTO reminders (user, days) VALUES (%s, %s)" # insert days interval
            values = (str(ctx.author), days)
            cursor.execute(setReminder, values) # execute
            # set next reminder to today
            nextReminder = str(date.today()).replace(",", "-").replace(" ", "") # do i even need all the replace replace
            values = (str(ctx.author), nextReminder)
            # insert date into db
            setDate = "INSERT INTO nextDateReminder (user, next_date) VALUES (%s, %s)"
            cursor.execute(setDate, values)
            db.commit()
            await ctx.respond(
                f"Going to be reminding you every `{days}`\nTo check your next reminder `/next_reminder`\n\n*Good job bruh, now time to get to work <:stronk_doge:925285801921769513> <:lezgooo:925286931221344256> If you need help, we got you <#867600399879372820>*"
            )
    elif goalsSet == False: # if goals haven't been set
            await ctx.respond(
            "Well it's great that you want to be reminded, but make sure you set goals first `/new_year_goal` :grin:"
            )

@bot.slash_command()
async def view_goals(ctx):
    """Displays your currently logged and achieved goals"""
    greenTickEmoji = discord.utils.get(bot.emojis, name="epicTick") # get a tick emoji
    slashEmoji = discord.utils.get(bot.emojis, name="aslash") # get a slash emoji
    goalsSet = False # variable that indicates that the user has sett their goals
    goals_message_list = ""
    goalsCounter = 0 # how many goals
    goalsAchievedCounter = 0 # how many goals have been achieved
    author = (str(ctx.author),)
    # get the users goals, status represents whether the goal has been achieved or not
    getGoals = "SELECT goals, status FROM 2022_Goals WHERE user = %s"
    cursor.execute(getGoals, author) # get each goal and corresponding status for the user
    for goalAndStatus in cursor: # loop through results
        goal,status = goalAndStatus # assign the results
        goalsSet = True # user has set their goals
        goalsCounter += 1 # increment the goals looped through
        if status == 1: # if goal achieved
            goals_message_list += f"{greenTickEmoji} `{goal}`\n"
            goalsAchievedCounter += 1
        elif status == 0: # if goal not achieved
            goals_message_list += f"{slashEmoji} `{goal}`\n"
    if goalsAchievedCounter > 0:
        await ctx.respond(
            f"Your goals are...\n\n{goals_message_list}\n**<:pepe_hypers:925274715214458880> You have achieved __{goalsAchievedCounter}__ out of __{goalsCounter}__ goals**\nKEEP GRINDING <:pepebuff:874499841407983647> <:pepebuff:874499841407983647>"
        )
    elif goalsSet == True:
        await ctx.respond(
            f"Your goals are...\n\n{goals_message_list}\nYou haven't achieved any of your {goalsCounter} goals, but that doesn't matter, **TRAIN HARD TRAIN SMART** (that's what Gravity Destroyers is for) and you'll get there <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>"
        )
    elif goalsSet == False: # respond to user that hasn't set goals
        await ctx.respond("Ummm, you need to set your goals first before viewing them lol\n\n*However, I live go serve bright human ;) ... these commands may help...* `/help` `/new_year_goal`")

@bot.slash_command()
async def view_ids(ctx):
    """Displays each logged called and it's unique ID to access"""
    final_message = ""
    author = (str(ctx.author),) # gets the command invoker
    sql = "SELECT goals, id FROM 2022_Goals WHERE user = %s" # searches the table for goals and ids with the user's name
    cursor.execute(sql, author)
    for entry in cursor: # loop through results
        goal, goal_id = entry # unpack results
        final_message = final_message + f"**{goal}** `{goal_id}`\n" # add to the final message the goal and goal id
    await ctx.respond(final_message) # send the final list


@bot.slash_command()
async def goal_achieved(ctx, id: Option(int, "Enter the ID of the goal you wish to mark as achieved", required=True)):
    """Log when you achieve a goal by goal ID"""
    userGoalIdVerified = False
    achieved_goal_name = ""
    fetchByID = (id,)
    cursor.execute("SELECT user, goals FROM 2022_Goals WHERE id = %s", fetchByID) # finds the goal corresponding to provided id
    for userandGoal in cursor: # loops through results
        user, goal = userandGoal # unpacks the resuts
        if user == str(ctx.author): # if the user of the requested goal is equal to the command invoker
            userGoalIdVerified = True # this right user
            achieved_goal_name = goal # gets the text of the goal
    if userGoalIdVerified == True: # if the user is correct
        value = (id,)
        markAchieved = "UPDATE 2022_Goals SET status = '1' WHERE id = %s"
        cursor.execute(markAchieved, value)
        db.commit()
        await ctx.respond(
            f"**Congratulations...**\n<:pepe_hypers:925274715214458880> You have ACHIEVED `{achieved_goal_name}`\n**Collect your trophy:**\n:trophy:"
            )
    elif userGoalIdVerified == False: # if it's the wrong user
        await ctx.respond(
            "Hmm, something sus be going on here, maybe you made an error with the id? I'm not sure... but I wasn't able to log the goal as achieved T_T"
                )

async def initialise_loop():
    # get each server and send a message to it's reminder channel
    get_servers_and_channels = "SELECT server_id, reminder_channel_id FROM config"
    cursor.execute(get_servers_and_channels)
    for entry in cursor:
        server_id, reminder_channel_id = entry
        print("Init loop; server id: ", reminder_channel_id)
        server = bot.get_guild(int(server_id))
        reminder_channel = server.get_channel(int(reminder_channel_id))
        await reminder_channel.send("Initialising...")

@tasks.loop(minutes = 2.0)
async def reminder_function():
    print("I'm running")
    goals = ""
    find_channel_id = 0
    reminder_channel_found = False
    reminder_channel_id_final = 0
    global_server_id = 0
    reminderChannelObject = None
    sql = "SELECT user, days FROM reminders"  # select the username and their selected reminder interval
    cursor.execute(sql)  # execute sql query
    for (username, howOften) in cursor:  # loop through the results of the sql query
        sql = "SELECT user, next_date FROM nextDateReminder WHERE user = %s"
        value = (username,)
        second_cursor.execute(sql, value)
        for dateEntry in second_cursor:
            userForThirdQuery, unpackedDate = dateEntry
            slashEmoji = discord.utils.get(bot.emojis, name="aslash")
            greenTickEmoji = discord.utils.get(bot.emojis, name="epicTick")
            if unpackedDate == date.today():
                get_goal_entry = "SELECT goals,status,userId,serverId FROM 2022_Goals WHERE user = %s"  # request for the users goals in the goals table
                userRequest = (userForThirdQuery,)
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
                        memberObject = f'User mention failed {userForThirdQuery}'
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
                    await reminderChannelObject.send(f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}")  # print the users goals
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
                updateSql = "UPDATE nextDateReminder SET next_date = %s WHERE user = %s"
                nextDate = date.today() + timedelta(days=howOften)
                valuesForChangingDate = (nextDate, userForThirdQuery)
                fourth_cursor.execute(updateSql, valuesForChangingDate)
                db.commit()

            elif unpackedDate < date.today(): #if the table is outdated
                print("Date smaller than current date triggered for", userForThirdQuery)
                get_goal_entry = "SELECT goals,status,userId,serverId FROM 2022_Goals WHERE user = %s"  # request for the users goals in the goals table
                userRequest = (userForThirdQuery,)
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
                        memberObject = f'User mention failed {userForThirdQuery}'
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
                    await reminderChannelObject.send(f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}")  # print the users goals
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
                updateSql = "UPDATE nextDateReminder SET next_date = %s WHERE user = %s"
                nextDate = date.today() + timedelta(days=howOften)
                valuesForChangingDate = (nextDate, userForThirdQuery)
                fourth_cursor.execute(updateSql, valuesForChangingDate)
                db.commit()

@bot.slash_command()
async def clear_goals(ctx, id: Option(int, "Enter the ID of the goal you wish to delete", required=False)):
    """Delete all logged goals, or a specific goal based on ID"""
    if id == None:
        deleteGoals = "DELETE FROM 2022_Goals WHERE user = %s"
        deleteReminderEntries = "DELETE FROM reminders WHERE user = %s"
        deleteDateReminderEntries = "Delete FROM nextDateReminder WHERE user = %s"
        user = (str(ctx.author),)
        cursor.execute(deleteGoals, user)
        cursor.execute(deleteReminderEntries, user)
        cursor.execute(deleteDateReminderEntries, user)
        db.commit()
        await ctx.respond(
            f"All goals deleted. {random.choice(all_goals_deleted)}\nNow time to put new ones in `/new_year_goal`\n*Also, your reminders have been removed*"
            )
    else:
        userAndIdMatch = False
        getUserFromGoal = "SELECT user FROM 2022_Goals WHERE id = %s"
        values = (id,)
        cursor.execute(getUserFromGoal, values)
        for goalEntry in cursor:
            userOfGoal, = goalEntry
            if userOfGoal == str(ctx.author):
                userAndIdMatch = True
        if userAndIdMatch == True:
            sql = "DELETE FROM 2022_Goals WHERE user = %s AND id = %s"
            user = str(ctx.author)
            goalId = int(id)
            values = (user, goalId)
            cursor.execute(sql, values)
            db.commit()
            await ctx.respond(
                f"Specific goal deleted {random.choice(specific_goal_deleted)}"
                )
        else:
            policeEmoji = discord.utils.get(bot.emojis, name="pepe_police")
            await ctx.respond(
                f"Wow, you trying to delete somebody elses goals? That's malicious dude {policeEmoji} <:angry_pepe_ak47:930283816143171604>\n||If not that means you put the wrong ID||"
            )   

@bot.slash_command()
async def stop_reminding(ctx):
    """Stops the bot from reminding you about your goals"""
    deleteReminderEntries = "DELETE FROM reminders WHERE user = %s"
    deleteDateReminderEntries = "Delete FROM nextDateReminder WHERE user = %s"
    user = (str(ctx.author),)
    cursor.execute(deleteReminderEntries, user)
    cursor.execute(deleteDateReminderEntries, user)
    db.commit()
    await ctx.respond(
        f"{random.choice(reminder_deleted)}\nDo `/remind_me` again to change the interval. If not then we're sad to see you go... all the best"
    )

@bot.slash_command()
async def change_reminder_interval(ctx, how_often: Option(int, "Enter how often in days you wish to be reminded", required=True)):
    """Adjusts how often you're reminded of your goals"""
    adjustInterval = "UPDATE reminders SET days = %s WHERE user = %s"
    values = (how_often, str(ctx.author))
    cursor.execute(adjustInterval, values)
    adjustIntervalDate = "UPDATE nextDateReminder SET next_date = %s WHERE user = %s"
    values = (
        str(date.today()),
        str(ctx.author)
        )
    cursor.execute(adjustIntervalDate, values)
    db.commit()
    cooldoge = discord.utils.get(bot.emojis, name="cooldoge")
    await ctx.respond(
        f"{cooldoge} Well, that went well. Your interval is now `{how_often}` day(s). Achievement time babyy"
        )

@bot.slash_command()
async def next_reminder(ctx):
    """Shows you how often you'll be reminded as well as your next reminder date"""
    reminderSet = False
    howOften = 0
    nextDate = None
    getReminderInterval = "SELECT days FROM reminders WHERE user = %s"
    values = (str(ctx.author),)
    cursor.execute(getReminderInterval, values)
    for entry in cursor:
        reminderSet = True
        howOften, = entry
    getNextReminderDate = "SELECT next_date FROM nextDateReminder WHERE user = %s"
    second_cursor.execute(getNextReminderDate, values)
    for dateEntry in second_cursor:
        nextDate, = dateEntry
    if reminderSet == True:
        await ctx.respond(
            f"You have set to be reminded every `{howOften}` day(s) and your next reminder is on `{nextDate}` meanwhile... KEEP GRINDING <:lezgooo:925286931221344256>"
            )    
    elif reminderSet == False:
        umEmoji = discord.utils.get(bot.emojis, name="um")
        await ctx.respond(
            f"{umEmoji} you need to set a reminder first before viewing it... `/remind_me`"
            )

@bot.slash_command()
async def get_started(ctx):
    """Helps you get started :)"""
    contentOne = "||**This is how I help you:**\n`/help` The help command is your go to command to understand anything, but here's the recommended sequence of commands:||"
    contentTwo = "||Run**`/new_year_goal`** for **each** new year goal you wish to achieve.\nRun **`/view_goals`** to ensure that all your goals havee been logged.\nRun **`/remind_me`** to set how often you'll be reminded.||"
    contentThree = "||For more command use the `/help` command. If you enounter any issues pls ping `@Zac the Wise#1381` :)||"

    await ctx.respond(
        f"Ayo {ctx.author.mention} so you want to get after those goals and make this year, YOUR year. Well GOOD NEWS, I'm here to help...\n{contentOne}\n{contentTwo}\n{contentThree}"
        )

@bot.slash_command()
async def edit_goal(ctx, id: Option(int, "Enter the ID corresponding to the goal you wish to change"), newtext: Option(str, "Enter the new goal you'd like to set")):
    """Edits a goal entry based on ID"""
    goalIsForUser = False
    checkGoalAndId = "SELECT user FROM 2022_Goals WHERE id = %s"
    values = (id,)
    cursor.execute(checkGoalAndId, values)
    for usernameEntry in cursor:
        user, = usernameEntry
        if user == str(ctx.author):
            goalIsForUser = True
    if goalIsForUser == True:
        changeGoal = "UPDATE 2022_Goals SET goals = %s WHERE user = %s AND id = %s"
        values = (newtext, str(ctx.author), id)
        cursor.execute(changeGoal, values)
        db.commit()
        await ctx.respond(f"Perfect, you've replaced goal `{id}` with the text `{newtext}`")
    else:
        await ctx.respond("Something sus here bruh, idk what it is tho, maybe the ID you put is wrong?")

@bot.event
async def on_user_update(before, after):
    if before.name == after.name and before.discriminator == after.discriminator: # if the name and the discriminator is the same which means they haven't been changed
        # username not changed and # discrim not changed
        pass
    elif before.name != after.name or before.discriminator != after.discriminator:
        member_in_goals = False
        member_in_reminders = False
        old_name = f"{before.name}#{before.discriminator}"
        new_name = f"{after.name}#{after.discriminator}"
        print(old_name)
        print(new_name)
        check_member = "SELECT * FROM 2022_Goals WHERE user = %s"
        values = (old_name,)
        cursor.execute(check_member, values)
        for entry in cursor: # run through the results
            member_in_goals = True # the member is in the goals table
        if member_in_goals == True:
            update_table = "UPDATE 2022_Goals SET user = %s WHERE user = %s" # update with new name where old name
            values = (new_name, old_name)
            cursor.execute(update_table, values) # excecute sql
            # since goals are set we need to check the reminders table to update those as well
            check_member_reminders = "SELECT * FROM reminders WHERE user = %s" # find any entries with users old name
            values = (old_name,)
            cursor.execute(check_member_reminders, values) # execute sql
            for entry in cursor: # loop through results
                member_in_reminders = True # confirm that the user has been found in the reminders table
            if member_in_reminders == True:
                # update both reminder tables with the users new name
                update_reminders = "UPDATE reminders SET user = %s WHERE user = %s"
                values = (new_name, old_name)
                cursor.execute(update_reminders, values)
                update_next_date_table = "UPDATE nextDateReminder SET user = %s WHERE user = %s"
                values = (new_name, old_name)
                cursor.execute(update_next_date_table, values)
                db.commit()
                await after.send(
                    "**Hi there,**\nyour profile change has been noted and updated in our goal and reminder tables\nAnyways... KEEP GRINDING <:lezgooo:923128327970099231><:lezgooo:923128327970099231><:lezgooo:923128327970099231>"
                        )
            elif member_in_reminders == False:
                print("Member not in reminders however is in goals table")
                await after.send(
                    "**Hi there,**\nyour profile change has been noted and updated in our goals table\nAnyways... KEEP GRINDING <:lezgooo:923128327970099231><:lezgooo:923128327970099231><:lezgooo:923128327970099231>"
                        )
        elif member_in_goals == False:
            print("User changed however not in goals table")
bot.run(BOT_TOKEN)
