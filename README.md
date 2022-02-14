
![Image](https://cdn.discordapp.com/emojis/925286931221344256.png?size=60 "lezgoo")
# New Years Resolution Bot #
Accountability incoming...
-----------
### What
The New Years Resolution Bot is a discord bot created to motivate users to log their new year resolutions, remind them about these resolutions and provide accountability and motivation to help achieve those goals. 

### How

The New Years Resolution Bot is coded in [*Pycord*](https://github.com/Pycord-Development/pycord) and [*Python MySQL Connector*](https://dev.mysql.com/doc/connector-python/en/). The bot is coded to use entirely slash commands as a user interface for commands.

### Where

Currently the bot is only functional in [one server](https://discord.gg/7Pjjf2XTFw) as this bot was created specifically for that server. Functionality to allow use in other servers will be developed later on

## Commands

`/help`  
*Displays a information about the capabilities of the bot as well as a list of commands and their users*

`/get_started`  
*Responds with a series of messages explaining the basic commands to begin using the bot*  

`/newyeargoal <goal>`  
*Logs a new goal*  

`/remindme <days>`  
*Instructs the bot how often to remind the user about their goals in days*  

`/view_goals`  
*Displays the users goals*  

`/view_ids`  
*Displays the users goals with their corresponding ID in the database. The ID is used for actions such as deleting a goal or marking it as achieved*  

`/goal_achieved <ID>`  
*Marks the goal with the specified ID as achieved*  

`/stop_reminding`  
*Instructs the bot to stop reminding the user of their goals* T_T  

`/change_reminder_interval <days>`  
*Changes how often the bot reminds the user*  
  
`/next_reminder`  
*Displays how often the user is being reminded and the date of their next reminder*

`/clear_goals` or   `/cleargoals <id>`  
*Deletes all goals and reminders or deletes a specific goal and preserves reminders.*

`/edit_goals <id> <new_goal>`
*Edits a goal*

## Setup & Tools
*The file `sqlConfig.py` contains the queries to create the three database tables used by the bot.*  

`2022_Goals` *is used for storing each users goals as well as their user ID and name, in the future it will also store the server ID of which the command was invoked in.*  

`reminders` *stores the uername and how often (in days) the user wishes to be reminded.*  

`nextDateReminder` *stores the next date each user should be reminded on.*    