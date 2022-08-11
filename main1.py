# #!/usr/bin/python

# # This is a simple bot with schedule timer
# # https://schedule.readthedocs.io
# # -*- coding: utf-8 -*-
# """
# This Example will show you how to use register_next_step handler.

from asyncio.windows_events import NULL
import pygsheets
from email import message
import telebot
from telebot import types
from datetime import datetime


# pygsheet
service_file = r'C:\Users\Administrator\Downloads\testproject123-357604-cfc897e14f4b.json'
gc = pygsheets.authorize(service_file=service_file)
sheetname = 'timelog'
sh = gc.open(sheetname)
wks = sh.worksheet_by_title('testlog')
wksnames = sh.worksheet_by_title('interns')


API_TOKEN = '5409120688:AAH99qIqgvRv6Aj-ojQK-1BNa6JHsw_LqaY'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

print("Bot starting..")

class User:
    def __init__(self, name):
        self.timein = name
        self.timeout = None

@bot.message_handler(commands=['help','start'])
def send_help(message):
    msg = bot.reply_to(message,
"""I am DTR Sample bot.\nAvailable commands on this bot\n
Type /timein to login
Type /timeout to logout
Type /status\n\n

""")


@bot.message_handler(commands=['timein'])   
# Timein

def process_timein(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        try:
            now = datetime.now()
            date_time = now.strftime("%H:%M:%S")
            time = now.strftime("%H:%M:%S")
            date = now.strftime('%m/%d/%y')
            chat_id = message.chat.id
            timein = message.text

            user = User(timein)
            user_dict[chat_id] = user
            user.timein = date_time
            
            if timein == "/timein":
                user_first_name = str(message.chat.first_name)
                user_last_name = str(message.chat.last_name)
                full_name = user_first_name + " "+ user_last_name
                grecord = wks.get_all_records()
                num = 2
                for i in range(len(grecord)):
                    num+=1
                    if full_name == grecord[i].get("Name") and date == grecord[i].get("Date"):
                        bot.reply_to(message, f'You already timed in for this day')
                        break
                else: 
                    wks.update_value((num,1),full_name)
                    wks.update_value((num,2),date)
                    wks.update_value((num,3),time)    
                    bot.reply_to(message, f'Successfully timed in on {str(date_time)}')
                            

        except Exception as e:
            bot.reply_to(message, 'Try again.')

    else:
        bot.reply_to(message, 'You are not authorized to use this, Sorry')
@bot.message_handler(commands=['timeout'])  
# Timeout
def process_timeout(message):
    try:
        now2 = datetime.now()
        date_time2 = now2.strftime("%H:%M:%S")
        time = now2.strftime("%H:%M:%S")
        timeout = message.text 
        user = User(timeout)
        user.timeout = date_time2
        user_first_name = str(message.chat.first_name)
        user_last_name = str(message.chat.last_name)
        full_name = user_first_name + " "+ user_last_name
        date = now2.strftime('%m/%d/%y')

        if timeout == "/timeout":
            grecord = wks.get_all_records()
            num = 1
            for i in range(len(grecord)):
                num += 1
                if full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timeout")== '':
                    print(num)
                    wks.update_value((num,4),time)
                    bot.reply_to(message, f'Successfully timed out on {str(date_time2)}')
                    break
                
                elif full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("timeout")!= '':
                    bot.reply_to(message, 'You have already timed out')


    except Exception as e:
        bot.reply_to(message, '')


# Status
@bot.message_handler(commands=['status'])  
def process_status(message):
    getusername = message.chat.username
    user_first_name = str(message.chat.first_name) 
    user_last_name = str(message.chat.last_name)
    full_name = user_first_name + " "+ user_last_name
    now = datetime.now()
    date = now.strftime('%m/%d/%y')
    grecord = wks.get_all_records()
    num = 1
    for i in range(len(grecord)):
        num += 1
        if full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timein")!= '' and grecord[i].get("Timeout")!= '':
            bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("Timein")}\nTimeout: {grecord[i].get("Timeout")}')
            break
        elif full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timein")!= '' and grecord[i].get("Timeout")== '':
            bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("Timein")}\nTimeout: NONE')
            break
    else:
        bot.reply_to(message, "You haven't TIMED IN yet today")  

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()




