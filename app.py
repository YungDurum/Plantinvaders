import os
from dotenv import load_dotenv
from helpers import moisture, plants_required, is_valid_email
from flask_session import Session
from flask import Flask, flash, jsonify, redirect, render_template, request, session 
from cs50 import SQL
from flask_mail import Mail, Message 
import threading
import time
import json
import re

#load env file
load_dotenv()

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///moisture.db")


# Configure application
app = Flask(__name__)

# app config
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False

# Flask-Mail config
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASS")

app.config["SESSION_PERMANENT"] = False

# Other email settings
# app.config["RAGTIME_ADMIN"] = os.environ.get('RAGTIME_ADMIN')
# app.config["RAGTIME_MAIL_SUBJECT_PREFIX"] = 'Ragtime —'
# app.config["RAGTIME_MAIL_SENDER"] = 'Ragtime Admin <ragtime.flask@gmail.com'

Session(app)

mail = Mail(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def email_alert():
    users = db.execute("SELECT name, mail from mailadresses")
    for user in users:
        msg = Message(subject = 'TEST, I am thirsty', sender ='plantje.dorstig@gmail.com', recipients = [user["mail"]])
        msg.body = f'Hello {user["name"]}, I need water! \n Your Sincerely, \nYour Favourite Plant'
        print("TEST")
        mail.send(msg) 

def email_happy(recipient = ["jeroen.vanasten@icloud.com"], name = "Jeroen"):
    users = db.execute("SELECT name, mail from mailadresses")
    print("SEND EMAIL HAPPY")

    for user in users:
        msg = Message(subject = 'Pfoe, I feel so much better :)', sender ='plantje.dorstig@gmail.com', recipients = [user["mail"]])
        msg.body = f'Thanks guys, I am fine now! \n Your Sincerely, \nYour Favourite Plant'
        mail.send(msg) 

def mail_checker(value,confirmation):
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
def update_db(wait):
    confirmation = False
    while True:
        value = moisture()
        confirmation = mail_checker(value, confirmation)
        plant = db.execute("SELECT id FROM plants")[0]["id"]
        db.execute("INSERT INTO saturation_data (id, saturation) VALUES (?,?)", plant , value)
        time.sleep(wait)
# threat the checker

thread = threading.Thread(target=update_db, args=(600,))

if db.execute("SELECT id FROM plants"):
    thread.start()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@plants_required
def index():
    value = moisture() * 100
    value_format = "{:.2f}".format(value)
    if value < 20:
        source = "static/verdrietig.png"

    elif value < 30:
        source= "static/boos.png"
    
    elif value < 50:
        source = "static/verontwaardigd.png"

    elif value < 80:
        source = "static/blij.png"

    elif value < 100:
        source = "static/verliefd.png"

    return render_template("index.html", plant_moist = value_format, picture = source)

@app.route("/new", methods=["GET", "POST"])
def addplant():
    if request.method == "POST":
        name = request.form.get("name")
        db.execute("INSERT INTO plants (name) VALUES (?)",name)
        thread.start()
        return redirect("/")
    return "error"

@app.route("/stats")
@plants_required
def stats():
    data = db.execute("SELECT timestamp, saturation FROM saturation_data")
    json_string = json.dumps(data)
    return render_template("graph.html", data=json_string)

@app.route("/notifications",  methods=["GET", "POST"])
@plants_required
def notify():
    if request.method == "GET":
        notify_info = db.execute("SELECT * FROM mailadresses")
        if not notify_info:
            return render_template("notifications.html")
       
        # mail should be anonymous
        for row in notify_info:
            row["mail"] = re.sub(r'.+(?=@.+?)', "xxxxx", row["mail"]) # stackoverflow @Briano
            
        return render_template("notifications.html", mail_data = notify_info)

    if request.method == "POST":
        mail_user = request.form.get("Mail-adress")
        name = request.form.get("name")

        if not is_valid_email(mail_user):
            flash('Mailaddress seems invalid!')
            return redirect("/notifications")
        
        for row in db.execute("SELECT * FROM mailadresses"):
            if row["mail"]==mail_user:
                flash('Mailadress already in list')
                return redirect("/notifications") 
        

        db.execute("INSERT INTO mailadresses (name, mail) VALUES (?,?)",name, mail_user)
        return redirect("/notifications")

@app.route("/delete",  methods=["POST"])
@plants_required
def delete():
    mail_id = request.form.get("delete")
    db.execute("DELETE FROM mailadresses WHERE id = ?", mail_id)
    return redirect("/notifications")

@app.route("/info")
@plants_required
def help():
    return (render_template("info.html"))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

