# Created by #Zac the Wise#1381 with help from #iamkneel#2359

# Update created by Zac on 2/Jan

# Made bot less insulting

# Version 1.1.2

import asyncio
from discord.app.commands import Option
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import date, timedelta
from discord.utils import get
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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="goals!", intents=intents)

db = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=PORT
)

cursor = db.cursor(buffered=True)
secondcursor = db.cursor(buffered=True)
thirdcursor = db.cursor(buffered=True)
fourthCursor = db.cursor(buffered=True)
fifthCursor = db.cursor(buffered=True)

reminderFunnyText = ["The force wishes me to remind you of your goals, here they are.", "Did you think I'd let you forget about your goals? NOT A CHANCE", "How's it going mate?", "*Mighty presense decscends from sky to deliver a reminder to you*", "Ay bro, it's been some time, keep working at it", "Gravity Destroyers 2022 checking in with you"]
reminderForOneAchieved = ["You've made the first step, now it's time for the second one <:lezgooo:925286931221344256>", "Hard work, smart work let's go <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>", "You got this baby, second goal achieve coming soon <:stronk_doge:925285801921769513>", "*Mighty presense decscends from sky to deliver a reminder to you*"]
reminderForTwoAchieved = ["Two goals achieved mate, the thirds gonna be a special one ;)", "Someones going for their 3rd goal this year <:lezgooo:925286931221344256>", "Third times a charm"]
reminderForThreePlusAchieved = ["This mans on a roll, keep it going bro", "Did you think I'd let you forget about your goals? NOT A CHANCE. You've come THIS far, next goal let's go", "Accountability session king achiever howsit going?", "Sup warrior, time to check in :sunglasses:"]
specificGoalDeleted = ["Can someone explain why?", "Who deletes their goals huh", "You just deleted a goal bruh, better make it up by adding two more", "Insane", "What is the meaning of life????? Humans make me doubt myself :rolling_eyes:"]
allGoalsDeleted = ["WTH THIS PEEP IS CRAZY", "Dude is on a KILLING RAMPAGE", "Somebody get the police, dude just deleted all his goals", "If you don't got goals you can't achieve em"]

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def help(ctx):
    """Helps you use the bots commands"""
    await ctx.respond(
        "**New Year Goal Command**\nTo use this command, type `/newyeargoal` and click space, enter or tab, then type in your goal, type one goal at a time and keep it to raw text.\n\n**View Goals Command**\nTo use this command, type `/view_goals`\n\n**View Ids Command**\nTo use this command, type `/view_ids`. Each goal will be displayed with it's corresponding ID in bold.\n\n**Goal Achieved**\nTo use this command, type `/goal_achieved` then press tab and enter the ID corresponding to the goal you wish to mark as achieved.\n\n**Remind Me Command**\nThis command instructs the bot to remind you of your goals. To use it type `/remindme` then press tab and enter how often you wish to be reminded of your goals in days."
    )


@bot.slash_command(
    guild_ids=[DEV_GUILD_ID]
)  # create a slash command for the supplied guilds
async def hello(ctx):
    """Say hello to the bot"""  # the command description can be supplied as the docstring
    await ctx.respond(f"Hello {ctx.author}!")


@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def newyeargoal(ctx, *, goal):
    """Log a goal, one at a time"""
    await ctx.respond(
        f"Yessir\nYour goal is `{goal}`\n**I've logged it for you, NOW LET'S GO GET IT <:lezgooo:923128327970099231>**\nOh and also, remember to do `/remindme` to let me know how often to remind you about it!"
    )
    person = str(ctx.author)
    personId = str(ctx.author.id)
    status = False
    finalValues = (person, goal, status, personId)
    sql = "INSERT INTO 2022_Goals_Str (user, goals, status, userId) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, finalValues)
    db.commit()
    # await asyncio.sleep(2628288)


@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def remindme(ctx, *, days):  # time in days
    """Tells the bot to remind you about your goals every x days"""
    # fullTimeInSeconds = days * 86400
    values = (str(ctx.author), days)
    sql = "INSERT INTO reminders (user, days) VALUES (%s, %s)"
    cursor.execute(sql, values)

    nextReminder = str(date.today()).replace(",", "-").replace(" ", "")
    values = (str(ctx.author), nextReminder)
    print(values)
    print(type(values))
    sql = "INSERT INTO nextDateReminder (user, next_date) VALUES (%s, %s)"
    cursor.execute(sql, values)

    db.commit()
    await ctx.respond(
        f"Going to be reminding you every `{days}`\n\n*Good job bruh, now time to get to work <:stronk_doge:925285801921769513> <:lezgooo:925286931221344256>*"
    )


