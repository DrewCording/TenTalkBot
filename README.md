TenTalkBot
Discord Bot for OSRS CC Ten Talk

===== Bot Descriptions =====

Control scripts
	start.sh - Starts bots individually or all at once
	stop.sh - Stops bots individually or all at once
	restart.sh - Restarts bots individually or all at once

CC Clone
	cc_to_disc.py - Reads cc messages from latest.log and sends them to Discord on specified channel
	disc_to_cc.py - Reads discord messages from specified channel and sends them to CC
		NOTE: Autotypers are bannable. Use at your own risk
	keep_alive.py - Prevents bot from being logged out and auto re-logs after 6 hour log
		NOTE: Autoclickers are bannable. Use at your own risk
	Note that there is no support to relog after the weekly update. You must manually restart Runelite
	mention.py - Turns @user@ into a proper Discord mention
	logger.py - Logs all messages sent to the CC Clone bot with Discord ID
		Prevents people impersonating others to get them banned

Discord commands
	!hello - Hello! Use this to confirm the bot is connected to the server
	!stats <rsn> - Shows stats for a specified RSN. Use quotes if RSN contains spaces "Eg RSN"
	!move <#Channel> <message ids> - Moves the specified message IDs to the #Channel specified
	!giverank <@User> <RSN> - In development
	!rankdown.py <@User> - In development
	!rankup.py <@User> - In development

===== Setup Instructions =====

To run this bot you will need 1 headless linux server and 1 headed pc, any OS
The OS for the headed PC must be capable of running Runelite
Debian is recommended for the Linux server
If the headed PC is running Linux, it can double as the headless linux server
You will not be able to use the headed PC once scripts are running, they will take over your mouse and keyboard

Before running any programs, install python3 and the following pip packages onto both computers:
	discord
	discord.py
	google-auth
	google-auth-oauthlib
	gspread
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
	channel=12321312312312332123


	Populate the .env file as described:
		TOKEN is your Discord Bot Token
		cclog is the full filepath of the runelite cc log, latest.log
		sheet is the unique id of the google sheet storing your member data
		password is the osrs password for the account running discord_to_cc/cc_to_discord
		ironman is the emote id of an ironman helm in your discord server
		hcim is the emote id of a hcim helm in your discord server
		uim is the emote id of a uim helm in your discord server
		channel is the discord channel id where ccbot will run

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

Additional setup for the headless linux server
	Perform the steps under the heading "Google Drive API and Service Account" on 
	https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
	Put the client_secret.json in the same folder as the git repo

Clone the git repo. Recommend using the master branch
