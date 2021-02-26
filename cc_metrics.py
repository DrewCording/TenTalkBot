#!/bin/python3 -u
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import re
import time

load_dotenv()

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
sheetclient = gspread.authorize(creds)
metric_sheet = sheetclient.open_by_key(os.getenv('sheet')).worksheet("CC Stats")

login_file = open("cc_logins.log", "r")
logged_users = login_file.read()
login_file.close()
os.remove("cc_logins.log")

mesg_file = open("cc_messages.log", "r")
mesgd_users = mesg_file.read()
mesg_file.close()
os.remove("cc_messages.log")

frst_ptrn = "\=(.*?)\+"

while logged_users:
    user = logged_users.splitlines()[0]
    user_count = logged_users.count(user)

    i=1
    flag=0
    for rsn in metric_sheet.col_values(1):
        if str(rsn) == str(user):
            if metric_sheet.cell(i, 2).value:
                old_week = str(metric_sheet.cell(i, 5, value_render_option='FORMULA').value)
                old_mnth = str(metric_sheet.cell(i, 6, value_render_option='FORMULA').value)
    
                frst_week = re.search(frst_ptrn, old_week)
                frst_mnth = re.search(frst_ptrn, old_mnth)
    
                full_week = str("=" + frst_week.group(1) + "+")
                full_mnth = str("=" + frst_mnth.group(1) + "+")
    
                new_week = old_week.replace(full_week, "=")
                new_mnth = old_mnth.replace(full_mnth, "=")
    
                new_week = str(new_week + "+" + str(user_count))
                new_mnth = str(new_mnth + "+" + str(user_count))
    
                metric_sheet.update_cell(i, 3, str(date.today()))
                metric_sheet.update_cell(i, 4, user_count)
                metric_sheet.update_cell(i, 5, new_week)
                metric_sheet.update_cell(i, 6, new_mnth)

            else:
                metric_sheet.update_cell(i, 2, str(date.today()))
                metric_sheet.update_cell(i, 3, str(date.today()))
                metric_sheet.update_cell(i, 4, user_count)
                metric_sheet.update_cell(i, 5, str("=0+0+0+0+0+0+" + str(user_count)))
                metric_sheet.update_cell(i, 6, str("=0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+" + str(user_count)))
    
            flag=1
            break
        i=i+1

    if not flag:
        metric_sheet.update_cell(i, 1, user)
        metric_sheet.update_cell(i, 2, str(date.today()))
        metric_sheet.update_cell(i, 3, str(date.today()))
        metric_sheet.update_cell(i, 4, user_count)
        metric_sheet.update_cell(i, 5, str("=0+0+0+0+0+0+" + str(user_count)))
        metric_sheet.update_cell(i, 6, str("=0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+" + str(user_count)))

    logged_users = logged_users.replace(str(user + "\n"), "")
    time.sleep(15)


while mesgd_users:
    user = mesgd_users.splitlines()[0]
    user_count = mesgd_users.count(user)

    i=1
    flag=0
    for rsn in metric_sheet.col_values(1):
        if str(rsn) == str(user):
            if metric_sheet.cell(i, 7).value:
                old_week = str(metric_sheet.cell(i, 10, value_render_option='FORMULA').value)
                old_mnth = str(metric_sheet.cell(i, 11, value_render_option='FORMULA').value)
    
                frst_week = re.search(frst_ptrn, old_week)
                frst_mnth = re.search(frst_ptrn, old_mnth)
    
                full_week = str("=" + frst_week.group(1) + "+")
                full_mnth = str("=" + frst_mnth.group(1) + "+")
    
                new_week = old_week.replace(full_week, "=")
                new_mnth = old_mnth.replace(full_mnth, "=")
    
                new_week = str(new_week + "+" + str(user_count))
                new_mnth = str(new_mnth + "+" + str(user_count))
    
                metric_sheet.update_cell(i, 8, str(date.today()))
                metric_sheet.update_cell(i, 9, user_count)
                metric_sheet.update_cell(i, 10, new_week)
                metric_sheet.update_cell(i, 11, new_mnth)

            else:
                metric_sheet.update_cell(i, 7, str(date.today()))
                metric_sheet.update_cell(i, 8, str(date.today()))
                metric_sheet.update_cell(i, 9, user_count)
                metric_sheet.update_cell(i, 10, str("=0+0+0+0+0+0+" + str(user_count)))
                metric_sheet.update_cell(i, 11, str("=0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+" + str(user_count)))
    
            flag=1
            break
        i=i+1

    if not flag:
        metric_sheet.update_cell(i, 1, user)
        metric_sheet.update_cell(i, 7, str(date.today()))
        metric_sheet.update_cell(i, 8, str(date.today()))
        metric_sheet.update_cell(i, 9, user_count)
        metric_sheet.update_cell(i, 10, str("=0+0+0+0+0+0+" + str(user_count)))
        metric_sheet.update_cell(i, 11, str("=0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+" + str(user_count)))

    mesgd_users = mesgd_users.replace(str(user + "\n"), "")
    time.sleep(15)