@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def view_goals(ctx):
    """Displays your currently logged and achieved goals"""
    goalsSet = False
    final = ""
    finalAchieved = ""
    goalsCounter = 0
    goalsAchievedCounter = 0
    author = (str(ctx.author),)
    print(author)
    sql = "SELECT goals FROM 2022_Goals_Str WHERE user = %s"
    cursor.execute(sql, (author))
    #if no goals send you need to add some goals
    for x in cursor:
        final += str(x)
        goalsCounter += 1
        # if achieved add a green tick to the message
        # add a counter to say that another goal has been achieved
    final = (
        final.replace("(", "").replace(")", "").replace("'", "``").replace(",", "\n")
    )
    cursor.execute(
        "SELECT goals FROM 2022_Goals_Str WHERE user = %s AND status = '1'", (author)
    )
    for x in cursor:
        goalsSet = True
        finalAchieved += str(x)
        goalsAchievedCounter += 1
    print(goalsAchievedCounter)
    # check the status for each goal with the username
    if goalsAchievedCounter > 0:
        await ctx.respond(
            f"Your goals are...\n\n{final}\n**<:pepe_hypers:925274715214458880> You have achieved __{goalsAchievedCounter}__ out of __{goalsCounter}__ goals**\nKEEP GRINDING <:pepebuff:874499841407983647> <:pepebuff:874499841407983647>"
        )
    elif goalsSet == True:
        await ctx.respond(
            f"Your goals are...\n\n{final}\nYou haven't achieved any of your {goalsCounter} goals, but that doesn't matter, **TRAIN HARD TRAIN SMART** (that's what Gravity Destroyers is for) and you'll get there <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>"
        )
    elif goalsSet == False:
        await ctx.respond("You need to set your goals first before viewing them -_-\n\n*However, I live go serve bright human... these commands may help...* `/help` `/newyeargoal`")


@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def view_ids(ctx):
    """Displays each logged called and it's unique ID to access"""
    author = str(ctx.author)
    print(author)
    final = ""
    author = (str(ctx.author),)
    print(author)
    sql = "SELECT goals, id FROM 2022_Goals_Str WHERE user = %s"
    cursor.execute(sql, (author))
    for x in cursor:
        xx = (
            str(x)
            .replace(",", "  **")
            .replace("'", "``")
            .replace("(", "")
            .replace(")", "**\n")
        )
        final += str(xx)
    await ctx.respond(final)


@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def goal_achieved(ctx, id):
    """Log when you achieve a goal by goal ID"""
    final = ""
    fetchByID = tuple(id)
    cursor.execute("SELECT goals FROM 2022_Goals_Str WHERE id = %s", (fetchByID))
    for x in cursor:
        print(x)
        xx = (
            str(x)
            .replace(",", " ")
            .replace("'", "")
            .replace("(", "")
            .replace(")", "\n")
        )
        final += str(xx)
    value = tuple(id)
    print(value)
    sql = "UPDATE 2022_Goals_Str SET status = '1' WHERE id = %s"
    cursor.execute(sql, value)
    db.commit()
    await ctx.respond(
        f"**Congratulations...**\n<:pepe_hypers:925274715214458880> You have ACHIEVED `{final}`**Collect your trophy:**\n:trophy:"
    )


@bot.command()
async def set_reminder(ctx, how_long, type_of_time, *, message):
    how_long = int(how_long)
    if type_of_time.lower() == "h" or "hour" in type_of_time.lower():
        finalTime = how_long * 3600
        await asyncio.sleep(int(finalTime))
        await ctx.send(f"reminder set will be waiting for {finalTime} seconds")
    if type_of_time.lower() == "d" or "day" in type_of_time.lower():
        finalTime = how_long * 86400
        await asyncio.sleep(int(finalTime))
        await ctx.send(f"reminder set will be waiting for {finalTime} seconds")
    if type_of_time.lower() == "m" or "minute" in type_of_time.lower():
        finalTime = how_long * 60
        await asyncio.sleep(int(finalTime))
        await ctx.send(f"reminder set will be waiting for {finalTime} seconds")


