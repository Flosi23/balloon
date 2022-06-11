#!usr/bin/python
import datetime
import random
from time import sleep
import SI1145.SI1145 as SI1145
import board
import adafruit_lps2x

fileHandler = open("data.csv", "a")

READING_INTERVAL = 2.0
RETRIES = 10

uvSensor = SI1145.SI1145()
pressureSensor = adafruit_lps2x.LPS22(board.I2C())

pressureSensorRetries = RETRIES
uvSensorRetries = RETRIES

pressureSensorError = False
uvSensorError = False

headings = ["Time", "Temperature", "Air Pressure", "UV", "IR", "Visible"]

def writeRow(values):
    if(len(values) != len(headings)):
        raise "values.length must be equal of the length of the headings"

    row = str(values[0])

    for i in range(1, len(values)):
        row += "," + str(values[i])

    row += "\n"

    fileHandler.write(row)

def sampleRow():
    time = datetime.datetime.now()
    temperature = random.uniform(-50, 20)
    humidity = random.uniform(10, 50)
    uv = random.uniform(0, 13)
    ir = random.uniform(0, 100)
    visible = random.uniform(0, 20)
    return [time, temperature, humidity, uv, ir, visible]
    
def readTempPressure():
    global pressureSensorError
    global pressureSensorRetries

    if(pressureSensorError and pressureSensorRetries == 0):
        print("All 10 pressureSensor retries failed")
        return ["err","err"]
    
    try:
        pressure = pressureSensor.pressure
        temp = pressureSensor.temperature

        return [temp, pressure]
    except Exception:
        pressureSensorError = True
        pressureSensorRetries -= 1
        return ["err", "err"]
        
def readIRVisibleUV():
    global uvSensorError
    global uvSensorRetries
    
    if(uvSensorError and uvSensorRetries == 0):
        print("All 10 uvSensor retries failed")
        return ["err","err","err"]

    try:
        vis = uvSensor.readVisible()
        uv = uvSensor.readUV()
        ir = uvSensor.readIR()

        return [uv, ir, vis]
    except Exception:
        uvSensorError = True
        uvSensorRetries -= 1
        return ["err","err","err"]
    
def writeSample():
    for _ in range(0, 100):
        writeRow(sampleRow())

def writeSensorData():
    while True:
        tempPressure = readTempPressure()
        uvIRVisible = readIRVisibleUV()
        time = [datetime.datetime.now()]
        writeRow(time + tempPressure + uvIRVisible)
        sleep(READING_INTERVAL)

fileHandler.close();


