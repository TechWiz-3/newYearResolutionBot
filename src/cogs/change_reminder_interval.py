from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
from dotenv import load_dotenv
import os
from datetime import date
from discord.utils import get
from discord.commands import Option
from cogs.functions.db_functions import connect,disconnect
from mysql.connector import errors as db_errors

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")

class ChangeReminderInterval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def change_reminder_interval(self, ctx, how_often: Option(int, "Enter how often in days you wish to be reminded", required=True)):  # type: ignore
        """Adjusts how often you're reminded of your goals"""
        cursor,db = connect()
        try:
            db.commit()
            adjust_interval = "UPDATE reminder SET days = %s WHERE user_id = %s" # update the reminders table and set the days interval to the new value
            values = (how_often, str(ctx.author.id))
            cursor.execute(adjust_interval, values)
            adjust_interval_date = "UPDATE next_reminder SET next_date = %s WHERE user_id = %s" # update the next date reminder table, to remind the user immediately
            values = (
                str(date.today()),
                str(ctx.author.id)
                )  # set values to today's date and the user's id
            cursor.execute(adjust_interval_date, values)
            db.commit()
            cooldoge = get(self.bot.emojis, name="cooldoge")
            await ctx.respond(
                f"{cooldoge} Well, that went well. Your interval is now `{how_often}` day(s). Achievement time babyy"
                )
        except db_errors:
            try:
                cursor,db = connect()
            except Exception as error:
                print("Attempt at reconnecting to DB failed", error)
                await ctx.respond("Sorry, datebase seems to be seriously bugged up rn ;(")
            else:
                await ctx.respond(
                    "An error occured while connecting to the database however an attempt to reconnect was successful, if you run the command again, it should work"
                        )
        disconnect(cursor,db)

def setup(bot):
    bot.add_cog(ChangeReminderInterval(bot))