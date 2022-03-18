from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command,Option
)
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector as connector

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")

db = connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=PORT
)

cursor = db.cursor(buffered=True)

class NewYearGoal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def new_year_goal(self, ctx, *, goal: Option(str, "Type the name of the goal (one only)", required=True)):
        """Log a goal, one at a time"""
        person = str(ctx.author) # get name
        personId = str(ctx.author.id) # get id
        serverId = str(ctx.guild.id) # get server id and assign it as a string
        status = False # set status if achieved to false
        duplicate_existant = False
        # check if the new goal is a duplicate
        check_goals = "SELECT * FROM 2022_Goals WHERE user = %s AND goals = %s" # checks for a goal from the user
        values = (person, goal)
        cursor.execute(check_goals, values)
        for entry in cursor: # loop through the results if they exist
            duplicate_existant = True # confirm through this variable that another duplicate exists
            print(entry)
        if duplicate_existant == False:
            finalValues = (person, goal, status, personId, serverId)
            insertGoals = "INSERT INTO 2022_Goals (user, goals, status, userId, serverId) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insertGoals, finalValues) # execute
            db.commit()
            await ctx.respond(
                f"Yessir\nYour goal is `{goal}`\n**I've logged it for you, NOW LET'S GO GET IT <:lezgooo:923128327970099231>**\nOh and also, remember to do `/remind_me` to let me know how often to remind you about it!"
                )
        elif duplicate_existant == True:
            await ctx.respond("Wowa, steady on there. This goal is seems to be a duplicate of another, if you wish to remove a goal use the `/edit_goal` command.")

def setup(bot):
    bot.add_cog(NewYearGoal(bot))