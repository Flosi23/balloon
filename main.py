import datetime
import random
from time import sleep;
import adafruit_dht;
import board;
import SI1145.SI1145 as SI1145;

fileHandler = open("data.csv", "a")

READING_INTERVAL = 2.0

htSensor = adafruit_dht.DHT22(board.GPIO4)
uvSensor = SI1145.SI1145()

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
    try:
        temperature = htSensor.temperature
        humidity = htSensor.humidity
    except RuntimeError as error:
        print(error)
        sleep(2)
    except Exception as error:
        htSensor.exit()
        raise error
    
    return [temperature, humidity]

def readIRVisibleUV():
    try:
        vis = uvSensor.readVisible()
        uv = uvSensor.readUV()
        ir = uvSensor.readIR()
    except RuntimeError as error:
        print(error)
        sleep(2)
    except Exception as error:
        raise error

    return [uv, ir, vis]

def writeSample():
    for i in range(0, 100):
        writeRow(sampleRow())

def writeSensorData():
    while True:
        tempAndHum = readHumidityAndTemperature()
        uvIRVisible = readIRVisibleUV()
        writeRow(tempAndHum + uvIRVisible)
        sleep(READING_INTERVAL)

writeSample()

fileHandler.close();