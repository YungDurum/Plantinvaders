import os
from moisturesensor_data import moisture, plants_required
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
import threading
import time
import json

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///moisture.db")

# Update database every five minutes 
def update_db(wait):
    while True:
        value = moisture()
        plant = db.execute("SELECT id FROM plants")[0]["id"]
        db.execute("INSERT INTO saturation_data (id, saturation) VALUES (?,?)", plant , value)
        time.sleep(wait)

thread = threading.Thread(target=update_db, args=(600,))

if db.execute("SELECT id FROM plants"):
    thread.start()

#create new datapoint every 5 minutes and thread this process

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
    value = "{:.2f}".format(value)
    return render_template("index.html", plant_moist = value)

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
def phonenumbers():
    if request.method == "GET":
        phonenumbers = db.execute("SELECT * FROM phonenumbers")
        for row in phonenumbers:
            anonymous = 8 *"*" + "{phone}"
            row["phone"]= anonymous.format(phone=row["phone"][-2:])
        # phonenumber should be anonymous
        if not phonenumbers:
            return render_template("notifications.html")
        return render_template("notifications.html", phone_data = phonenumbers)

        
    if request.method == "POST":
        phonenumber = request.form.get("phonenumber")
        name = request.form.get("name")
        db.execute("INSERT INTO phonenumbers (name, phone) VALUES (?,?)",name, phonenumber)
        return redirect("/notifications")

if __name__ == '__main__':
    app.run(debug=True)

