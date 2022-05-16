
from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from discord.utils import get
from discord.errors import HTTPException
from cogs.functions.db_functions import connect,disconnect




class ViewIds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command()
    async def view_ids(self, ctx):
        """Displays each logged called and it's unique ID to access"""
        cursor,db=connect()
        db.commit()
        final_message = ""
        author = (str(ctx.author.id),) # gets the command invoker
        goals_logged = False
        sql = "SELECT goal, id FROM goal WHERE user_id = %s" # searches the table for goals and ids with the user's name
        cursor.execute(sql, author)
        for entry in cursor: # loop through results
            goals_logged = True
            goal, goal_id = entry # unpack results
            final_message = final_message + f"`{goal}`\t`{goal_id}`\n" # add to the final message the goal and goal id
        try:
            await ctx.respond(final_message) # send the final list
        except HTTPException:
            if goals_logged:
                await ctx.respond("Seems like you don't have any goals?")
        disconnect(cursor,db)

def setup(bot):
    bot.add_cog(ViewIds(bot))