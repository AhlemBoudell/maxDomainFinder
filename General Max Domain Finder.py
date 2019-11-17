import os
import fnmatch
import math

class Domain:
    startPos = 0
    size = 0
    E_value = 0
    all_E_values = []
    all_Feat_counts = []
    all_feats = []

    def __init__(self, SP=0, S=0, E_list=[], F_list =[], allFs =[], a = []):
        self.startPos = SP
        self.size = S
        #self.E_value = E
        self.all_E_values = E_list
        self.calculateESum()
        self.all_Feat_counts = F_list
        self.all_feats = allFs
        self.allAnno = a

    def getStartPos(self):
        return self.startPos

    def getAnno(self):
        return self.allAnno

    def getAnnoStr(self):
        tempStr = ""
        for a in self.allAnno:
            tempStr += a+","
        if tempStr == "":
            tempStr = "-"
        return tempStr

    def getfeats(self):
        return self.all_feats

    def getSize(self):
        return self.size

    def getEvalue(self):
        return self.E_value

    def getElist(self):
        return self.all_E_values

    def getFlist(self):
        tempList = []
        for tfc in self.all_Feat_counts:
            tempList.append(int(tfc))
        return tempList

    def setDomain(self,SP, S, EL,Fs,As):
        self.startPos = SP
        self.size = S
        #self.E_value = E
        self.all_E_values = EL
        self.all_feats = Fs
        self.calculateESum()
        self.allAnno = As

    def slide(self,windowSize, newE):
        # move the starting position by one window
        self.startPos = self.startPos + windowSize
        # remove the E value of the removed window from the list and the total E value,
        # then add the new window E value
        #self.E_value = self.E_value - self.all_E_values[0] + newE
        self.all_E_values.pop(0)
        self.all_E_values.append(newE)
        self.calculateESum()

    def calculateESum(self):
        total = 0
        for e in self.all_E_values:
            total = total + e
        self.E_value = total
    def printDomain(self):
        print("Start Pos: " + self.startPos.__str__() + "   E value: " + self.E_value.__str__())

class DomainClass:
    classSize = 0
    classGroups = []
    classGroupsCounts= []

    def __init__(self, s=0):
        self.classSize = s
        self.classGroups=[]
        self.classGroupsCounts=[]

    def getSize(self):
        return self.classSize

    def getGroups(self):
        return self.classGroups

    def getOneGroupGroups(self, index):
        str = ""
        self.classGroups[index].sort()
        for g in self.classGroups[index]:
            str += g + ","
        return str[0:str.__len__()-1]

    def getGroupCounts(self):
        return self.classGroupsCounts

    def getGroupCountsStr(self):
        str = ""
        for g in self.classGroupsCounts:
            str = str + g.__str__() + ","
        return str[0:str.__len__()-1]

    def getGroupsStr(self):
        str = ""
        for g in self.classGroups:
            subStr = ""
            for sg in g:
                subStr = subStr + sg + ","
            subStr = subStr[0:subStr.__len__()-1]
            str = str + subStr.__str__() + "_"
        return str[0:str.__len__()-1]

    def addGroup(self,group):
        if group.__len__() == self.classSize:
            found = False
            for i in range(0, self.classGroups.__len__()):
                if self.AreSameList(self.classGroups[i], group):
                    self.classGroupsCounts[i]+=1
                    found = True
                    break

            if not found:
                self.classGroups.append(group)
                self.classGroupsCounts.append(1)
        else:
            print("Wrong Group size!")



    def AreSameList(self, L1,L2):
        if L1.__len__() != L2.__len__():
            return False
        else:
            for item in L1:
                if not L2.__contains__(item):
                    return False
            return True
    def getDiffGroups(self):
        return self.classGroups.__len__()

