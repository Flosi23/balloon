import sys

#srcDir = sys.argv[1]

srcDir ="/Users/simon/Documents/P-Seminar/Daten Misson vom 28.03.2017 DLR/Data Mission 28 03 2017/" 

lines = []

def formatLine(line):
    fields = line.replace("\n","").split(',')

    for i in range(0, len(fields)):
        fields[i] = fields[i].split(' ')[1]

    return ",".join(fields) 

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

lines = sorted(lines, key=lambda x: x[0])

f = open("./data.csv", "w")
f.write("\n".join(lines))
f.close()


