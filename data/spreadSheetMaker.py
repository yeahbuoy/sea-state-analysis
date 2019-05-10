import os
import csv
import unittest


# this script assumes that all the picture are already in a folder within the same directory as this script
# also assumes that all the data is using the same naming schemes (such as all photos are labeled with

PicturesDirs = ["Pictures"]
WindFiles = ["41001_201812061335-WIND.csv","41048_201902061931 -WIND.csv","41048_201902191939 - WIND.csv"]
WaveFiles = ["41001_201812061340-WAVE.csv","41048_201902061917 -WAVE.csv","41048_201902191945 - WAVE.csv"]
NewFileName = "CoolSpreadSheet.csv"

def getListofPics():
    finalList = []
    for pics in PicturesDirs:
        tempList = os.listdir(pics)
        finalList += tempList

    return finalList


def getWindList2D():

    tempList = []
    for fileName in WindFiles:
        with open(fileName) as csv_file:
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
    for fileName in WaveFiles:
        with open(fileName) as csv_file:
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

def checkSpreadSheet():

    tempList = []
    for fileName in WaveFiles:
        with open(NewFileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if(len(row) > 0):
                    if line_count == 0:
                        line_count += 1
                    else:
                        if(len(row) < 4):
                            print(row[0])
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
    else:
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
    return (float(WindMS)*1.94384);


class UnitTests(unittest.TestCase):

    def test_knots_conversion(self):
        self.assertAlmostEqual(convertToKnots(11), 21.3823, 2)

    def test_beaufort_force_wind(self):
        self.assertEqual(getBeaufortForceFromWind(4.2), 3)

    def test_beaufort_force_wave(self):
        self.assertEqual(getBeaufortForceFromWave(.8), 3)

if __name__ == 'UnitTests':
    unittest.main()

newList = []
countList = [0,0,0,0,0,0,0,0,0,0,0,0,0]
total = 0
windList = getWindList2D()
waveList = getWaveList2D()
firstRow = ["PictureName", "WindSpeed(m/s)", "WaveHeight(m)", "BeaufortForce"]
newList.append(firstRow)
listOfPics = getListofPics()

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
            else:
                tempRow.append("")
            break

    ##if we get through the list and still no waves, append it as empty
    if(not hadWave):
        tempRow.append("")

    if(hadWind):
        ## get BeafortForce from wind
        BNumber = getBeaufortForceFromWind(tempRow[1])
        tempRow.append(BNumber)
        newList.append(tempRow)
        countList[BNumber] += 1
        total += 1

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


myFile = open(NewFileName, 'w')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(newList)

#checks to see if there are any empty slots, and prints out the image name if there was
checkSpreadSheet()