def FeatureGroupsFinder(ifile, ofile):
    istream = open(ifile,"r")
    ostream = open(ofile, "w")

    classesList =[]

    header = istream.readline()
    ostream.write(header)
    temp = istream.readline()
    ostream.write(temp)
    temp = istream.readline()
    temp = istream.readline()
    while temp!= "":
        lineParts = temp.strip().split("\t")

        if lineParts.__len__() == 4:
            fts = lineParts[3].strip().split(",")
            fts = fts[0:fts.__len__()-1]
            found = False
            for c in classesList:
                if c.getSize() == fts.__len__():
                    found = True
                    c.addGroup(fts)
                    break

            if not found:
                tempClass = DomainClass(fts.__len__())
                tempClass.addGroup(fts)
                classesList.append(tempClass)

        temp = istream.readline()

    classesList.sort(key=lambda x: x.classSize, reverse=True)
    strList = []
    ostream.write("ClassSize \t ClassesCount \t\t\t ClassesAndCounts \n")
    for c in classesList:
        if c.getSize()>1:
            ostream.write(c.getSize().__str__() + "\t"+ c.getDiffGroups().__str__()+"\n")
            for i in range (0, c.getGroups().__len__()):
                ostream.write(c.getGroupCounts()[i].__str__() + "\t" + c.getOneGroupGroups(i).__str__() + "\n")
                if strList.__contains__(c.getOneGroupGroups(i).__str__()):
                    print ("ERROR!!!!!")
                else:
                    strList.append(c.getOneGroupGroups(i).__str__())

    istream.close()
    ostream.close()

def FeatureGroupsFinderForDomains(feats):

    classesList =[]
    for flist in feats:
        found = False
        fts = flist.split(",")
        for c in classesList:
            if c.getSize() == fts.__len__():
                found = True
                c.addGroup(fts)
                break
        if not found:
            tempClass = DomainClass(fts.__len__())
            tempClass.addGroup(fts)
            classesList.append(tempClass)

    classesList.sort(key=lambda x: x.classSize, reverse=True)

    str = ""
    for c in classesList:
        str = str+ "[" + c.getSize().__str__() + "|" + c.getDiffGroups().__str__() + "]"

    return str

def featuresReader(folderDir, target = "A"):
    features = []
    fileName = ""
    if target.upper() == "C":
        fileName = folderDir + "commonFeaturesList.txt"
    #elif target.upper()== "U":
    #    fileName = folderDir + "uniqueFeaturesList.txt"
    else:
        # if not "C" or "U", it will be considered "A" regardless
        fileName = folderDir + "fullFeaturesList.txt"

    file = open(fileName,"r")
    line = file.readline().strip().split(":")
    counter = int(line[1])
    for i in range (0, counter):
        features.append(file.readline().strip())
    file.close()

    return features

def EntropyCalc(peakCount , totalHMcount):
    if peakCount ==0:
        return 0
    else:
        E = -(peakCount/totalHMcount) * math.log2((peakCount/totalHMcount))
        return E

