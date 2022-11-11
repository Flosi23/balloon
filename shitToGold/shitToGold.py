import sys
import datetime

#srcDir = sys.argv[1]

srcDir ="/Users/simon/Documents/P-Seminar/Daten Misson vom 28.03.2017 DLR/Data Mission 28 03 2017/" 

lines = []

def formatLine(line):
    fields = line.replace("\n","").split(',')

    for i in range(0, len(fields)):
        fields[i] = fields[i].split(' ')[1]

    hms = list(map(lambda x: int(x), fields[6].split(":")))
    dm  = list(map(lambda x: int(x), fields[7].split("/")))
    
    timestamp = 0
    # If month or day are invalid values set 0 as unix timestamp
    if dm[0] > 0 or dm[0] <= 31 or dm[1] > 0 or dm[1] <= 12:
        time = datetime.datetime(2022, dm[0], dm[1], hms[0], hms[1],hms[2])
        timestamp = datetime.datetime.timeStamp(time) * 1000

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


