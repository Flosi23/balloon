import datetime
import random;

fileHandler = open("data.csv", "a")

headings = ["Time", "Temperature", "Humidity", "UV Index"]

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
    uvIndex = random.uniform(0, 13)
    return [time, temperature, humidity, uvIndex]

writeRow(headings)

for i in range(0, 100):
    writeRow(sampleRow())

fileHandler.close();