from flask import flash, redirect, render_template, request
from helpers import  app, mail, db, moisture, plants_required, is_valid_email, update_db, email_welcome
import json
import re
import threading

# CONSTANTS (many assigned in helper file)
app
mail
db
NAME_PLANT = None # Gets assigned later when plant is named or already named
WAIT = 600 # time between every database update and when is checked if an email needs to be send

# if a plant has been declared.
if len(db.execute("SELECT * from plants")):
    NAME_PLANT = db.execute("SELECT * from plants")[0]['name'].upper()
    thread = threading.Thread(target=update_db, args=(app, WAIT, NAME_PLANT,))
    thread.start()

# All the app routes
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Home screen (decorator renders other page when no plant is registered)
@app.route("/")
@plants_required
def index():
    # What emoji does the plant have
    value = moisture() * 100 #to get percentage
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

    return render_template("index.html", plant_moist = value_format, picture = source, nameplant = NAME_PLANT )

# First time usage
@app.route("/new", methods=["GET", "POST"])
def addplant():
    if request.method == "POST":
        global NAME_PLANT
        NAME_PLANT = request.form.get("name")
        db.execute("INSERT INTO plants (name) VALUES (?)", NAME_PLANT)
        thread = threading.Thread(target=update_db, args=(app, WAIT, NAME_PLANT,))
        thread.start()
        return redirect("/")
    return "error"

# The page with the stats
@app.route("/stats")
@plants_required
def stats():
    data = db.execute("SELECT timestamp, saturation FROM saturation_data")
    json_string = json.dumps(data)
    return render_template("graph.html", data=json_string)

# The notifications page and page where you can add yourself too.
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
        email_welcome(recipient=[mail_user], name = name, plantname = NAME_PLANT)
        return redirect("/notifications")

# Delete you from the list
@app.route("/delete",  methods=["POST"])
@plants_required
def delete():
    mail_id = request.form.get("delete")
    db.execute("DELETE FROM mailadresses WHERE id = ?", mail_id)
    return redirect("/notifications")

# Info page
@app.route("/info")
def help():
    return (render_template("info.html"))

# Info page
@app.route("/contactme")
def contact():
    return (render_template("contactme.html"))

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0',use_reloader=False)

