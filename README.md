# Welcome to plantinvaders # 
#### Video Demo:  https://youtu.be/jUbRthYP-_0
#### Description:

Plantinvaders is a flask application that represents virtually your household plant. The application was inspired by Tamagotchi. By using the application you get better insight into the waterlevel and it is a great tool for monitoring when to water your plant. Also you get better understanding in  the water usage of your plant.

##### Features of the application #####

- An easy to use and friendly looking interface.
- Get statistics to view the historical waterlevels of your plant
- Get notified by email when your plant needs to be watered.

#### SET-UP ####

##### For this app to work you need the following: #####

- A RaspberryPi 3B
- Capacitive Moisture sensor V1.2
- MCP3008
- Breadboard and wires

This page shows the circuit connection and the calibration.
https://www.instructables.com/Measuring-Soil-Moisture-Using-Raspberry-Pi/

##### Interface #####

After installing the app you have to set-up an email credentials. For this to work you have to create a .env file with the following key value pairs
EMAIL_USER = ["YOUR EMAIL"] *#only works with a gmail account*
EMAIL_PASS = ["YOUR PASSWORD"]

The plant uses sqlite3 to save the data for this to work you have to create a file called moisture.db and load the sensordata.sql file inside of this.

When everything is set-up you can run the app.py file and the application should start running. Now your are able to access the webapplication locally on your network.

### Code deepening ####

#### Helper.py ####
The main code for the app is inside the app.py. The supporting file, the helpers.py file consist of the functions being called by this main file. The function being used are:

moisture():
This function is responsible for checking the current waterlevel. By making use of the sensorreading of the capacitive moisture sensor. For the circuit connection, accessing the GPIO pins and the usage of the library, I would like to refer to the instructables page mentioned above. The two calibration points being used are the sensor dry and drained with water. The relationship between the waterlevel and motionsensor value is linear. 

*plants_required(f):*
This is a decorator function that is used to make certain app.routes not accesible as long as their are no plants created (named). It also consist of a wraps(f) function from the functools module and its used to preserve the metadata of the original function otherwise the plants_required decorator could not be used multipletimes since multiple functions would exist with the same metadata.

*is_valid_email(email):*
Check if the email that is being entered could exist. Created by using regex

*update_db(app, wait, name):*
This function is responsible for the updating of the database and checks whether if an emails needs to be send. The functional elements are moisture(), email_alert(plantname), email_happy(plantname = None), mail_checker(app, value, confirmation, name). More information can be viewed inside the helpersfile. How the update_db function is used in the main app will be be elaborated in the multithreading section. 

##### Multithreading #####
After initializing the app (and having named a plant). The function (from helpers.py, update_db)is being activated. Causing the moisture.db database being updated every 15 minutes with the current waterlevel. This function also checks whether the waterlevel has crossed a threshold or not, if true this activates the mailing list. Sending people on the list an email suggesting if plant needs te be watered or not. Since this function is running all the time on the background and to prevent the application from stopping, a multithread function is being used.

##### config.py #####
In this file the Mail is being configured, the port and mail server are assigned. 
For the username and password the .env file is being used to keep it more secure. This is user specific. Never share your password.

