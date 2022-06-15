from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from discord.commands import Option
from datetime import date
from cogs.functions.db_functions import disconnect

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")


class RemindMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def remind_me(self, ctx, *, days: Option(int, "Enter how often you'd like to be reminded in days", required=True)):  # type: ignore # time in days
        """Tells the bot to remind you about your goals every x days"""
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=PORT,
            pool_name="remindmepool",
            pool_size=24
                )

        cursor = db.cursor(buffered=True)
        second_cursor = db.cursor(buffered=True)

        db.commit()
        goal_set = False # automatically assume that goals haven't been set
        check_goals = "SELECT * FROM goal WHERE user_id = %s" # check if goals have been set
        values = (str(ctx.author.id),) # get the users name
        cursor.execute(check_goals, values) # execute
        for entry in cursor: # loop through results if there are any
            goal_set = True # goals indeed have been set
        if goal_set == True: # go ahead to next check
            reminder_set_previously = False # assume that a reminder has not been set before
            get_reminders = "SELECT days FROM reminder WHERE user_id = %s" # find reminders set previously
            values = (str(ctx.author.id),) # users name
            second_cursor.execute(get_reminders, values) # execute
            for reminder in second_cursor: # loop through results if they exist
                print(f"running\n{reminder}")
                reminder_set_previously = True # reminder has been set prevously
            if reminder_set_previously == True: # reminder has been set previously
                # tell them off
                await ctx.respond(
                    "MATE, like BRUH lmao :joy:\nYou've already set a reminder, are you trying to break me?\nBut what you can do... is reset your reminder time with `/change_reminder_interval`. Also if you don't wish to be reminded type `/stop_reminding`"
                        )
            else: # if reminder hasn't been set previously
                # finally execute remind me command
                set_reminder = "INSERT INTO reminder (user, days, user_id) VALUES (%s, %s, %s)" # insert days interval
                values = (str(ctx.author), days, str(ctx.author.id))
                cursor.execute(set_reminder, values) # execute
                # set next reminder to today
                next_reminder = str(date.today()).replace(",", "-").replace(" ", "") # do i even need all the replace replace
                values = (str(ctx.author), next_reminder, str(ctx.author.id))
                # insert date into db
                setDate = "INSERT INTO next_reminder (user, next_date, user_id) VALUES (%s, %s, %s)"
                cursor.execute(setDate, values)
                db.commit()
                await ctx.respond(
                    f"Going to be reminding you every `{days}`\nTo check your next reminder `/next_reminder`\n\n*Good job bruh, now time to get to work <:stronk_doge:925285801921769513> <:lezgooo:925286931221344256> If you need help, we got you <#867600399879372820>*"
                )
        elif goal_set == False: # if goals haven't been set
                await ctx.respond(
                "Well it's great that you want to be reminded, but make sure you set goals first `/new_year_goal` :grin:"
                )
        disconnect(cursor,db)

def setup(bot):
    bot.add_cog(RemindMe(bot))
