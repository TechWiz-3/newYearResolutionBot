from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command,commands
)
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from discord.commands import Option
from datetime import date

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
second_cursor = db.cursor(buffered=True)

class RemindMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def remind_me(self, ctx, *, days: Option(int, "Enter how often you'd like to be reminded in days", required=True)):  # time in days
        """Tells the bot to remind you about your goals every x days"""
        goalsSet = False # automatically assume that goals haven't been set
        checkGoals = "SELECT * FROM 2022_Goals WHERE userId = %s" # check if goals have been set
        values = (str(ctx.author.id),) # get the users name
        cursor.execute(checkGoals, values) # execute
        for entry in cursor: # loop through results if there are any
            goalsSet = True # goals indeed have been set
        if goalsSet == True: # go ahead to next check
            reminderSetPreviously = False # assume that a reminder has not been set before
            getReminders = "SELECT days FROM reminders WHERE userId = %s" # find reminders set previously
            values = (str(ctx.author.id),) # users name
            second_cursor.execute(getReminders, values) # execute
            for reminder in second_cursor: # loop through results if they exist
                print(f"running\n{reminder}")
                reminderSetPreviously = True # reminder has been set prevously
            if reminderSetPreviously == True: # reminder has been set previously
                # tell them off
                await ctx.respond(
                    "MATE, like BRUH lmao :joy:\nYou've already set a reminder, are you trying to break me?\nBut what you can do... is reset your reminder time with `/change_reminder_interval`. Also if you don't wish to be reminded type `/stop_reminding`"
                        )
            else: # if reminder hasn't been set previously
                # finally execute remind me command
                setReminder = "INSERT INTO reminders (user, days, userId) VALUES (%s, %s, %s)" # insert days interval
                values = (str(ctx.author), days, str(ctx.author.id))
                cursor.execute(setReminder, values) # execute
                # set next reminder to today
                nextReminder = str(date.today()).replace(",", "-").replace(" ", "") # do i even need all the replace replace
                values = (str(ctx.author), nextReminder, str(ctx.author.id))
                # insert date into db
                setDate = "INSERT INTO nextDateReminder (user, next_date, userId) VALUES (%s, %s, %s)"
                cursor.execute(setDate, values)
                db.commit()
                await ctx.respond(
                    f"Going to be reminding you every `{days}`\nTo check your next reminder `/next_reminder`\n\n*Good job bruh, now time to get to work <:stronk_doge:925285801921769513> <:lezgooo:925286931221344256> If you need help, we got you <#867600399879372820>*"
                )
        elif goalsSet == False: # if goals haven't been set
                await ctx.respond(
                "Well it's great that you want to be reminded, but make sure you set goals first `/new_year_goal` :grin:"
                )

def setup(bot):
    bot.add_cog(RemindMe(bot))