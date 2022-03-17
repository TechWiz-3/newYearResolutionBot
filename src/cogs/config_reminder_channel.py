from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command,commands
)
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import mysql.connector
import random
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

reminder_channel_success_response = [
    "THAT'S THE WAY TO GO",
    "yeah boi",
    "now, let's get this show started",
    "great start bois n gorls",
    "xD",
    "lez get it now"
        ]

class ConfigReminderChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command(default_permissions = False)
    async def config_reminder_channel(self, ctx, reminder_channel: Option(discord.TextChannel, "Reminder channel", required = True)):
        """Sets the server's reminder channel"""
        if ctx.author.guild_permissions.administrator or ctx.author.id == 760345587802964010:
            server_logged = False
            get_servers_config = "SELECT server_id FROM config WHERE server_id = %s" # checks if the server is in the config table
            values = (ctx.guild.id,)
            cursor.execute(get_servers_config, values)
            for entry in cursor:
                server_logged = True
            if server_logged == True:
                await ctx.respond("You server is already logged in my table, I'm updating the channel for you :)")
                insert_reminder_channel = "UPDATE config SET reminder_channel_id = %s WHERE server_id = %s"
                values = (str(reminder_channel.id), str(ctx.guild.id))
                cursor.execute(insert_reminder_channel, values)
                db.commit()
                await ctx.send(f"<:agreentick:875244017833639956> Sucess {random.choice(reminder_channel_success_response)}")
            elif server_logged == False:
                insert_reminder_channel = "INSERT INTO config (server_id, reminder_channel_id) VALUES (%s, %s)"
                values = (str(ctx.guild.id), str(reminder_channel.id))
                cursor.execute(insert_reminder_channel, values)
                db.commit()
                await ctx.respond(f"<:agreentick:875244017833639956> Sucess {random.choice(reminder_channel_success_response)}")

def setup(bot):
    bot.add_cog(ConfigReminderChannel(bot))