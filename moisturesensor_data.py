import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from statistics import mean

def moisture():
    # Create the SPI bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # Create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D8)

    # Create the MCP3008 object
    mcp = MCP.MCP3008(spi, cs)

    # Create an analog input channel on Pin 0
    chan = AnalogIn(mcp, MCP.P0)

    start_time = time.time()
    i = 0


    while True:
        rollingmean=[]
        
        for x in range(10):
            rollingmean.append(chan.value)
            time.sleep(1)
        
        print("Time:", time.time()-start_time)
        print("The rolling average is:", mean(rollingmean))
        ##make an update for the next database update
        ##in case nothing is being updated create an update with value None
        

    ## create a database if is existing on the raspberry pi
    ##connect to the raspberry pi and request the data via a post request

#def createDB():
     

if __name__ == "__main__":
    moisture()