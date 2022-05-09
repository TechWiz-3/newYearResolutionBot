from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import mysql.connector
import random
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

all_goals_deleted = [
    "WTH THIS PEEP IS CRAZY",
    "Dude is on a KILLING RAMPAGE",
    "Somebody get the police, dude just deleted all his goals",
    "If you don't got goals you can't achieve em"
        ]
specific_goal_deleted = [
    "Can someone explain why?",
    "Who deletes their goals huh",
    "You just deleted a goal bruh, better make it up by adding two more",
    "Insane",
    "What is the meaning of life????? Humans make me doubt myself :rolling_eyes:"
        ]


class ClearGoals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def clear_goals(self, ctx, id: Option(int, "Enter the ID of the goal you wish to delete", required=False)):  # type: ignore
        """Delete all logged goals, or a specific goal based on ID"""
        db.commit()
        if id == None:
            deleteGoals = "DELETE FROM goal WHERE user_id = %s"
            deleteReminderEntries = "DELETE FROM reminder WHERE user_id = %s"
            deleteDateReminderEntries = "Delete FROM next_reminder WHERE user_id = %s"
            user = (str(ctx.author.id),)
            cursor.execute(deleteGoals, user)
            cursor.execute(deleteReminderEntries, user)
            cursor.execute(deleteDateReminderEntries, user)
            db.commit()
            await ctx.respond(
                f"All goals deleted. {random.choice(all_goals_deleted)}\nNow time to put new\
                 ones in `/new_year_goal`\n*Also, your reminders have been removed*"
                )
        else:
            userAndIdMatch = False
            getUserFromGoal = "SELECT user_id FROM goals WHERE id = %s"
            values = (id,)
            cursor.execute(getUserFromGoal, values)
            for goalEntry in cursor:
                userOfGoal, = goalEntry
                if str(userOfGoal) == str(ctx.author.id):
                    userAndIdMatch = True
            if userAndIdMatch == True:
                sql = "DELETE FROM goal WHERE user_id = %s AND id = %s"
                user = str(ctx.author.id)
                goalId = int(id)
                values = (user, goalId)
                cursor.execute(sql, values)
                db.commit()
                await ctx.respond(
                    f"Specific goal deleted. {random.choice(specific_goal_deleted)}"
                    )
            else:
                policeEmoji = get(self.bot.emojis, name="pepe_police")
                await ctx.respond(
                    f"Wow, you trying to delete somebody elses goals? That's malicious dude {policeEmoji} <:angry_pepe_ak47:930283816143171604>\n||If not that means you put the wrong ID||"
                )   

def setup(bot):
    bot.add_cog(ClearGoals(bot))