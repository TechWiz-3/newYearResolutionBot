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
mydb = mysql.connector.connect(
  host="containers-us-west-23.railway.app",
  user="root",
  password="yUWgeMOav9HmGFDqUIXo",
  database="railway",
  port="6499"
)
mycursor = mydb.cursor()

load_dotenv()
token = os.getenv("token")

bot = commands.Bot(command_prefix=".")


@bot.slash_command(guild_ids=[864438892736282625])  # create a slash command for the supplied guilds
async def hello(ctx):
    """Say hello to the bot"""  # the command description can be supplied as the docstring
    await ctx.respond(f"Hello {ctx.author}!")

@bot.slash_command(guild_ids=[864438892736282625])
async def newyeargoal(ctx,*,goal):
    """Log a goal, one at a time"""
    await ctx.respond(f"Yessir\nYour goal is `{goal}`")

bot.run(token)