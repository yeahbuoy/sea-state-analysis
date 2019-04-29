import os
import csv
import unittest

NewFileName = "SuperCoolSpreadSheet.csv"
fileName = "CombinedSpreadSheet.csv"

def getCurrList():

    tempList = []
    firstRow = ["PictureName", "WindSpeed(m/s)", "WaveHeight(m)", "BeaufortForce", "BucketForce"]
    tempList.append(firstRow)
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print("")
                line_count += 1
            else:
                tempList.append(row)
                line_count += 1

    return tempList

def getBeaufortForceFromWind(windFloat):
    knots = convertToKnots(windFloat)

    if (knots < 7):
        return 1
    elif (knots < 22):
        return 4
    else:
        return 7

def convertToKnots(WindMS):
    return (float(WindMS)*1.94384);


currList = getCurrList()

countList = [0,0,0,0,0,0,0,0,0,0,0,0,0]
total = 0
index = 0
for currRow in currList:
    if(index != 0):
        wind = currRow[1]
        if(wind != "MM"):
            BNumber = getBeaufortForceFromWind(wind)
            currRow.append(BNumber)
            countList[BNumber] += 1
            total += 1
        else:
            currRow.append(4)

    index += 1

print("Beaufort Force 1: " + str(countList[0]))
print("Beaufort Force 2: " + str(countList[1]))
print("Beaufort Force 3: " + str(countList[2]))
print("Beaufort Force 4: " + str(countList[3]))
print("Beaufort Force 5: " + str(countList[4]))
print("Beaufort Force 6: " + str(countList[5]))
print("Beaufort Force 7: " + str(countList[6]))
print("Beaufort Force 8: " + str(countList[7]))
print("Beaufort Force 9: " + str(countList[8]))
print("Beaufort Force 10: " + str(countList[9]))
print("Beaufort Force 11: " + str(countList[10]))
print("Beaufort Force 12: " + str(countList[11]))
print("Beaufort Force 13: " + str(countList[12]))
print("Total images:" + str(total))

myFile = open(NewFileName, 'w',  newline='')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(currList)