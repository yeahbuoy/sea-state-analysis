import os
import csv


# this script assumes that all the picture are already in a folder within the same directory as this script
# also assumes that all the data is using the same naming schemes (such as all photos are labeled with

PicturesDir = "Pictures"
WindFile = "41001_201812061335-WIND.csv"
WaveFile = "41001_201812061340-WAVE.csv"
NewFileName = "CoolSpreadSheet.csv"


listOfPics = os.listdir(PicturesDir)


def getWindList2D():

    tempList = []
    with open(WindFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            tempRow = []
            if line_count == 0:
                print("")
                line_count += 1
            else:
                tempRow.append(row[0])  # this will be the datetime
                tempRow.append(row[1])  # this will be the wind speed in m/s
                tempList.append(tempRow)
                line_count += 1

    return tempList

def getWaveList2D():

    tempList = []
    with open(WaveFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            tempRow = []
            if line_count == 0:
                print("")
                line_count += 1
            else:
                tempRow.append(row[0])  # this will be the datetime
                tempRow.append(row[3])  # this will be the wind speed in m/s
                tempList.append(tempRow)
                line_count += 1

    return tempList

def isWindTimeTheSame(pictureTime, dataTime):
    pictureDay = pictureTime[11:13]
    pictureMonth = pictureTime[14:16]
    pictureYear = pictureTime[6:10]
    pictureTime0 = pictureTime[17:21]

    dataDay = dataTime[0:2]
    dataMonth = dataTime[3:5]
    dataYear = dataTime[6:10]
    dataTime0 = dataTime[11:]


    if(pictureDay == dataDay and pictureMonth == dataMonth and pictureYear == dataYear and pictureTime0 == dataTime0):
        return True
    else:
        return False


def isWaveTimeTheSame(pictureTime, dataTime):
    pictureDay = pictureTime[11:13]
    pictureMonth = pictureTime[14:16]
    pictureYear = pictureTime[6:10]
    pictureTime0 = pictureTime[17:19]

    dataDay = dataTime[0:2]
    dataMonth = dataTime[3:5]
    dataYear = dataTime[6:10]
    dataTime0 = dataTime[11:13]

    if(pictureDay == dataDay and pictureMonth == dataMonth and pictureYear == dataYear and pictureTime0 == dataTime0):
        return True
    else:
        return False



newList = []
windList = getWindList2D()
waveList = getWaveList2D()

for picture in listOfPics:
    tempRow = []
    tempRow.append(picture)
    hadWind = False
    hadWave = False

    for windLine in windList:
        if(isWindTimeTheSame(picture,windLine[0])):
            if(windLine[1] != ""):
                tempRow.append(windLine[1])
                hadWind = True
            break

    for wavLine in waveList:
        if(isWaveTimeTheSame(picture,wavLine[0])):
            if (wavLine[1] != ""):
                tempRow.append(wavLine[1])
                hadWave = True
            break

    if(hadWind and hadWave):
        newList.append(tempRow)


myFile = open(NewFileName, 'w')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(newList)
