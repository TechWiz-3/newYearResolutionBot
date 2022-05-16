from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command,Option
)
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
#import mysql.connector as connector
from mysql.connector import errors as db_errors
from discord.utils import get as discord_getter
from cogs.functions.db_functions import connect,disconnect

class NewYearGoal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def new_year_goal(self, ctx, *, goal: Option(str, "Type the name of the goal (one only)", required=True)):  # type: ignore
        """Log a goal, one at a time"""
        cursor,db = connect()
        try:
            db.commit()
            person = str(ctx.author) # get name
            person_id = str(ctx.author.id) # get id
            server_id = str(ctx.guild.id) # get server id and assign it as a string
            status = False # set status if achieved to false
            duplicate_existant = False
            # check if the new goal is a duplicate
            check_goals = "SELECT * FROM goal WHERE user = %s AND goal = %s" # checks for a goal from the user
            values = (person, goal)
            cursor.execute(check_goals, values)
            for entry in cursor: # loop through the results if they exist
                duplicate_existant = True # confirm through this variable that another duplicate exists
                print(entry)
            if duplicate_existant == False:
                final_values = (person, goal, status, person_id, server_id)
                insert_goals = "INSERT INTO goal (user, goal, status, user_id, server_id) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_goals, final_values) # execute
                db.commit()
                lez_goo_emoji = discord_getter(self.bot.emojis, name='lezgooo')
                await ctx.respond(
                    f"Yessir\nYour goal is `{goal}`\n**I've logged it for you, NOW LET'S GO GET IT {lez_goo_emoji}**\nOh and also, remember to do `/remind_me` to let me know how often to remind you about it!"
                    )
            elif duplicate_existant == True:
                await ctx.respond("Wowa, steady on there. This goal is seems to be a duplicate of another, if you wish to remove a goal use the `/edit_goal` command.")
        except db_errors:
            try:
                cursor,db = connect()
            except Exception as error:
                print("Attempt at reconnecting to DB failed", error)
                await ctx.respond("Sorry, datebase seems to be seriously bugged up rn ;(")
            else:
                await ctx.respond(
                    "An error occured while connecting to the database however an attempt to reconnect was successful, if you run the command again, it should work :pray:"
                        )
            disconnect(cursor,db)


def setup(bot):
    bot.add_cog(NewYearGoal(bot))