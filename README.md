TenTalkBot
Discord Bot for OSRS CC Ten Talk

===== Bot Descriptions =====

Control scripts

	start.sh - Starts bots individually or all at once
	stop.sh - Stops bots individually or all at once
	restart.sh - Restarts bots individually or all at once

Discord commands

	!application_set - Sets the application message
		Requires manage messages permissions
	!commands - Shows a list of available commands
		Supports CCBot use
	!discord - Friendly link to the Discord server
		Supports CCBot use
	!hello - Hello! Use this to confirm the bot is connected to the server
		Supports CCBot use
	!info - Shows whetever is set by !info_set
		Supports CCBot use
	!info_set <cc/disc> <"message"> - Set a pre-recorded !info message; supports seperate messages for CC and Disc
		Requires manage messages permissions
	!motd - Shows whetever is set by !motd_set
		Supports CCBot use
	!motd_set <cc/disc> <"message"> - Set a pre-recorded !motd message; supports seperate messages for CC and Disc
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
	!register <Twitch Name> - Register Twitch Name to the Live bot; 1 Twitch ID per Discord user
	!reminder - Drink Up!
		Supports CCBot use
	!stats <rsn> - Shows stats for a specified RSN. Use quotes if RSN contains spaces "Eg RSN"
	!sotw - shows a predefined message in sotw.msg
		Supports CCBot use
	!unregister <Twitch Name> - Unregister Twitch Name from the Live bot; Mods can unregister anyone, users can only unregister themselves
	!verify <@user> - Verifies the user and deletes the application channel

Other

	application.py - Creates a temporary application channel when a member reacts to a message
	disc_commands.cfg - Allows controlling what is shown by !commands in Discord
	live.py - Send notifications to specified channel when Discord members go live on Twitch


===== Setup Instructions =====

To run this bot you will need 1 headless linux server
Debian is recommended for the Linux server. 

Before running any programs, install python3 and the following pip packages onto both computers:

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
	twitch-python
	typing-extensions

Create your .env file

	Create a file called .env using this template:

	TOKEN=123hjk123hjk123hjk123hjk123hjk123hjk123hkj
	welcome_chan=894569845768943
	register_msg=45769569075567
	app_cat=47656754754757
	twitch_client=fio34ni9fn93infg08543n0g
	twitch_secret=mi09435jng03809g3480g
	twitch_channel=4390589034859034234235
	


	Populate the .env file as described:
		TOKEN is your Discord Bot Token
		welcome_chan is the channel where new member notifications are shown
		register_msg is the message to react to when a member applies
		app_cat is the category where application threads will appear
		twitch_client is your Twitch API client ID
		twitch_secret is your Twitch API secret ID
		twitch_channel is the UID of the discord channel where Twitch notifications will be sent


Clone the git repo. Recommend using the burnt branch
