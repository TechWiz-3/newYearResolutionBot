from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
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

class EditGoal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def edit_goal(self, ctx, id: Option(int, "Enter the ID corresponding to the goal you wish to change"), newtext: Option(str, "Enter the new goal you'd like to set")):
        """Edits a goal entry based on ID"""
        goalIsForUser = False
        checkGoalAndId = "SELECT userId FROM 2022_Goals WHERE id = %s" # looks for the goal with that id
        values = (id,)
        cursor.execute(checkGoalAndId, values)
        for userid_entry in cursor:
            user, = userid_entry
            if str(user) == str(ctx.author.id): # checks if the user and goal creator are the same
                goalIsForUser = True # confirms that the goal creator and command in invoker are the same
        if goalIsForUser == True:
            # goes ahead and updated the goal
            changeGoal = "UPDATE 2022_Goals SET goals = %s WHERE userId = %s AND id = %s"
            values = (newtext, str(ctx.author.id), id)
            cursor.execute(changeGoal, values)
            db.commit()
            await ctx.respond(f"Perfect, you've replaced goal `{id}` with the text `{newtext}`")
        else:
            # if the goal doesn't belong to the command invoker
            await ctx.respond("Something sus here bruh, idk what it is tho, maybe the ID you put is wrong?")

def setup(bot):
    bot.add_cog(EditGoal(bot))