def peakFinder(file_dir,features, chrmNumber = "I", minPos = 0, DomainSize = 3000, WindowSize = 200, targetFeature="C" ):
    maxPos = minPos + DomainSize
    windowsCount = math.ceil((maxPos - minPos) / WindowSize)
    chrfile = file_dir + "chr:"+ chrmNumber + "_targetFeatures:" + targetFeature+'_Listed.txt'
    chrStat = open(chrfile, "a")
    entries = os.listdir(file_dir)

    peaks = [0] * windowsCount
    ftPeaks = [""] * windowsCount
    filecount = 0

    for Gdir in entries:
        if Gdir.startswith("modEncode"):
            newDir = file_dir + Gdir + "/interpreted_data_files/"
            subEnt = os.listdir(newDir)
            for file in subEnt:

                if file.endswith(".gff3") or file.endswith(".gff"):
                    #filecount += 1
                    fname = newDir + file
                    with open(fname)as f:
                        # peakFound = False
                        nameSeg = file.strip().split("_")
                        hmtemp  = ''.join(e for e in nameSeg[2] if e.isalnum())
                        hmtemp.upper()
                        if (features.__contains__(hmtemp)):
                            WStart = minPos
                            WEnd = WStart + WindowSize

                            for line in f:
                                lineParts = line.strip().split("\t")
                                # print(lineParts)
                                if (lineParts[0] == chrmNumber) and not (lineParts[3]== ".") and not (lineParts[4]== "."):  # find only peaks of specified chromosome and ignore lines with errors
                                    #print(lineParts)
                                    #print(fname)

                                    if (int(lineParts[3]) >= minPos and int(lineParts[3]) <= maxPos) or (int(lineParts[4]) <= maxPos and int(lineParts[4]) >= minPos):
                                        # make sure the peaks are in the specified domain
                                        # calculate the span only for the windows in the Domain

                                        # peakFound = True
                                        spanStart = int(lineParts[3])
                                        if (minPos > spanStart):
                                            spanStart = minPos
                                        spanEnd = int(lineParts[4])
                                        if (spanEnd > maxPos):
                                            spanEnd = maxPos

                                        startPos = int((spanStart - minPos) / WindowSize)
                                        # endPos = int(spanEnd-minPos)/WindowSize
                                        if (int(spanEnd - minPos) % int(WindowSize)) == 0:
                                            endPos = int((spanEnd - minPos) / WindowSize) - 1
                                            # special case when end position is the start of next interval, so it doesnt count in the next one
                                        else:
                                            endPos = int((spanEnd - minPos) / WindowSize)

                                        # print("Peak found!! \n Start\t" + startPos.__str__() + "\t endPos \t" +endPos.__str__())
                                        # print("Peak found!! \n Start\t" + lineParts[3].__str__() + "\t endPos \t" + lineParts[4].__str__())
                                        for i in range(startPos, endPos):
                                            # print (i)
                                            templist = ftPeaks[i].strip().split(",")
                                            #print(hmtemp)
                                            if not (templist.__contains__(hmtemp)):
                                                peaks[i] += 1
                                                ftPeaks[i] = ftPeaks[i] + hmtemp + ","

                    f.close()

    #print(filecount)
    totalPeaks = 0
    for i in range(0, 15):
        #print("W" + (1+i).__str__() + "\t" + peaks[i].__str__() + "\t" + ftPeaks[i])
        Etp = EntropyCalc(peaks[i],features.__len__())

        chrStat.write((int(minPos) + (i*int(WindowSize))).__str__() + "\t" + peaks[i].__str__() +"\t"+ Etp.__str__()+"\t" + ftPeaks[i]+"\n")
        #chrStat.write("W" + (i+1).__str__() + "\t" + peaks[i].__str__() + "\t" + ftPeaks[i] + "Entropy: \t" + Etp.__str__() +"\n")

    chrStat.close()

def findCommonfeatures(Odir):
    '''
     a function to go through 2 different folders in the directory, find the list of the features (transcription factors, histon modifications ...etc)
     and print out to 3 different files in each sub directory:   1. a ful list of all different features
                                                                 2. a list of common features between the stages
                                                                 3. a list of the unique features that exist in one but not the other stage (removed)

    :param Odir: original directory that contains the 2 stages data (modEncode files, uncompressed) in different folders
    :return:
    '''
    originalDir = Odir
    #listing all sub directories in folder
    entries = os.listdir(originalDir)

    allFeaturesMatrix = []
    allFeatureFolders = []
    for DirFolder in entries:
        file = open(originalDir + "/"+DirFolder + "/fullFeaturesList.txt", "w")
        allFeatureFolders.append(DirFolder)
        allFeatures = []
        SubEntries = os.listdir(originalDir+'/'+DirFolder)
        for subDir in SubEntries:
            if subDir.startswith("modEncode"):
                newDir = originalDir +'/'+DirFolder+ '/'+ subDir + "/interpreted_data_files/"
                subEnt = os.listdir(newDir)
                checked = False
                for folder in subEnt:
                    if not checked:
                        # print("In dir :" + folder.__str__())
                        if not (folder.endswith(".gz")):
                            lineParts = folder.split("_")
                            checked = True
                            tempTF = ''.join(e for e in lineParts[2] if e.isalnum())
                            tempTF = tempTF.upper()
                            if not allFeatures.__contains__(tempTF):
                                allFeatures.append(tempTF)

        file.write("features Count:" + allFeatures.__len__().__str__() + "\n")
        allFeatures.sort()
        for i in range(0, allFeatures.__len__()):
            file.write(allFeatures[i] + "\n")
        file.close()
        allFeaturesMatrix.append(allFeatures)


    # finding common and unique features of both categories
    fileC = open(originalDir +"/" +allFeatureFolders[0] + "/commonFeaturesList.txt", "w")
    #fileU = open(originalDir +"/" + allFeatureFolders[0] + "/uniqueFeaturesList.txt", "w")
    common =[]
    #unique = []
    for i in range (0, allFeaturesMatrix[0].__len__()):
        if allFeaturesMatrix[1].__contains__(allFeaturesMatrix[0][i]):
            common.append(allFeaturesMatrix[0][i])
        #else:
            #unique.append(allFeaturesMatrix[0][i])
    fileC.write("features Count:" + common.__len__().__str__() + "\n")
    common.sort()
    for i in range(0, common.__len__()):
        fileC.write(common[i].__str__() + "\n")
    fileC.close()

    #fileU.write("features Count:" + unique.__len__().__str__() + "\n")
    #unique.sort()
    #for i in range(0, unique.__len__()):
    #    fileU.write(unique[i] + "\n")
    #fileU.close()

    fileC = open(originalDir +"/" + allFeatureFolders[1] + "/commonFeaturesList.txt", "w")
    #fileU = open(originalDir + "/" +allFeatureFolders[1] + "/uniqueFeaturesList.txt", "w")
    common = []
    #unique = []
    for i in range(0, allFeaturesMatrix[1].__len__()):
        if allFeaturesMatrix[0].__contains__(allFeaturesMatrix[1][i]):
            common.append(allFeaturesMatrix[1][i])
    #    else:
    #        unique.append(allFeaturesMatrix[1][i])
    fileC.write("features Count:" + common.__len__().__str__() + "\n")
    common.sort()
    for i in range(0, common.__len__()):
        fileC.write(common[i].__str__() + "\n")
    fileC.close()

    #fileU.write("features Count:" + unique.__len__().__str__() + "\n")
    #unique.sort()
    #for i in range(0, unique.__len__()):
    #    fileU.write(unique[i] + "\n")
    #fileU.close()

