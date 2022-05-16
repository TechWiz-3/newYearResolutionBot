from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import mysql.connector
from discord.utils import get
from cogs.functions.db_functions import disconnect

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")



class NextReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def next_reminder(self, ctx):
        """Shows you how often you'll be reminded as well as your next reminder date"""
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=PORT,
            pool_name="nreminderpool",
            pool_size=24
                )
        cursor = db.cursor(buffered=True)
        second_cursor = db.cursor(buffered=True)
        db.commit()
        reminder_set = False
        how_often = 0
        next_date = None
        get_reminder_interval = "SELECT days FROM reminder WHERE user_id = %s" # find the reminder interval
        user = (str(ctx.author.id),)
        cursor.execute(get_reminder_interval, user)
        for entry in cursor:
            reminder_set = True # confirms that a reminder has been set
            how_often, = entry # store the days interval in how_often
        get_next_reminder_date = "SELECT next_date FROM next_reminder WHERE user_id = %s" # find the new reminder date
        second_cursor.execute(get_next_reminder_date, user)
        for dateEntry in second_cursor:
            next_date, = dateEntry # store the next date in next_date
        if reminder_set == True:
            await ctx.respond(
                f"You have set to be reminded every `{how_often}` day(s) and your next reminder is on `{next_date}` meanwhile... KEEP GRINDING <:lezgooo:925286931221344256>"
                )    
        elif reminder_set == False: # if a reminder hasn't been found in the table
            um_emoji = get(self.bot.emojis, name="um")
            await ctx.respond(
                f"{um_emoji} you need to set a reminder first before viewing it... `/remind_me`"
                )
        disconnect(cursor,db)

def setup(bot):
    bot.add_cog(NextReminder(bot))