@bot.command()
async def initialise(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(
            "**You don't have the right permissions for that.**", ephemeral=True
        )
        return
    counter = 0
    while True:
        goals = ""
        sql = "SELECT user, days FROM reminders"  # select the username and their selected reminder interval
        cursor.execute(sql)  # execute sql query
        for (username, howOften) in cursor:  # loop through the results of the sql query
            sql = "SELECT user, next_date FROM nextDateReminder WHERE user = %s"
            value = (username,)
            secondcursor.execute(sql, value)
            for dateEntry in secondcursor:
                userForThirdQuery, unpackedDate = dateEntry
                server = bot.get_guild(864438892736282625)
                reminderChannel = server.get_channel(869508676581466112)
                slashEmoji = discord.utils.get(bot.emojis, name="aslash")
                greenTickEmoji = discord.utils.get(bot.emojis, name="epicTick")

                if unpackedDate == date.today():
                    sql = "SELECT goals,status,userId FROM 2022_Goals_Str WHERE user = %s"  # request for the users goals in the goals table
                    userRequest = (userForThirdQuery,)
                    thirdcursor.execute(sql, userRequest)  # execute sql query
                    statusCounter = 0
                    global memberObject
                    for (
                        goalAndStatus
                    ) in thirdcursor:  # loop the the results of the latest query
                        goal,status,idByMember = goalAndStatus #assign the variables returned
                        idByMember = int(idByMember)
                        try:
                            memberObject = bot.get_user(int(idByMember))
                        except:
                            memberObject = f'User mention failed {userForThirdQuery}'
                            print('Issue occured, none was returned as memberObject as shown here', memberObject)
                        if status == 1:
                            goals += f'{greenTickEmoji} `{goal}`\n'
                            statusCounter+=1
                        elif status == 0:
                            goals += f'{slashEmoji} `{goal}`\n'   
                    if statusCounter == 0:
                        sendFunnyText = random.choice(reminderFunnyText)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter == 1:
                        sendFunnyText = random.choice(reminderForOneAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter == 2:
                        sendFunnyText = random.choice(reminderForTwoAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter > 2:
                        sendFunnyText = random.choice(reminderForThreePlusAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    goals = "" #reset goals variable
                    # insertSql = "INSERT INTO nextDateReminder (user, next_date) VALUES (%s, %s)"
                    updateSql = "UPDATE nextDateReminder SET next_date = %s WHERE user = %s"
                    nextDate = date.today() + timedelta(days=howOften)
                    valuesForChangingDate = (nextDate, userForThirdQuery)
                    fourthCursor.execute(updateSql, valuesForChangingDate)
                    db.commit()
                    await ctx.send("**End of mighty reminder message**")
                elif unpackedDate < date.today(): #if the table is outdated
                    print("Date smaller than current date triggered for", userForThirdQuery)
                    sql = "SELECT goals,status,userId FROM 2022_Goals_Str WHERE user = %s"  # request for the users goals in the goals table
                    userRequest = (userForThirdQuery,)
                    thirdcursor.execute(sql, userRequest)  # execute sql query
                    statusCounter = 0
                    for (
                        goalAndStatus
                    ) in thirdcursor:  # loop the the results of the latest query
                        goal,status,idByMember = goalAndStatus #assign the variables returned
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
                    #print users goals to remind them
                    if statusCounter == 0:
                        sendFunnyText = random.choice(reminderFunnyText)
                        await reminderChannel.send(f"{sendFunnyText}\n{goals}")  # print the users goals
                    elif statusCounter == 1:
                        sendFunnyText = random.choice(reminderForOneAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter == 2:
                        sendFunnyText = random.choice(reminderForTwoAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter > 2:
                        sendFunnyText = random.choice(reminderForThreePlusAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                ) # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    goals = "" #reset goals variable
                    updateSql = "UPDATE nextDateReminder SET next_date = %s WHERE user = %s"
                    nextDate = date.today() + timedelta(days=howOften)
                    valuesForChangingDate = (nextDate, userForThirdQuery)
                    fourthCursor.execute(updateSql, valuesForChangingDate)
                    db.commit()
                    await ctx.send("**End of mighty reminder message**")
        
        await asyncio.sleep(120)

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])#id: Option(str "Enter the goal id if you wish to remove a goal")
async def clear_goals(ctx, id: Option(int, "Enter the ID of the goal you wish to delete", required=False)):
    """Delete all logged goals, or a specific goal based on ID"""
    #sql = "SELECT goals FROM 2022_Goals_Str WHERE us"
    if id == None:
        sql = "DELETE FROM 2022_Goals_Str WHERE user = %s"
        user = (str(ctx.author),)
        cursor.execute(sql, user)
        db.commit()
        await ctx.respond(
            f"All goals deleted. {allGoalsDeleted}\nNow time to put new ones in `/newyeargoal`"
            )
    else:
        sql = "DELETE FROM 2022_Goals_Str WHERE user = %s AND id = %s"
        user = str(ctx.author)
        goalId = int(id)
        values = (user, goalId)
        cursor.execute(sql, values)
        db.commit()
        await ctx.respond(
            f"Specific goal deleted {specificGoalDeleted}"
            )

bot.run(BOT_TOKEN)
