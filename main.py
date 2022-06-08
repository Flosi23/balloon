#!usr/bin/python

import datetime
import random
from time import sleep
import SI1145.SI1145 as SI1145
import pigpio
import DHT


fileHandler = open("data.csv", "a")

READING_INTERVAL = 2.0
RETRIES = 10

pi = pigpio.pi()

if not pi.connected:
    print("Pi not connected")
    exit()

dhtSensor = DHT.sensor(pi, 12, DHT.DHT11)

uvSensor = SI1145.SI1145()


dhtSensorRetries = RETRIES
uvSensorRetries = RETRIES

dhtSensorError = False
uvSensorError = False

headings = ["Time", "Temperature", "Humidity", "UV", "IR", "Visible"]

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

def readHumidityAndTemperature():
    global dhtSensorError
    global dhtSensorRetries

    if(dhtSensorError and dhtSensorRetries == 0):
        print("All 10 dhtSensor retries failed")
        return [0,0]

    timestamp, gpio, status, temperature, humidity = dhtSensor.read() 

    if(status == DHT.DHT_GOOD):
        return [temperature, humidity]

    if(status == DHT.DHT_TIMEOUT):
        print("DHT Sensor timed out")
        dhtSensorError = True
        dhtSensorRetries -= 1
        return [0,0]

    return [0,0]
    

def readIRVisibleUV():
    global uvSensorError
    global uvSensorRetries
    
    if(uvSensorError and uvSensorRetries == 0):
        print("All 10 uvSensor retries failed")
        return [0,0,0]

    try:
        vis = uvSensor.readVisible()
        uv = uvSensor.readUV()
        ir = uvSensor.readIR()

        return [uv, ir, vis]
    except Exception as error:
        uvSensorError = True
        uvSensorRetries -= 1
        return [0,0,0]
    
def writeSample():
    for i in range(0, 100):
        writeRow(sampleRow())

def writeSensorData():
    while True:
        tempAndHum = readHumidityAndTemperature()
        uvIRVisible = readIRVisibleUV()
        time = [datetime.datetime.now()]
        writeRow(time + tempAndHum + uvIRVisible)
        sleep(READING_INTERVAL)

readHumidityAndTemperature()

fileHandler.close();


