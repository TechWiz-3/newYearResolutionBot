import discord
import asyncio
import random
import aiohttp
import json
from discord.utils import get
import requests
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
import datetime


load_dotenv()
token = os.getenv("token")
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")
port = os.getenv("port")

bot = commands.Bot(command_prefix=".")

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
    await ctx.respond(f"Going to be reminding you every `{days}`\nGood job :trophy:")
    fullTimeInSeconds = days*86400
    while True:
        await asyncio.sleep(fullTimeInSeconds)
        mycursor.execute("SELECT * FROM 2022_Goals ORDER BY user;")
        mydb.commit()

        #mysql fetch
        #remind person of their goals

@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def wait_until(ctx, dt):
    # sleep until the specified datetime
    # while True:
    now = datetime.datetime.now()
    await ctx.respond(now)
    #     remaining = (dt - now).total_seconds()
    #     await asyncio.sleep(remaining)
    #     if remaining == 0:
    #         break


@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def view_goals(ctx):
    """Displays your currently logged and achieved goals"""
    final = ""
    author = (str(ctx.author),)
    print(author)
    sql = "SELECT goals FROM 2022_Goals WHERE user = %s"
    mycursor.execute("SELECT goals, id FROM 2022_Goals WHERE user = %s", (author))
    for x in mycursor:
        final += str(x)
        #if achieved add a green tick to the message
        #add a counter to say that another goal has been achieved
    final = final.replace("(", "")
    final = final.replace(")", "")
    final = final.replace("\'", "``")
    final = final.replace(",", "\n")
    #check the status for each goal with the username
    await ctx.respond(f"Your goals are...\n\n{final}\nYou have achieved x/y number of goals")

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
    await ctx.respond(f"**Congratulations...**\nYou have ACHIEVED `{final}`**Collect your trophy:**\n:trophy:")



@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def initialise(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("**You don't have the right permissions for that.**", ephemeral = True)
        return
    else:
        await ctx.respond("done")


bot.run(token)