def maxDomainWithNoGaps(inputFile, outputFile, threshold=0.75):

    ifile = inputFile
    ofile = outputFile

    file = open(ifile, 'r')
    result = open(ofile, 'w')

    header = file.readline()
    temp = file.readline()

    result.write(header)
    result.write(temp)
    hparts = header.strip().split()
    temp = file.readline()

    thresholdFeatures = float(hparts[9]) * float(threshold)
    #print("thrishold = " + threshold.__str__() + "*" + hparts[9] + " = " + thresholdFeatures.__str__())

    maxNoGapList = []
    maxLenNoGapDomain = Domain()
    maxHeightNoGapDomain = Domain()
    line = file.readline()
    while (line != ''):
        lparts = line.strip().split()
        if (float (lparts[1]) >= thresholdFeatures):
            StartPos = lparts[0]
            domainList = []
            domainListEntropy =[]
            domainListFeats = []
            Alist = []
            while (float (lparts[1]) >= thresholdFeatures):
                domainList.append(float(lparts[1]))
                domainListEntropy.append(float(lparts[2]))
                domainListFeats.append(lparts[3][0:lparts[3].__len__()-1])
                aparts = lparts[4].split(",")
                aparts = aparts[0:aparts.__len__() - 1]
                for a in aparts:
                    if not Alist.__contains__(a):
                        Alist.append(a)
                line = file.readline()
                if(line == ''):
                    break
                else:
                    lparts = line.strip().split()

            if (int (domainList.__len__()) > int ( maxLenNoGapDomain.getSize())):
                maxLenNoGapDomain.setDomain(StartPos, domainListEntropy.__len__(), domainListEntropy,domainListFeats,Alist)
            tempDomain = Domain(StartPos,domainList.__len__(),domainListEntropy,domainList,domainListFeats,Alist)
            maxNoGapList.append(tempDomain)

            Evalue = 0
            for e in domainListEntropy:
                Evalue = Evalue + e

            if (Evalue > float ( maxHeightNoGapDomain.getEvalue())):
                maxHeightNoGapDomain.setDomain(StartPos, domainListEntropy.__len__(), domainListEntropy,domainListFeats,Alist)

        else:
            line = file.readline()

    maxNoGapList.sort(key=lambda x: x.size, reverse=True)

    nparts = inputFile.split(".")
    statsFile = open(nparts[0]+"Stats_."+nparts[1], "a")
    features = nparts[0].split("_")[1].split(":")[1]
    statsFile.write(threshold.__str__() + "\t")
    statsFile.write(hparts[9] + "\t")
    statsFile.write( maxNoGapList.__len__().__str__() + "\n")
    statsFile.close()
    result.write("Total Number of Domains = " + maxNoGapList.__len__().__str__()+"\n")
    result.write("StartPosition \t DomainSize(inWindows) \t [classSize|ClassCombinations] \t FeatureAnnotations \n")
    for i in range (0, maxNoGapList.__len__()):
        #print("StartPosition: " + maxNoGapList[i].getStartPos().__str__() + "\t Size: " + maxNoGapList[i].getSize().__str__() + "\n" )
        #strCombs = FeatureGroupsFinderForDomains(maxNoGapList[i].getfeats())


        listA = maxNoGapList[i].getAnno()
        result.write(maxNoGapList[i].getStartPos().__str__() + "\t" + maxNoGapList[i].getSize().__str__() +"\t"+ maxNoGapList[i].getfeats().__str__()+"\t"+ maxNoGapList[i].getAnnoStr()+"\n")
        #result.write(maxNoGapList[i].getStartPos().__str__() + "\t" + maxNoGapList[i].getSize().__str__() +"\t"+ strCombs+"\t"+ maxNoGapList[i].getAnnoStr()+"\n")
        #result.write(maxNoGapList[i].getStartPos().__str__() + "\t" + maxNoGapList[i].getSize().__str__() +"\t" +maxNoGapList[i].getFlist().__str__()+"\t"+ strCombs+"\n")


    file.close()
    result.close()

