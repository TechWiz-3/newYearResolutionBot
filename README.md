
![Image](https://cdn.discordapp.com/emojis/925286931221344256.png?size=60 "lezgoo")
# New Years Resolution Bot #
Accountability incoming...
-----------
[![Image](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge&logo=gnu)](https://github.com/TechWiz-3/newYearsResolutionBot/blob/main/LICENSE)
![image](https://img.shields.io/github/v/release/TechWiz-3/newYearsResolutionBot?color=green&logo=semantic-release&sort=semver&style=for-the-badge)
![Image](https://img.shields.io/github/last-commit/TechWiz-3/newYearsResolutionBot?color=yellow&logo=github&style=for-the-badge)
![Image](https://img.shields.io/github/commit-activity/m/TechWiz-3/newYearsResolutionBot?color=yellowgreen&logo=git&style=for-the-badge)
![Image](https://img.shields.io/badge/python-3.9-informational?style=for-the-badge&logo=python&logoColor=yellow)
![Image](https://img.shields.io/badge/Host-Railway-blueviolet?style=for-the-badge&logo=railway)
![Image](https://img.shields.io/tokei/lines/github/TechWiz-3/newYearsResolutionBot?color=36b2f5&logo=visual%20studio%20code&logoColor=0078d7&style=for-the-badge)
### Invite
[![Invite Me](https://www.imagefu.com/create/button#%7B%22content%22:%22%3Cspan+style=%5C%22font-family:+&quot;Open+Sans&quot;,+sans-serif;+color:+rgb(255,+255,+0);+font-weight:+bold;+text-shadow:+rgb(51,+51,+51)+1px+1px+0px;%5C%22%3E%3Cspan+style=%5C%22color:+rgb(102,+102,+102);+text-shadow:+none;%5C%22%3EInvite+Me%3C/span%3E%3Cbr+/%3E%3C/span%3E%22,%22background%22:%7B%22orientation%22:0,%22stops%22:%5B%7B%22color%22:%22#e4ee17ff%22,%22offset%22:0%7D,%7B%22color%22:%22#edc951ff%22,%22offset%22:100%7D%5D%7D,%22borders%22:%7B%22top%22:%7B%22color%22:%22#ffff00ff%22,%22width%22:1%7D,%22right%22:%7B%22color%22:%22#ffff00ff%22,%22width%22:1%7D,%22bottom%22:%7B%22color%22:%22#ffff00ff%22,%22width%22:1%7D,%22left%22:%7B%22color%22:%22#ffff00ff%22,%22width%22:1%7D%7D,%22corners%22:%7B%22topLeft%22:%7B%22horizontalRadius%22:5,%22verticalRadius%22:5%7D,%22topRight%22:%7B%22horizontalRadius%22:5,%22verticalRadius%22:5%7D,%22bottomRight%22:%7B%22horizontalRadius%22:5,%22verticalRadius%22:5%7D,%22bottomLeft%22:%7B%22horizontalRadius%22:5,%22verticalRadius%22:5%7D%7D,%22sizeOrPadding%22:%7B%22top%22:10,%22right%22:10,%22left%22:10,%22bottom%22:10%7D,%22shadows%22:%5B%7B%22type%22:0,%22horizontalOffset%22:0,%22verticalOffset%22:0,%22blur%22:0,%22color%22:%22#444444dd%22%7D%5D%7D)](https://discord.com/api/oauth2/authorize?client_id=922767657265168394&permissions=2147838976&scope=applications.commands%20bot)
### What
The New Years Resolution Bot is a discord bot created to motivate users to log their new year resolutions, remind them about these resolutions and provide accountability and motivation to help achieve those goals. 

### How

The New Years Resolution Bot is coded in [*Pycord*](https://github.com/Pycord-Development/pycord) and [*Python MySQL Connector*](https://dev.mysql.com/doc/connector-python/en/). The bot is coded to use entirely slash commands as a user interface for commands.

### Where

This bot was initially created for [one server](https://discord.gg/7Pjjf2XTFw) however we now have compatibility for **all** servers. Here's the [invite](https://discord.com/api/oauth2/authorize?client_id=922767657265168394&permissions=2147838976&scope=applications.commands%20bot).

## Commands

`/help`  
*Displays a information about the capabilities of the bot as well as a list of commands and their users*

`/get_started`  
*Responds with a message explaining the basic commands to begin using the bot*  

`/config_reminder_channel`
*Sets the server's reminder channel to enable reminding*

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

## Setup
### Environment Variables
 
Create a `.env` or set environment variables with the following values  
The discord bot's token `TOKEN`    
MySQL DB information: `MYSQLHOST` `MYSQLUSER` `MYSQLPASSWORD` `MYSQLDATABASE` `MYSQLPORT`    

### Tools

*The file [`sqlConfig.py`](https://github.com/TechWiz-3/newYearsResolutionBot/blob/main/tools/sqlConfig.py) contains the queries to create the four database tables used by the bot.*  

`2022_Goals` *is used for storing each users goals as well as their user id and name, in the future it will also store the server ID of which the command was invoked in.*  

`reminders` *stores the uername, user id and how often (in days) the user wishes to be reminded.*  

`nextDateReminder` *stores the username, user id and next date each user should be reminded on.*    
  
`config` *stores server ids and their preferred reminder channel id*

## Hosting
Currently RailwayApp is used for hosting.  
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app?referralCode=6KJ1hh)
