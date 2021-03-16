TenTalkBot
Discord Bot for OSRS CC Ten Talk

===== Bot Descriptions =====

Control scripts

	start.sh - Starts bots individually or all at once
	stop.sh - Stops bots individually or all at once
	restart.sh - Restarts bots individually or all at once

CCBot

	cc_to_disc.py - Reads cc messages from latest.log and sends them to Discord on specified channel
		Supports @discord name@ pings
		Supports #discord channel# pings
	disc_to_cc.py - Reads discord messages from specified channel and sends them to CC
		NOTE: Autotypers are bannable. Use at your own risk
		Supports @discord-user conversion to name in cc
		Supports #discord-channel conversion to name in cc
		Supports :emote: conversion to name in cc
	keep_alive.py - Prevents bot from being logged out and auto re-logs after 6 hour log
		NOTE: Autoclickers are bannable. Use at your own risk
	Note that there is no support to relog after the weekly update. You must manually restart Runelite
	mention.py - Turns @user@ into a proper Discord mention
	mouse_pos.py - Use to find appropriate mouse locations during setup of keep_alive.py
	ccbot_logger.py - Logs all messages sent to the CC Clone bot with Discord ID
		Prevents people impersonating others nefariously
	ccbot_commands.py - Allows !commands to be used in CC
	ccbot_commands.cfg - Allows controlling which commands will work in CC
	cc_metrics.py - Pushes cc data such as logins and messages to Google Sheets

Discord commands

	!discord - Friendly link to the Discord server
		Supports CCBot use
	!givefriend <@User> <RSN> - Give user Clan Friend rank and add them to the Clan Spreadsheet
		If the user is already a clan member, it removes member role
		Requires manage roles permissions
	!giverank <@User> <RSN> - Give user Member rank and add them to the clan spreadsheet
		If the user is already a clan friend, it removes friend role
		Requires manage roles permissions
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
	!online - Shows RSNs of all players currently online in CC
	!poll <mins> <question> <opt1> .. <opt 8>
		Create a poll that lasts for <mins> minutes
		Up to 8 available options
		Use reactions to answer
	!poll_cancel <number>
		Cancel a specific poll number
		Users are able to only cancel their own polls
		Mods/Admins can calcel any poll
	!raids - Gives a link to the Level 3 Raids Discord server
		Supports CCBot use
	!rankup.py <@User> - Refresh user stats in Clan Spreadsheet and give new rank to member
	!reminder - Drink Up!
		Supports CCBot use
	!signup - Tells mods you have passed probation and want to join sotw
		Supports CCBot use
	!sotw - Shows whetever is set by !sotw_set
		Supports CCBot use
	!sotw_set <cc/disc> <"message"> - Set a pre-recorded !sotw message; supports seperate messages for CC and Disc
		Requires manage messages permissions
	!stats <rsn> - Shows stats for a specified RSN. Use quotes if RSN contains spaces "Eg RSN"
	!sotw - shows a predefined message in sotw.msg
		Supports CCBot use
	!welcome_set <"message"> - Set a pre-recorded welcome message
		Requires manage messages permissions

Other

	disc_commands.cfg - Allows controlling what is shown by !commands in Discord
	reaction_roles.py - Gives users roles when reacting to a specified message
	welcome.py - Shows a pre-recorded message when a new user joins the Discord

Runelite Plugin
	
	There are two java files that comprise a custom Runelite plugin, Chat Logger Extended. 

===== Setup Instructions =====

To run this bot you will need 1 headless linux server and 1 headed pc, any OS. 
The OS for the headed PC must be capable of running Runelite. 
Debian is recommended for the Linux server. 
If the headed PC is running Linux, it can double as the headless linux server. 
You will not be able to use the headed PC once scripts are running, they will take over your mouse and keyboard. 

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
	typing-extensions

Create your .env file

	Create a file called .env using this template:

	TOKEN=123hjk123hjk123hjk123hjk123hjk123hjk123hkj
	cclog=C:\\Users\\Admin\\.runelite\\chatlogs\\friends\\latest.log
	sheet=123ghj123ghj123gjh543ghj6iuy654iuy654iuy654
	password=hunter2
	ironman=<:ironman:4356734645643564536>
	hcim=<:HCIM:4356456435643653456>
	uim=<:UIM:43563456435634564356>
	hp10=<:10hp:124234235423453425324>
	skiller=<:skiller:3245324523453425>
	f2p=<:f2p:34532452345234532>
	maxed=<:maxed:4563456345643563456>
	champ=<"champ:7345897234895>
	channel=12321312312312332123
	botchan=798437598347598347859
	reactchan=435984738298573849589342
	reactmsg=39045830492589034
	leader=32904583904589034
	council=89034859034850345
	welcome_chan=348093845908390534


	Populate the .env file as described:
		TOKEN is your Discord Bot Token
		cclog is the full filepath of the runelite cc log, latest.log
		sheet is the unique id of the google sheet storing your member data
		password is the osrs password for the account running discord_to_cc/cc_to_discord
		ironman is the emote id of an ironman helm in your discord server
		hcim is the emote id of a hcim helm in your discord server
		uim is the emote id of a uim helm in your discord server
		hp10 is the emote id of a 10HP logo in your discord server
		skiller is the emote id of a skiller logo in your discord server
		f2p is the emote id of a f2p logo in your discord server
		maxed is the emote id of a maxed logo in your discord server
		champ is the emote id of a champ cape logo in your discord server
		channel is the discord channel id where ccbot will run
		botchan is channel that only bots can access to pass data between them
		reactchan is the channel where reaction_roles will run
		reactmsg is the message in reactchan where reaction_roles will run
		leader is the UID of the leader role
		council is the UID of the council role
		welcome_chan is the channel where new member notifications are shown

Additional setup for the headed PC

	Open Runelite
	Install the plugin "Chat Logger" and enable it
	Login in to an account
	Recommend using a burner account and connecting pc to a VPN, bot ban IS possible
	Note that the burner must have a minimum total level of 150 to join a CC
	Join the CC you desire to sync between Discord and in-game CC
	Put runelite in the top-left of your screen
	Note that the keep_alive.py and disc_to_cc.py are designed for a 4K screen
	If running a different resolution you must change the moveTo() command locations
	Use mouse_pos.py to calibrate this
	By default Chat Logger does not support login/logout messages, but many CCBot features require this
	In order to support this you must compile Runelite from source and inject the 2 .java files as a custom plugin
	After Runelite is compiled, just turn on Chat Logger Extended
	Checkout this guide on Runelite plugin development:
		https://www.osrsbox.com/blog/2018/08/10/writing-runelite-plugins-part-1-building/
		https://www.osrsbox.com/blog/2018/08/12/writing-runelite-plugins-part-2-structure/
		https://www.osrsbox.com/blog/2018/08/18/writing-runelite-plugins-part-3-config/
		https://www.osrsbox.com/blog/2019/01/17/writing-runelite-plugins-part-4-overlays/

Additional setup for the headless linux server

	Perform the steps under the heading "Google Drive API and Service Account" on 
	https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
	Put the client_secret.json in the same folder as the git repo
	Add cc_metrics to your crontab to run daily

Clone the git repo. Recommend using the master branch
