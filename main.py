#!usr/bin/python
import datetime
import random
from time import sleep
import SI1145.SI1145 as SI1145
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_lps2x

fileHandler = open("data.csv", "a")

READING_INTERVAL = 2.0

uvSensor = SI1145.SI1145()
pressureSensor = adafruit_lps2x.LPS22(I2C(3))

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
    airPressure = random.uniform(1050, 100)
    uv = random.uniform(0, 13)
    ir = random.uniform(0, 100)
    visible = random.uniform(0, 20)
    return [time, temperature, airPressure, uv, ir, visible]
    
def readTempPressure():
    try:
        pressure = pressureSensor.pressure
        temp = pressureSensor.temperature

        return [temp, pressure]
    except Exception:
        return ["err", "err"]
        
def readIRVisibleUV():
    try:
        vis = uvSensor.readVisible()
        uv = uvSensor.readUV()
        ir = uvSensor.readIR()

        return [uv, ir, vis]
    except Exception:
        return ["err","err","err"]
    
def writeSample():
    for _ in range(0, 100):
        writeRow(sampleRow())

def writeSensorData():
    while True:
        tempPressure = readTempPressure()
        uvIRVisible = readIRVisibleUV()
        time = [datetime.datetime.now()]
        row = time + tempPressure + uvIRVisible
        print(row)
        writeRow(time + tempPressure + uvIRVisible)
        sleep(READING_INTERVAL)

writeSample()

fileHandler.close();