def MainFunc(Odir = "/home/boudela/mountboudela/HisMod/", Targets =["C", "A"], Chrm = "I" , DomainSize = 3000, WindowSize = 200, threshold = 0.0):
    findCommonfeatures(Odir)
    targetFeaturesList = ["A", "C"]

    subDir = os.listdir(Odir)
    # to go over the 2 sub directories, in every level
    for folder in subDir:
        newDir = Odir+folder+"/"
        for t in targetFeaturesList:
            if Targets.__contains__(t.lower()) or Targets.__contains__(t) or Targets.__len__()==0 :

                dirList = []
                chrfile = newDir + "chr:" + Chrm.upper() + "_targetFeatures:" + t + '_Listed'
                dirList.append(chrfile)
                chrfile +='.txt'

                features = featuresReader(newDir, t)
                '''
                fileChr = open(chrfile, "w")
                header = "Chr: " + Chrm + "\t WindowSize: " + WindowSize.__str__() + "
                header += "\t FeaturesTargeted: " + t + "\t FeaturesCount: " + features.__len__().__str__() + "\n"
                fileChr.write(header)
                fileChr.write("--------------------------------------------------------------------------\n")
                fileChr.write("StartPos \t FeaturesCount \t    Entropy\t  FeaturesList\n")
                fileChr.close()
                chrmSizes = (newDir + 'chrLen.txt')
                with open(chrmSizes)as chmFile:
                    for line in chmFile:
                        Lparts = line.strip().split()
                        chrmNum = Lparts[0]
                        chrmLen = int(Lparts[1])

                        startDomainPos = 0
                        if (chrmNum.upper() == Chrm.upper() or Chrm.upper() == "ALL"):
                            while (startDomainPos < chrmLen) and ((startDomainPos + DomainSize) <= int(chrmLen)):
                                peakFinder(newDir,features, chrmNum.upper(), startDomainPos,DomainSize,WindowSize,t)
                                startDomainPos += DomainSize


                chmFile.close()
                #==============================================
                '''
                FeatureGroupsFinder(chrfile,(chrfile.split(".")[0]+"Groups.txt"))
                for dirName in dirList:
                    inputfile = dirName + '.txt'
                    thresholds = [0.650,0.7,0.750]
                    nparts = inputfile.split(".")
                    statsFile = open(nparts[0] + "Stats_." + nparts[1], "w")
                    statsFile.write("Threshold \t FeatureCount \t DomainsCount \n")
                    statsFile.close()
                    for thr in thresholds:
                        dparts = dirName.split("_")
                        outputfile = dparts[0] + dparts[1] + "_MaxDomAno_" + thr.__str__()+".txt"
                        maxDomainWithNoGaps( newDir + "chr:I_targetFeatures:C_ListedWithAnnotation.txt", outputfile,thr)
        #print("Done: " + folder.__str__())


MainFunc()