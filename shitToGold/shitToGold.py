import datetime

# Specifying the srcDir like this means that this script expects to be executed from ./balloon/shitToGold!
srcDir ="./rawdata/" 

lines = []

# The generated CSV has the form: 
#   0  Running second,
#   1  Pressure,
#   2  Humidity inside,
#   3  Temperature inside,
#   4  Humidity outside,
#   5  Temperature outside,
#   6  Unix timestamp,
#   7  GPS-Fix,
#   8  GPS-Satellites,
#   9  GPS-Length,
#   10 GPS-Width,
#   11 GPS-Height
# If a value was not recorded, the fields value will instead be "--.---"

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

def parseRawDateAndTimeToUnixTimestamp(hms, md):
    # md has the form [DAY,MONTH]
    month = int(md[1])
    day = int(md[0])
    # hms has the form [HOUR,MINUTE,SECOND]
    hour = int(hms[0])
    minute = int(hms[1]) 
    second = int(hms[2])
    return createUnixTimestamp(month, day, hour, minute, second)


def formatLine(line):
    # split the line in its columns
    fields = line.replace("\n","").split(',')

    # raw lines have the form: UNIT VALUE
    # we remove the unit, because we only want the value
    for i in range(0, len(fields)):
        fields[i] = fields[i].split(' ')[1]

    # take the two columns month/date and hour:minute:seconds and combine them into one unix timestamp column
    timestamp = parseRawDateAndTimeToUnixTimestamp(fields[6].split(":"), fields[7].split("/"))
    fields[6] = str(timestamp)
    del fields[7]

    # reassemble the fields into one line
    return ",".join(fields)

# cleanUpLines() loops through all lines and removes running seconds duplicates
def cleanUpLines():
    lastLineSeconds = -1
    i = 0
    # We do expect the lines to be sorted, thus duplicates have to appear after each other
    # Save running seconds of last line and compare them with current. If equal remove last line
    while i < len(lines):
        thisLineSeconds = int(lines[i].split(',')[0])
        if thisLineSeconds == lastLineSeconds:
            del lines[i-1]
        else:
            i += 1
        lastLineSeconds = thisLineSeconds


# loop through all 100 files, format each line and collect all lines in one array
for i in range(0,99):
    filename = "DATA_"+f'{i:02d}'+".TXT"
    f = open(srcDir + filename,"r")
    flines = f.readlines()

    for i in range(0, len(flines)):
        formattedLine = formatLine(flines[i])
        lines.append(formattedLine)


# Sort the lines by running seconds (lines[0])
lines = sorted(lines, key=lambda line: line.split(',')[0])

cleanUpLines()

f = open("./data.csv", "w")
f.write("\n".join(lines))
f.close()


