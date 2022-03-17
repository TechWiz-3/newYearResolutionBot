# Created by #Zac the Wise#1381 with help from #iamkneel#2359

# Update created by Zac on 17/Mar

# huge cogs update, however not finalised

# Version 5.0.0

import asyncio
from discord.commands import Option
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import date, timedelta
from discord.utils import get
#from discord.commands import permissions
import discord
import random

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
DEV_GUILD_ID = 864438892736282625
PROD_GUILD_ID = 867597533458202644

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="goals!", intents=intents)
            
bot.load_extension('cogs.new_year_goal')
bot.load_extension('cogs.remind_me')
bot.load_extension('cogs.view_goals')
bot.load_extension('cogs.view_ids')
bot.load_extension('cogs.config_reminder_channel')
bot.load_extension('cogs.help')
bot.load_extension('cogs.stop_reminding')
bot.load_extension('cogs.goal_achieved')
bot.load_extension('cogs.edit_goal')
bot.load_extension('cogs.next_reminder')
bot.load_extension('cogs.change_reminder_interval')
bot.load_extension('cogs.clear_goals')
bot.load_extension('cogs.events')

bot.run(BOT_TOKEN)
