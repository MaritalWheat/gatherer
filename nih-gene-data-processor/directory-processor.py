import argparse
import glob

class Sample:
     bkgrdFile = None
     nucleiFiles = []

class FileData:
    def __init__(self, sampleName, timePoint, nucleusName, bottomPlane, topPlane):
        self.sampleName = sampleName
        self.timePoint = timePoint
        self.nucleusName = nucleusName
        self.bottomPlane = bottomPlane
        self.topPlane = topPlane
    redChannel = []
    greenChannel = []
    meanOfMeanRed = 0.0
    meanOfMeanGreen = 0.0
    area = 0;
    numberOfPlanes = 0
        
class DataLine:
    def __init__(self, number, area, mean, sampleMin, sampleMax, intDen, rawIntDen, channel):
        self.number = number
        self.area = area
        self.mean = mean
        self.sampleMin = sampleMin
        self.sampleMax = sampleMax
        self.intDen = intDen
        self.rawIntDen = rawIntDen
        self.channel = channel

def processFile(fileToProcess, fileData):
    
    
    numPlanes = int(fileData.topPlane) - int(fileData.bottomPlane) + 1
    redChannel = []
    redChannelIndex = 1
    meanOfMeanRed = 0.0
    greenChannel = []
    greenChannelIndex = 1
    meanOfMeanGreen = 0.0
    area = 0
    isHeaderLine = 1
    

    for line in fileToProcess:
        #print (line)
        
        #first line will be labels, check to ignore it first time through
        if (isHeaderLine != 1):
            tokens = line.split(",")
            
            #[num][label][area][mean][min][max][int][rawInt][channel]
            channel = tokens[8]
            if (int(channel) == 1):
                number = tokens[0]
            else:
                number = str(int(tokens[0]) - 1)
            area = tokens[2]
            mean = tokens[3]
            sampleMin = tokens[4]
            sampleMax = tokens[5]
            intDen = tokens[6]
            rawIntDen = tokens[7]
            thisLine = DataLine(number, area, mean, sampleMin, sampleMax, intDen, rawIntDen, channel)
            
            if (int(channel) == 1):
                redChannel.append(thisLine)
                if (redChannelIndex >= int(fileData.bottomPlane) and redChannelIndex <= int(fileData.topPlane)):
                    meanOfMeanRed += float(mean)
                redChannelIndex+=1
            else:
                greenChannel.append(thisLine)
                if (greenChannelIndex >= int(fileData.bottomPlane) and greenChannelIndex <= int(fileData.topPlane)):
                    meanOfMeanGreen += float(mean)
                greenChannelIndex+=1
                
        isHeaderLine = 0
    
    #write file data to object
    fileData.redChannel = redChannel
    fileData.greenChannel = greenChannel
    fileData.meanOfMeanRed = meanOfMeanRed/numPlanes
    fileData.meanOfMeanGreen = meanOfMeanGreen/numPlanes
    fileData.area = area
    fileData.numberOfPlanes = numPlanes
    return fileData

def writeToFile(sample):
    f = open('Output/' + sample.nucleiFiles[0].sampleName + '_' + sample.nucleiFiles[0].timePoint + '_combined.csv', 'w')
    f.write("Nucleus Name,Area,Number of Planes,MoM(Red), MoM(Green),Corrected Intensity(Red),CorrectedIntensity(Green),Ratio(Red:Green)\n")
    for nucleusFile in sample.nucleiFiles:
        f.write(nucleusFile.nucleusName + ",")
        f.write(nucleusFile.area + ",")
        f.write(str(nucleusFile.numberOfPlanes) + ",")
        f.write(str(nucleusFile.meanOfMeanRed) + ",")
        f.write(str(nucleusFile.meanOfMeanGreen) + ",")
        correctedIntensityRed = int(nucleusFile.area) * int(nucleusFile.numberOfPlanes) * (nucleusFile.meanOfMeanRed - sample.bkgrdFile.meanOfMeanRed)
        correctedIntensityGreen = int(nucleusFile.area) * int(nucleusFile.numberOfPlanes) * (nucleusFile.meanOfMeanGreen - sample.bkgrdFile.meanOfMeanGreen)
        f.write(str(correctedIntensityRed) + ",")
        f.write(str(correctedIntensityGreen) + ",")
        f.write(str(correctedIntensityRed/correctedIntensityGreen) + "\n")
    
    nucleusFile = sample.bkgrdFile
    f.write(nucleusFile.sampleName + ",")
    f.write(nucleusFile.area + ",")
    f.write(str(nucleusFile.numberOfPlanes) + ",")
    f.write(str(nucleusFile.meanOfMeanRed) + ",")
    f.write(str(nucleusFile.meanOfMeanGreen) + ",")
    correctedIntensityRed = int(nucleusFile.area) * int(nucleusFile.numberOfPlanes) * (nucleusFile.meanOfMeanRed - sample.bkgrdFile.meanOfMeanRed)
    correctedIntensityGreen = int(nucleusFile.area) * int(nucleusFile.numberOfPlanes) * (nucleusFile.meanOfMeanGreen - sample.bkgrdFile.meanOfMeanGreen)
    f.write(str(correctedIntensityRed) + ",")
    f.write(str(correctedIntensityGreen) + ",")
    #prevent division by zero for bkgrd
    #f.write(str(correctedIntensityRed/correctedIntensityGreen) + "\n")
    f.close()
############

files = glob.glob('*.csv')

#parser = argparse.ArgumentParser()
#parser.add_argument("file", help="file to read")
#args = parser.parse_args()

sample = Sample()

for currFile in files:
    print("Current file is: " + currFile)
    bottomPlane = input("Bottom plane: ")
    topPlane = input("Top plane: ")
        
    fileName = ((currFile).split("."))[0]
    fileNameTokens = fileName.split("_")
        
    thisFile = FileData(fileNameTokens[0], fileNameTokens[1], fileNameTokens[2], bottomPlane, topPlane)
        
    f = open(currFile)
        
    thisFile = processFile(f, thisFile)
    
    if (thisFile.nucleusName == "slidebkgrd"):
        sample.bkgrdFile = thisFile
    else:
        sample.nucleiFiles.append(thisFile)
    print(thisFile.meanOfMeanRed)

writeToFile(sample)
###########  
	
