from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import mysql.connector

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

class ViewGoals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command()
    async def view_goals(self, ctx):
        """Displays your currently logged and achieved goals"""
        greenTickEmoji = discord.utils.get(self.bot.emojis, name="epicTick") # get a tick emoji
        slashEmoji = discord.utils.get(self.bot.emojis, name="aslash") # get a slash emoji
        goalsSet = False # variable that indicates that the user has sett their goals
        goals_message_list = ""
        goalsCounter = 0 # how many goals
        goalsAchievedCounter = 0 # how many goals have been achieved
        author_id = (str(ctx.author.id),)
        # get the users goals, status represents whether the goal has been achieved or not
        getGoals = "SELECT goals, status FROM 2022_Goals WHERE userId = %s"
        cursor.execute(getGoals, author_id) # get each goal and corresponding status for the user
        for goalAndStatus in cursor: # loop through results
            goal,status = goalAndStatus # assign the results
            goalsSet = True # user has set their goals
            goalsCounter += 1 # increment the goals looped through
            if status == 1: # if goal achieved
                goals_message_list += f"{greenTickEmoji} `{goal}`\n"
                goalsAchievedCounter += 1
            elif status == 0: # if goal not achieved
                goals_message_list += f"{slashEmoji} `{goal}`\n"
        if goalsAchievedCounter > 0:
            await ctx.respond(
                f"Your goals are...\n\n{goals_message_list}\n**<:pepe_hypers:925274715214458880> You have achieved __{goalsAchievedCounter}__ out of __{goalsCounter}__ goals**\nKEEP GRINDING <:pepebuff:874499841407983647> <:pepebuff:874499841407983647>"
            )
        elif goalsSet == True:
            await ctx.respond(
                f"Your goals are...\n\n{goals_message_list}\nYou haven't achieved any of your {goalsCounter} goals, but that doesn't matter, **TRAIN HARD TRAIN SMART** (that's what Gravity Destroyers is for) and you'll get there <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>"
            )
        elif goalsSet == False: # respond to user that hasn't set goals
            await ctx.respond("Ummm, you need to set your goals first before viewing them lol\n\n*However, I live go serve bright human ;) ... these commands may help...* `/help` `/new_year_goal`")

def setup(bot):
    bot.add_cog(ViewGoals(bot))