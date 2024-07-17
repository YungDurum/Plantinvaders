# Welcome to plantinvaders # 
#### Video Demo:  https://youtu.be/jUbRthYP-_0
#### Description:

Plantinvaders is a flask application that represents virtually your household plant. The application was inspired by Tamagotchi. The app is designed as a tool to maintain the watering levels of the soil of your favourite plant, by using a capacitive soil moisture sensor and a Raspberry Pi. People who connect to the local network will be able to view the plant by visiting its ip-address in the webbrowser. Ones a connection is established you can view the current waterlevel in the soil. Every ten minutes the current waterlevel will be saved on a database. One of the features of the app is to be able to view the historical data of the soil at the stats-page. Another feature of the app is for people who wish to be notified whenever the plant is thirsty. You can sign-up for notifications with your emailaddress and name. In case the plants have been watered you also get an email, so you will not get stressed out, and the plant will not be drowned ;)

##### Features of the application #####

- An easy to use and friendly looking interface.
- Get statistics to view the historical waterlevels of your plant
- Get notified by email when your plant needs to be watered.

#### SET-UP ####

##### For this app to work you need the following: #####

- A RaspberryPi 3B running Raspbian GNU/Linux 11 (bullseye)
- Capacitive Moisture sensor link: https://banggood.onelink.me/zMT7/74qip91d
- ADC : MCP3008
- Breadboard and wires

This page shows the circuit connection, the calibration and code being used to access the sensor readings.
https://www.instructables.com/Measuring-Soil-Moisture-Using-Raspberry-Pi/

#### Application set-up ####

After installing the app you have to set-up your email credentials. For this to work you have to create a file named .env on the route level of the application with the following key-value pairs.
- EMAIL_USER = ["YOUR EMAIL"] *only works with a gmail account, if else is wished change the mailserver being found in Config.py file*
- EMAIL_PASS = ["YOUR PASSWORD"]

The plant uses sqlite3 to save the data for this to work you have to create a file called moisture.db and load the sensordata.sql file inside of this.  

*Code*   
sqlite3 moisture.db;  
.read sensordata.sql;  

When everything is set-up you can run the app.py file and the application should start running. Inside the terminal the ip-address of the webapplication will be displayed, use this to be able to access the webapplication locally on your network.

### Code deepening ###
The main code for the app is inside the app.py. The supporting file, the helpers.py file, consist of: setting up the environment of the app and mailservice; connecting to the database being used; defining the functions used by the app.py.

The design choice for separating the code in this matter is to create code that is more readable, and the database saves the most essential data for when something goes wrong and the app needs to restart.

#### app.py ####
Here it is determined to not cache data on the clientside. This is done because some information changes realtime and its is not favoured to have conflicts with the data on the clientside.

There is also a decorator called @plants_required some functions and therefor pages are not accesible if there is no plant registered.

##### Multithreading #####
After initializing the app and having created a name for a plant the function (from helpers.py, update_db) is being activated. Causing the moisture.db database being updated every 10 minutes with the current waterlevel. This function also checks if the waterlevel has crossed a threshold or not, if true this activates the mailing list. Sending people on the list an email suggesting if plant needs te be watered or not. Since this function is running all the time on the background and to prevent the application from stopping, a multithread function is being used.


#### Helper.py ####
The helpers file setsup the app and configures the app.

*moisture():*  
This function is responsible for checking the current waterlevel. By making use of the sensorreading of the capacitive moisture sensor. For the circuit connection, accessing the GPIO pins and the usage of the library I would like to refer to the instructables page mentioned above. The two calibration points being used are the sensor's readings when dry and drained with water. The relationship between the waterlevel and sensor reading value is linear. 

*plants_required(f):*  
This is a decorator function that is used to make certain app.routes not accesible as long as their are no plants created (named). It also consist of a wraps(f) function from the functools module and its used to preserve the metadata of the original function otherwise the plants_required decorator could not be used multipletimes since multiple functions would exist with the same metadata.

*is_valid_email(email):*  
Check if the email that is being entered could exist. Created by using regex

*update_db(app, wait, name):*  
This function is responsible for the updating of the database and checks whether if an emails needs to be send. The functional elements are moisture(), email_alert(plantname), email_happy(plantname = None), mail_checker(app, value, confirmation, name). More information can be viewed inside the helpers file. How the update_db function is used in the main app will be be elaborated in the multithreading section.

##### Config.py #####
In this file the Mail function from flask_mail is being configured, meaning the port and mail server are assigned. 
For the username and password the .env file is being used to keep it more secure. This is user specific. Never share your password.

##### moisture.db #####
The moisture.db file consists of the following tables: plants, saturation_data and mailadresses.
- plants table conceals the name of the plant and id.
- saturation_data table is the file being updated every 10 minutes and holds a *timestamp* with the datetime, the saturation level, and plant id.
- mailaddreses table hold the name and mailadresses of the people to be notified.

### HTML AND CHART JS ###
The pages are created by HTML/CSS and jinja. Most are design choices so I will not go into to much detail. One of the libraries I have used is ChartJS and with the help of the CHART JS youtube channel, I figured my way through the library. The graph that is designed can be zoomed in and out. In the end I was not really satisfied with the result. I hope to improve this in the future, and I hope to make this more user-friendly and easier to use for research purposes.

### Front-end design choices ###
For the design I wished to create a friendly, retro looking application thats easy to use.

THANKS CS50 for the opportunity to learn more about computerscience and programming. It is a rabbithole but fun :).

