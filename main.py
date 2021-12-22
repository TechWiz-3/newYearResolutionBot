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
    finalValues = (person, goal)
    sql = "INSERT INTO test_goals_2002 (user, goals) VALUES (%s, %s)"
    mycursor.execute(sql, finalValues)
    mydb.commit()
    #await asyncio.sleep(2628288)

@bot.slash_command(guild_ids=[864438892736282625, 867597533458202644])
async def remindme(ctx,*,days):#time in days
    await ctx.respond(f"Going to be reminding you every `{days}`\nGood job :trophy:")
    fullTimeInSeconds = days*86400
    while True:
        await asyncio.sleep(fullTimeInSeconds)
        mycursor.execute("SELECT * FROM railway ORDER BY name")
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

bot.run(token)