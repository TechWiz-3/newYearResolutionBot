from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
import discord
from dotenv import load_dotenv

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command()
    async def help(self, ctx):
        """Helps you use the bots commands"""
        print(f"Help command invoked by {ctx.author.name} in {ctx.channel.name}")
        embed=discord.Embed(title="About Me", description="I'm a bot specifically created for Gravity Destroyers. My purpose is simple:\n<:agreentick:875244017833639956> Log users goals\n<:agreentick:875244017833639956> Remind users about their goals\n<:agreentick:875244017833639956> Help motivate and remind users to keep working at and achieve their goals :muscle:", colour = discord.Color.yellow()) ##ebd534
        embed.add_field(
            name="Config Reminder Channel Command",
            value=":warning: **Extremely important command.**\nWithout setting a channel, the reminder function won't work. To use this command, type `/config_reminder_channel` and enter the channel you in your server you wish to for goal reminders.",
            inline=False
                )
        embed.add_field(
            name="New Year Goal Command",
            value="To use this command, type `/new_year_goal` and click space, enter or tab, then type in your goal, type one goal at a time and keep it to raw text.",
            inline=False
                )
        embed.add_field(
            name="View Goals Command",
            value="To use this command, type `/view_goals`",
            inline=False
                )
        embed.add_field(
            name="View Ids Command",
            value="To use this command, type `/view_ids`. Each goal will be displayed with it's corresponding ID in bold.",
            inline=False
                )
        embed.add_field(
            name="Goal Achieved Command",
            value="To use this command, type `/goal_achieved` then press tab and enter the ID corresponding to the goal you wish to mark as achieved.",
            inline=False
                )
        embed.add_field(
            name="Remind Me Command",
            value="This command instructs the bot to remind you of your goals. To use it type `/remind_me` then press tab and enter how often you wish to be reminded of your goals in days.",
            inline=False
                )
        embed.add_field(
            name="Stop Reminding Commnad",
            value="This command stops the bot from reminding you about your goals, to use it type `/stop_reminding`",
            inline=False
                )
        embed.add_field(
            name="Clear Goals Command",
            value="Removes all logged goals and reminders OR a single goal and leaves reminders. To delete all goals, type `/clear_goals`. To delete a specific goal type `/clear_goals id` the ID should be that of the goal you wish to delete, to get the ID’s for your goals type `/view_ids`",
            inline=False
                )
        embed.add_field(
            name="Edit Goal Command",
            value="This command edits a goal based on it’s ID. To use this command type `/edit_goal id newgoal`",
            inline=False
                )
        embed.add_field(
            name = "Next Reminder Command",
            value = "Shows you when your next goal reminder is. To use this command type `/next_reminder`",
            inline =False
                )
        embed.add_field(
            name = "Change Reminder Interval Command",
            value = "Allows you to change how often you are reminded in days `/change_reminder_interval days`",
            inline=False
            )
        try:
            await ctx.respond(embed=embed)
            print("Responded successfully")
        except Exception as error:
            print("Help command response failed")
            await ctx.respond(f"{error}")

    @slash_command()
    async def get_started(self, ctx):
        """Helps you get started :)"""
        print(f"Get started command invoked by {ctx.author.name} in {ctx.channel.name}")
        content_one = "||`/help` The help command is your go to command to understand anything, but here's the recommended sequence of commands:||"
        content_two = "||Run`/new_year_goal` for **each** new year goal you wish to achieve.\n\nRun `/view_goals` to ensure that all your goals havee been logged.\n\nRun `/remind_me` to set how often you'll be reminded.||"
        content_three = "||For more command use the `/help` command. If you enounter any issues pls ping `@Zac the Wise#1381` :)||"

        await ctx.respond(
            f"Ayo {ctx.author.mention} so you want to get after those goals and make this year, your year. Well GOOD NEWS, I'm here to help...\n\n{content_one}\n\n{content_two}\n\n{content_three}"
            )

def setup(bot):
    bot.add_cog(Help(bot))