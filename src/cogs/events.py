import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from discord.utils import get
#from discord.commands import permissions
import discord
from cogs.tasks import reminder_function
from cogs.functions.db_functions import connect,disconnect

cursor,db=connect()

"""
----Remember to commit any DB changes----

----Global variables----

memberObject - for reminder function
"""

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server = self.bot.get_guild(864438892736282625)
        log = server.get_channel(866217361115316284)
        await log.send(f"New server joined\n{guild.id}\n{guild.member_count}\n{guild.name}")

    # @commands.Cog.listener()
    # async def on_application_command_error(self, ctx, error): # if slash command error occurs
    #     await ctx.send(f":weary: {error}") # send the error
    #     #if isinstance(error, commands.MissingPermissions):
    
    @commands.Cog.listener()
    async def on_ready(self):
        #await Events.initialise_loop(self)
        await reminder_function.start(self.bot)
        try:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you achieve your goals"))
            while True:
                # alternate between two bot statuses 
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you achieve your goals"))
                await asyncio.sleep(5)
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="get started | /help"))
                await asyncio.sleep(5)
        except Exception as error:
            print(f"Status setup failed due to \n{error}")
    
    # async def initialise_loop(self):
    #     # get each server and send a message to it's reminder channel
    #     get_servers_and_channels = "SELECT server_id, reminder_channel_id FROM config"
    #     cursor.execute(get_servers_and_channels)
    #     for entry in cursor:
    #         server_id, reminder_channel_id = entry
    #         print("Init loop; server id: ", reminder_channel_id)
    #         server = self.bot.get_guild(int(server_id))
    #         reminder_channel = server.get_channel(int(reminder_channel_id))
            #await reminder_channel.send("Initialising...")

    # @commands.Cog.listener()
    # async def on_user_update(self, before, after):
    #     if before.name == after.name and before.discriminator == after.discriminator: # if the name and the discriminator is the same which means they haven't been changed
    #         # username not changed and # discrim not changed
    #         pass
    #     elif before.name != after.name or before.discriminator != after.discriminator:
    #         member_in_goals = False
    #         member_in_reminders = False
    #         old_name = f"{before.name}#{before.discriminator}"
    #         new_name = f"{after.name}#{after.discriminator}"
    #         print(old_name)
    #         print(new_name)
    #         check_member = "SELECT * FROM 2022_Goals WHERE user = %s"
    #         values = (old_name,)
    #         cursor.execute(check_member, values)
    #         for entry in cursor: # run through the results
    #             member_in_goals = True # the member is in the goals table
    #         if member_in_goals == True:
    #             update_table = "UPDATE 2022_Goals SET user = %s WHERE user = %s" # update with new name where old name
    #             values = (new_name, old_name)
    #             cursor.execute(update_table, values) # excecute sql
    #             # since goals are set we need to check the reminders table to update those as well
    #             check_member_reminders = "SELECT * FROM reminders WHERE user = %s" # find any entries with users old name
    #             values = (old_name,)
    #             cursor.execute(check_member_reminders, values) # execute sql
    #             for entry in cursor: # loop through results
    #                 member_in_reminders = True # confirm that the user has been found in the reminders table
    #             if member_in_reminders == True:
    #                 # update both reminder tables with the users new name
    #                 update_reminders = "UPDATE reminders SET user = %s WHERE user = %s"
    #                 values = (new_name, old_name)
    #                 cursor.execute(update_reminders, values)
    #                 update_next_date_table = "UPDATE nextDateReminder SET user = %s WHERE user = %s"
    #                 values = (new_name, old_name)
    #                 cursor.execute(update_next_date_table, values)
    #                 db.commit()
    #                 await after.send(
    #                     "**Hi there,**\nyour profile change has been noted and updated in our goal and reminder tables\nAnyways... KEEP GRINDING <:lezgooo:925286931221344256>"
    #                         )
    #             elif member_in_reminders == False:
    #                 print("Member not in reminders however is in goals table")
    #                 await after.send(
    #                     "**Hi there,**\nyour profile change has been noted and updated in our goals table\nAnyways... KEEP GRINDING <:lezgooo:925286931221344256>"
    #                         )
    #         elif member_in_goals == False:
    #             print("User changed however not in goals table")

def setup(bot):
    bot.add_cog(Events(bot))