import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from flask_mail import Mail, Message 
from flask import Flask, flash, jsonify, redirect, render_template, request, session # type: ignore
from flask_session import Session
from statistics import mean
from cs50 import SQL
from functools import wraps
import re

# Configure application
# Initialize the app
app = Flask(__name__)
app.config.from_object('config.Config')
mail = Mail(app)
db = SQL(app.config['DATABASE'])
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///moisture.db")

# Create the SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D8)

# Create the MCP3008 object
mcp = MCP.MCP3008(spi, cs)

# Create an analog input channel on Pin 0
chan = AnalogIn(mcp, MCP.P0)

# Sensor readings wet soil
min_value = 56060
# Sensor readings dry soil
max_value = 29532

def moisture():
    # Go from current value to moisture percentage
    def percentage(value_now):
         moist = (value_now - min_value)/(max_value-min_value)
         return moist

    rollingmean=[]
        
    for x in range(5):
        rollingmean.append(chan.value)
        time.sleep(0.5)
             
    average_value = mean(rollingmean)     
    return (percentage(average_value))
        #
        # #make an update for the next database update
        ##in case nothing is being updated create an update with value None
    
def plants_required(f):
    @wraps(f)
    def decoratedfunction(*args, **kwargs):
            if len(db.execute("SELECT * from plants")) == 0:
                return render_template(("first.html"))
            return f(*args, **kwargs)
    return decoratedfunction

# attribution cs50 duck
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def email_alert():
    users = db.execute("SELECT name, mail from mailadresses")
    for user in users:
        msg = Message(subject = 'TEST, I am thirsty', sender ='plantje.dorstig@gmail.com', recipients = [user["mail"]])
        msg.body = f'Hello {user["name"]}, I need water! \n Yours Sincerely, \nYour favourite plant'
        mail.send(msg) 

def email_happy(recipient = ["jeroen.vanasten@icloud.com"], name = "Jeroen"):
    users = db.execute("SELECT name, mail from mailadresses")

    for user in users:
        msg = Message(subject = 'Pfoe, I feel so much better :)', sender ='plantje.dorstig@gmail.com', recipients = [user["mail"]])
        msg.body = f'Thanks guys, I am fine now! \n Yours Sincerely, \nYour favourite plant'
        mail.send(msg) 

def mail_checker(app, value, confirmation):
    #checks if email has been sent of not in case both are true an email will be sent
    if value > 0.8 and confirmation == False:
       with app.app_context():
            email_happy()
            return True
    #if email have been sent resets in the middle
    elif value < 0.75 and value > 0.45:
        return False
    
    #checks if email has been sent of not in case both are true an email alert will be sent
    elif value < 0.4 and confirmation == False:
        with app.app_context():
            email_alert()
            return True
    #in the value goes into a buffer are (in between 0.4 and 0.45). The value will be returned of the current state. This to make sure only one email gets sent
    else:
        return confirmation
     

# Update database every five minutes and check if mail needs to be sent
def update_db(app, wait):
    confirmation = False
    while True:
        value = moisture()
        confirmation = mail_checker(app, value, confirmation)
        plant = db.execute("SELECT id FROM plants")[0]["id"]
        db.execute("INSERT INTO saturation_data (id, saturation) VALUES (?,?)", plant , value)
        time.sleep(wait)
# threat the checker
    
if __name__ == "__main__":
    moisture()