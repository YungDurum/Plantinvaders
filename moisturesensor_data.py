import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from statistics import mean
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from functools import wraps


db = SQL("sqlite:///moisture.db")

def moisture():
    # Create the SPI bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # Create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D8)

    # Create the MCP3008 object
    mcp = MCP.MCP3008(spi, cs)

    # Create an analog input channel on Pin 0
    chan = AnalogIn(mcp, MCP.P0)

    # Sensor readings wet soil
    max_value = 56060
    # Sensor readings dry soil
    min_value = 29532

    # Go from current value to moisture percentage
    def percentage(value_now):
         moist = ((value_now - min_value) * 100)/(max_value-min_value)
         return moist


    while True:
        rollingmean=[]
        
        for x in range(10):
            rollingmean.append(chan.value)
            time.sleep(1)
            average_value = mean(rollingmean)
        
            return percentage(average_value)
        ##make an update for the next database update
        ##in case nothing is being updated create an update with value None
    
def plants_required(f):
    @wraps(f)
    def decoratedfunction(*args, **kwargs):
            if len(db.execute("SELECT * from plants")) == 0:
                return render_template(("first.html"))
            return f(*args, **kwargs)
    return decoratedfunction

if __name__ == "__main__":
    moisture()