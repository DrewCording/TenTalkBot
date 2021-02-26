#!/bin/python3 -u
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
sheetclient = gspread.authorize(creds)

login_file = open("cc_logins.log", "r")
logged_users = login_file.read()
login_file.close()

while logged_users:
    user = logged_users.splitlines()[0]
    print(user, "=", logged_users.count(user))
    logged_users = logged_users.replace(str(user + "\n"), "")

    #sheet = sheetclient.open_by_key(os.getenv('sheet')).worksheet("CC Stats")

    #for rsn in sheet.col_values(1):
    #    if str(rsn) == str(user):
    #        print("Found user ", membername, " on row ", i)
    #        sheet.update_cell(i, 12, "Should be banned")

