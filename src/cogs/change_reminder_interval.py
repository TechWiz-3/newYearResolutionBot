from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command,commands
)
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import date
from discord.utils import get
from discord.commands import Option

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

class ChangeReminderInterval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def change_reminder_interval(self, ctx, how_often: Option(int, "Enter how often in days you wish to be reminded", required=True)):
        """Adjusts how often you're reminded of your goals"""
        adjustInterval = "UPDATE reminders SET days = %s WHERE userId = %s" # update the reminders table and set the days interval to the new value
        values = (how_often, str(ctx.author.id))
        cursor.execute(adjustInterval, values)
        adjustIntervalDate = "UPDATE nextDateReminder SET next_date = %s WHERE userId = %s" # update the next date reminder table, to remind the user immediately
        values = (
            str(date.today()),
            str(ctx.author.id)
            )
        cursor.execute(adjustIntervalDate, values)
        db.commit()
        cooldoge = discord.utils.get(self.bot.emojis, name="cooldoge")
        await ctx.respond(
            f"{cooldoge} Well, that went well. Your interval is now `{how_often}` day(s). Achievement time babyy"
            )

def setup(bot):
    bot.add_cog(ChangeReminderInterval(bot))