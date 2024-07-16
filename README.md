# Welcome # 

Plantinvaders is a flask application that represents virtually your household plant. The application was inspired by Tamagotchi. By using the application you get better insight into the waterlevel and it is a great tool for monitoring when to water your plant. Also you get better understanding in  the water usage of your plant.

##### Features of the application #####

- An easy to use and friendly looking interface.
- Get statistics to view the historical waterlevels of your plant
- Get notified by email when your plant needs to be watered.

#### SET-UP ####

##### For this app to work you need the following: #####

- A RaspberryPi 3b
- Capacitive Moisture sensor V1.2
- MCP3008

This page shows the circuit connection and the calibration.
https://www.instructables.com/Measuring-Soil-Moisture-Using-Raspberry-Pi/

##### Interface #####

After installing the app you have to set-up an email credentials. For this to work you have to create a .env file with the following key value pairs
EMAIL_USER = ["YOUR EMAIL"] *#only works with a gmail account*
EMAIL_PASS = ["YOUR PASSWORD"]

The plant uses sqlite3 to save the data for this to work you have to create a file called moisture.db and load the sensordata.sql file inside of this.

When everything is set-up you can run the app.py file and the application should start running. Now your are able to access the webapplication locally on your network.

