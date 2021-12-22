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

@bot.slash_command(guild_ids=[864438892736282625])
async def help(ctx):
    """Helps you use the bots commands"""
    await ctx.respond("**New Year Goal Command**\nTo use this command, type `/newyeargoal` and click space, enter or tab, then type in your goal, for best effect, type on goal at a time.")

@bot.slash_command(guild_ids=[864438892736282625])  # create a slash command for the supplied guilds
async def hello(ctx):
    """Say hello to the bot"""  # the command description can be supplied as the docstring
    await ctx.respond(f"Hello {ctx.author}!")

@bot.slash_command(guild_ids=[864438892736282625])
async def newyeargoal(ctx,*,goal):
    """Log a goal, one at a time"""
    await ctx.respond(f"Yessir\nYour goal is `{goal}`\nI've logged it for you, NOW LET'S GO GET IT <:lezgooo:923128327970099231>")
    person = str(ctx.author)
    finalValues = (person, goal)
    sql = "INSERT INTO test_goals_2002 (user, goals) VALUES (%s, %s)"
    mycursor.execute(sql, finalValues)
    mydb.commit()
    await asyncio.sleep(2628288)

bot.run(token)