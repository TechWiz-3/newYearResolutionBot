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
from cogs.functions.db_functions import connect,disconnect

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
        cursor,db = connect()
        db.commit()
        if id == None:
            delete_goals = "DELETE FROM goal WHERE user_id = %s"
            delete_reminder_entries = "DELETE FROM reminder WHERE user_id = %s"
            delete_date_reminder_entries = "Delete FROM next_reminder WHERE user_id = %s"
            user = (str(ctx.author.id),)
            cursor.execute(delete_goals, user)
            cursor.execute(delete_reminder_entries, user)
            cursor.execute(delete_date_reminder_entries, user)
            db.commit()
            await ctx.respond(
                f"All goals deleted. {random.choice(all_goals_deleted)}\nNow time to put new ones in `/new_year_goal`\n*Also, your reminders have been removed*"
                )
        else:
            user_and_id_match = False
            get_user_from_goal = "SELECT user_id FROM goal WHERE id = %s"
            values = (id,)
            cursor.execute(get_user_from_goal, values)
            for goalEntry in cursor:
                user_of_goal, = goalEntry
                if str(user_of_goal) == str(ctx.author.id):
                    user_and_id_match = True
            if user_and_id_match == True:
                sql = "DELETE FROM goal WHERE user_id = %s AND id = %s"
                user = str(ctx.author.id)
                goal_id = int(id)
                values = (user, goal_id)
                cursor.execute(sql, values)
                db.commit()
                await ctx.respond(
                    f"Specific goal deleted. {random.choice(specific_goal_deleted)}"
                    )
            else:
                police_emoji = get(self.bot.emojis, name="pepe_police")
                await ctx.respond(
                    f"Wow, you trying to delete somebody elses goals? That's malicious dude {police_emoji} <:angry_pepe_ak47:930283816143171604>\n||If not that means you put the wrong ID||"
                )
        disconnect(cursor,db)

def setup(bot):
    bot.add_cog(ClearGoals(bot))
