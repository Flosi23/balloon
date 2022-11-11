import sys
import datetime

# Specifying the srcDir like this means that this script expects to be executed from ./balloon/shitToGold!
srcDir ="./rawdata/" 

lines = []

def createUnixTimestamp(month, day, hour, minute, second):
    timestamp = 0
    # Only create a unix timestamp if the given parameters are valid
    if (
        (month >= 1 and month <= 12) and 
        (day >= 1 and day <= 31) and 
        (hour >= 0 and hour < 24) and 
        (minute >= 0 and minute < 60) and
        (second >= 0 and second < 60)
    ):
        timestamp = datetime.datetime(2022, month, day, hour, minute,second).timestamp()

    return timestamp

def parseRawDateAndTimeToUnixTimestamp(md,hms):
    month = int(md[0])
    day = int(md[1])
    hour = int(hms[0])
    minute = int(hms[1]) 
    second = int(hms[2])
    return createUnixTimestamp(month, day, hour, minute, second)


def formatLine(line):
    fields = line.replace("\n","").split(',')

    for i in range(0, len(fields)):
        fields[i] = fields[i].split(' ')[1]

    timestamp = parseRawDateAndTimeToUnixTimestamp(fields[6], fields[7])

    fields[6] = timestamp
    del fields[7]

    return ",".join(fields)

def cleanUpLines():
    lastLineSeconds = -1
    i = 0
    while i < len(lines):
        thisLineSeconds = int(lines[i].split(',')[0])
        if thisLineSeconds == lastLineSeconds:
            del lines[i-1]
        else:
            i += 1
        lastLineSeconds = thisLineSeconds


for i in range(0,99):
    try:
        filename = "DATA_"+f'{i:02d}'+".TXT"
        f = open(srcDir + filename,"r")
        flines = f.readlines()

        for i in range(0, len(flines)):
            formattedLine = formatLine(flines[i])
            lines.append(formattedLine)

        f.close()
    except e: 
        print("Unable to open file", e)

lines = sorted(lines, key=lambda line: line.split(',')[0])

cleanUpLines()

f = open("./data.csv", "w")
f.write("\n".join(lines))
f.close()


