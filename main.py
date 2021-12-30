from typing import ValuesView
import discord
import asyncio
import random
import aiohttp
import json
from discord.utils import get
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import mysql.connector
import datetime
from itertools import cycle


load_dotenv()
token = os.getenv("token")
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")
port = os.getenv("port")

bot = commands.Bot(command_prefix="goals!")

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database,
  port=port
)
mycursor = mydb.cursor()
secondcursor = mydb.cursor()

@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def help(ctx):
    """Helps you use the bots commands"""
    await ctx.respond("**New Year Goal Command**\nTo use this command, type `/newyeargoal` and click space, enter or tab, then type in your goal, for best effect, type on goal at a time.")

@bot.slash_command(guild_ids=[864438892736282625])  # create a slash command for the supplied guilds
async def hello(ctx):
    """Say hello to the bot"""  # the command description can be supplied as the docstring
    await ctx.respond(f"Hello {ctx.author}!")

@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def newyeargoal(ctx,*,goal):
    """Log a goal, one at a time"""
    await ctx.respond(f"Yessir\nYour goal is `{goal}`\n**I've logged it for you, NOW LET'S GO GET IT <:lezgooo:923128327970099231>**\nOh and also, remember to do `/remindme` to let me know how often to remind you about it!")
    person = str(ctx.author)
    status = False
    finalValues = (person, goal, status)
    sql = "INSERT INTO 2022_Goals (user, goals, status) VALUES (%s, %s, %s)"
    mycursor.execute(sql, finalValues)
    mydb.commit()
    #await asyncio.sleep(2628288)

@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def remindme(ctx,*,days):#time in days
    """Tells the bot to remind you about your goals every x days"""
    fullTimeInSeconds = days*86400
    values = (str(ctx.author), days)
    sql = "INSERT INTO reminders (user, days) VALUES (%s, %s)"
    mycursor.execute(sql, values)
    mydb.commit()
    await ctx.respond(f"Going to be reminding you every `{days}`\n\n*Good job bruh, now time to get to work <:stronk_doge:925285801921769513> <:lezgooo:925286931221344256>*")
    
    # while True:
    #     await asyncio.sleep(fullTimeInSeconds)
    #     mycursor.execute("SELECT * FROM 2022_Goals ORDER BY user;")
    #     mydb.commit()

        #mysql fetch
        #remind person of their goals



@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def view_goals(ctx):
    """Displays your currently logged and achieved goals"""
    final = ""
    finalAchieved = ""
    goalsCounter = 0
    goalsAchievedCounter = 0
    author = (str(ctx.author),)
    print(author)
    sql = "SELECT goals FROM 2022_Goals WHERE user = %s"
    mycursor.execute("SELECT goals FROM 2022_Goals WHERE user = %s", (author))
    for x in mycursor:
        final += str(x)
        goalsCounter +=1
        #if achieved add a green tick to the message
        #add a counter to say that another goal has been achieved
    final = final.replace("(", "")
    final = final.replace(")", "")
    final = final.replace("\'", "``")
    final = final.replace(",", "\n")
    mycursor.execute("SELECT goals FROM 2022_Goals WHERE user = %s AND status = '1'", (author))
    for x in mycursor:
        finalAchieved += str(x)
        goalsAchievedCounter +=1
    print(goalsAchievedCounter)
    #check the status for each goal with the username
    if goalsAchievedCounter > 0:
        await ctx.respond(f"Your goals are...\n\n{final}\n**<:pepe_hypers:925274715214458880> You have achieved __{goalsAchievedCounter}__ out of __{goalsCounter}__ goals**\nKEEP GRINDING <:pepebuff:874499841407983647> <:pepebuff:874499841407983647>")
    else:
        await ctx.respond(f"Your goals are...\n\n{final}\nYou haven't achieved any of your {goalsCounter} goals, but that doesn't matter, **TRAIN HARD TRAIN SMART** (that's what Gravity Destroyers is for) and you'll get there <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>")
@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def view_ids(ctx):
    """Displays each logged called and it's unique ID to access"""
    author = str(ctx.author)
    print(author)
    final = ""
    author = (str(ctx.author),)
    print(author)
    sql = "SELECT goals, id FROM 2022_Goals WHERE user = %s"
    # query = sql + author
    # mycursor.execute(query)
    mycursor.execute("SELECT goals, id FROM 2022_Goals WHERE user = %s", (author))
    # mycursor.execute(sql, author)
    # mycursor.execute("SELECT goals, id FROM 2022_Goals WHERE user = %s", (author))
    # mycursor.execute(f"SELECT goals, id FROM 2022_Goals WHERE user = {author}")
    # mycursor.execute("SELECT goals, id FROM 2022_Goals WHERE user = %s." % (author))
    # mycursor.execute("SELECT goals, id FROM 2022_Goals WHERE user = author")
    # mycursor.execute("SELECT goa fruit (name, variety) VALUES (%s, %s)", (new_fruit, new_fruit_type));
    # mycursor.execute("SELECT * FROM 2022_Goals WHERE user = author")
    for x in mycursor:
        xx = str(x)
        xx = xx.replace(",", "  **")
        xx = xx.replace("'", "``")
        xx = xx.replace("(", "")
        xx = xx.replace(")", "**\n")
        final += str(xx)
    await ctx.respond(final)


@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def goal_achieved(ctx, id):
    """Log when you achieve a goal by goal ID"""
    final = ""
    fetchByID = tuple(id)
    mycursor.execute("SELECT goals FROM 2022_Goals WHERE id = %s", (fetchByID))
    for x in mycursor:
        print(x)
        xx = str(x)
        xx = xx.replace(",", " ")
        xx = xx.replace("'", "")
        xx = xx.replace("(", "")
        xx = xx.replace(")", "\n")
        final += str(xx)
    value = tuple(id) 
    print(value)
    sql = "UPDATE 2022_Goals SET status = '1' WHERE id = %s"
    mycursor.execute(sql, value)
    mydb.commit()
    await ctx.respond(f"**Congratulations...**\n<:pepe_hypers:925274715214458880> You have ACHIEVED `{final}`**Collect your trophy:**\n:trophy:")

@bot.command()
async def set_reminder(ctx, how_long, type_of_time,*,message):
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
        await ctx.respond("**You don't have the right permissions for that.**", ephemeral = True)
        return
    else:
        goals = ""
        sql = "SELECT user, days FROM reminders" #select the username and their selected reminder interval
        # while True:
        mycursor.execute(sql) #execute sql query
        for x in mycursor: #loop through the results of the sql query
            (username, howOften) = x #assign the username and reminder interval provided by x
            await asyncio.sleep(5) #sleep
            sql = "SELECT goals FROM 2022_Goals WHERE user = %s" #request for the users goals in the goals table
            userRequest = (username,)
            secondcursor.execute(sql, userRequest) #execute sql query
            for goal in secondcursor: #loop the the results of the latest query
                goal = str(goal)
                goal = goal.replace(",", " ")
                goal = goal.replace("'", "`")
                goal = goal.replace("(", "")
                goal = goal.replace(")", "\n")
                goals += goal
            await ctx.send(f'Your goals\n{goals}') #print the users goals
        await ctx.send("Done")

# @bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
# async def initialise(ctx):
#     if not ctx.author.guild_permissions.administrator:
#         await ctx.respond("**You don't have the right permissions for that.**", ephemeral = True)
#         return
#     else:
#         sql = "FROM "
#         await ctx.respond("done")


bot.run(token)