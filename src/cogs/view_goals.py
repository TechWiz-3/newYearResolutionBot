from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import mysql.connector
from discord.utils import get
from cogs.functions.db_functions import connect,disconnect


class ViewGoals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command()
    async def view_goals(self, ctx):
        """Displays your currently logged and achieved goals"""
        cursor,db=connect()
        db.commit()
        green_tick_emoji = get(self.bot.emojis, name="epicTick") # get a tick emoji
        slash_emoji = get(self.bot.emojis, name="aslash") # get a slash emoji
        goals_set = False # variable that indicates that the user has sett their goals
        goals_message_list = ""
        goals_counter = 0 # how many goals
        goals_achieved_counter = 0 # how many goals have been achieved
        author_id = (str(ctx.author.id),)
        # get the users goals, status represents whether the goal has been achieved or not
        get_goals = "SELECT goal, status FROM goal WHERE user_id = %s"
        cursor.execute(get_goals, author_id) # get each goal and corresponding status for the user
        for goal_and_status in cursor: # loop through results
            goal,status = goal_and_status # assign the results
            goals_set = True # user has set their goals
            goals_counter += 1 # increment the goals looped through
            if status == 1: # if goal achieved
                goals_message_list += f"{green_tick_emoji} `{goal}`\n"
                goals_achieved_counter += 1
            elif status == 0: # if goal not achieved
                goals_message_list += f"{slash_emoji} `{goal}`\n"
        if goals_achieved_counter > 0:
            await ctx.respond(
                f"Your goals are...\n\n{goals_message_list}\n**<:pepe_hypers:925274715214458880> You have achieved __{goals_achieved_counter}__ out of __{goals_counter}__ goals**\nKEEP GRINDING <:pepebuff:874499841407983647> <:pepebuff:874499841407983647>"
            )
        elif goals_set == True:
            await ctx.respond(
                f"Your goals are...\n\n{goals_message_list}\nYou haven't achieved any of your {goals_counter} goals, but that doesn't matter, **TRAIN HARD TRAIN SMART** (that's what Gravity Destroyers is for) and you'll get there <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>"
            )
        elif goals_set == False: # respond to user that hasn't set goals
            await ctx.respond("Ummm, you need to set your goals first before viewing them lol\n\n*However, I live go serve bright human ;) ... these commands may help...* `/help` `/new_year_goal`")
        disconnect(cursor,db)

def setup(bot):
    bot.add_cog(ViewGoals(bot))