VMU Bot
Discord Bot for VMU Discord Server

===== Bot Descriptions =====

Control scripts

	start.sh - Starts bots individually or all at once
	stop.sh - Stops bots individually or all at once
	restart.sh - Restarts bots individually or all at once

Discord commands

	!discord - Friendly link to the Discord server
		Supports CCBot use
	!hello - Hello! Use this to confirm the bot is connected to the server
		Supports CCBot use
	!info - Shows whetever is set by !info_set
		Supports CCBot use
	!info_set <"message"> - Set a pre-recorded !info message; supports seperate messages for CC and Disc
		Requires manage messages permissions
	!join <@User> <"Name"> <Role> - Gives a new user membership, changes nickname to Name, and gives them role Role
		Reuires manage roles permissions
	!motd - Shows whetever is set by !motd_set
		Supports CCBot use
	!motd_set <"message"> - Set a pre-recorded !motd message; supports seperate messages for CC and Disc
		Requires manage messages permissions
	!move <#Channel> <message ids> - Moves the specified message IDs to the #Channel specified
		Requires manage_messages permissions
	!poll <mins> <question> <opt1> .. <opt 8>
		Create a poll that lasts for <mins> minutes
		Up to 8 available options
		Use reactions to answer
	!poll_cancel <number>
		Cancel a specific poll number
		Users are able to only cancel their own polls
		Mods/Admins can calcel any poll
	!welcome_set <"message"> - Set a pre-recorded welcome message
		Requires manage messages permissions

Other

	disc_commands.cfg - Allows controlling what is shown by !commands in Discord
	reaction_roles.py - Gives users roles when reacting to a specified message
	welcome.py - Shows a pre-recorded message when a new user joins the Discord

===== Setup Instructions =====

To run this bot you will need 1 headless linux server

Before running any programs, install python3 and the following pip packages onto the server:

	discord
	discord.py
	google-auth
	google-auth-oauthlib
	gspread
	matplotlib
	numpy
	oauth2client
	oauthlib
	OSRSBytes
	Pillow
	PyAutoGUI
	pycrypto
	PyGetWindow
	python-dotenv
	python-imagesearch
	PyTweening
	typing-extensions

Create your .env file

	Create a file called .env using this template:

	TOKEN=123hjk123hjk123hjk123hjk123hjk123hjk123hkj
	channel=0001
	botchan=0001
	reactchan=0001
	reactmsg=0001
	leader=32904583904589034
	council=89034859034850345
	welcome_chan=348093845908390534


	Populate the .env file as described:
		TOKEN is your Discord Bot Token
		channel is a placeholder, use any integer
		botchan is a placeholder, use any integer
		reactchan is a placeholder, use any integer
		reactmsg is a placeholder, use any integer
		leader is the UID of the leader role
		council is the UID of the council role
		welcome_chan is the channel where new member notifications are shown

Clone the git repo. Must use the vmu branch
