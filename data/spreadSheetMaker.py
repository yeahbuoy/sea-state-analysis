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
                tempRow.append(row[4])  # this will be the wind speed in m/s
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


def getBeaufortForceFromWind(windFloat):
    knots = convertToKnots(windFloat)

    if(knots < 1):
        return 0
    elif(knots < 4):
        return 1
    elif (knots < 7):
        return 2
    elif (knots < 11):
        return 3
    elif (knots < 17):
        return 4
    elif (knots < 22):
        return 5
    elif (knots < 28):
        return 6
    elif (knots < 34):
        return 7
    elif (knots < 41):
        return 8
    elif (knots < 48):
        return 9
    elif (knots < 56):
        return 10
    elif (knots < 64):
        return 11
    elif (knots >= 64):
        return 12

def getBeaufortForceFromWave(waveFloat):

    ## comments reference actual scale (which has several overlaps)

    if(waveFloat < .1):
        ##sea like mirror
        return 0
    elif(waveFloat < .2):
        ## .1
        return 1
    elif (waveFloat < .6):
        ## .2 - .3
        return 2
    elif (waveFloat < 1):
        ## .6 - 1
        return 3
    elif (waveFloat < 2):
        ## 1 - 1.5
        return 4
    elif (waveFloat < 3):
        ## 2 - 2.5
        return 5
    elif (waveFloat < 4):
        ## 3 - 4
        return 6
    elif (waveFloat < 5.5):
        ## 4 - 5.5
        return 7
    elif (waveFloat < 7.5):
        ## 5.5 - 7.5
        return 8
    elif (waveFloat < 10):
        ## 7 - 10
        return 9
    elif (waveFloat < 12.5):
        ## 9 - 12.5
        return 10
    elif (waveFloat < 16):
        ## 11.5 - 16
        return 11
    elif (waveFloat >= 16):
        ## POSEIDON's WRATH
        return 12

def convertToKnots(WindMS):
    return (float(WindMS)*1.943844)



newList = []
windList = getWindList2D()
waveList = getWaveList2D()
firstRow = ["PictureName", "WindSpeed(m/s)", "WaveHeight(m)", "BeaufortForce"]
newList.append(firstRow)

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
        ## get BeafortForce from wind
        tempRow.append(getBeaufortForceFromWind(tempRow[1]))
        newList.append(tempRow)


myFile = open(NewFileName, 'w')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(newList)

