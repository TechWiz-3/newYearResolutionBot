from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from discord.commands import Option
from cogs.functions.db_functions import connect,disconnect

class EditGoal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def edit_goal(self, ctx, id: Option(int, "Enter the ID corresponding to the goal you wish to change"), newtext: Option(str, "Enter the new goal you'd like to set")):  # type: ignore
        """Edits a goal entry based on ID"""
        cursor,db=connect()
        db.commit()
        goal_is_for_user = False
        check_goal_and_id = "SELECT user_id FROM goal WHERE id = %s" # looks for the goal with that id
        values = (id,)
        cursor.execute(check_goal_and_id, values)
        for userid_entry in cursor:
            user, = userid_entry
            if str(user) == str(ctx.author.id): # checks if the user and goal creator are the same
                goal_is_for_user = True # confirms that the goal creator and command in invoker are the same
        if goal_is_for_user == True:
            # goes ahead and updated the goal
            change_goal = "UPDATE goal SET goal = %s WHERE user_id = %s AND id = %s"
            values = (newtext, str(ctx.author.id), id)
            cursor.execute(change_goal, values)
            db.commit()
            await ctx.respond(f"Perfect, you've replaced goal `{id}` with the text `{newtext}`")
        else:
            # if the goal doesn't belong to the command invoker
            await ctx.respond("Something sus here bruh, idk what it is tho, maybe the ID you put is wrong?")
        disconnect(cursor,db)

def setup(bot):
    bot.add_cog(EditGoal(bot))