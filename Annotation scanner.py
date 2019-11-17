import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#colors = ["red", "black", "blue","yellow", "magenta", "green","cyan"]
colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:brown","tab:pink","tab:gray","tab:olive","tab:cyan"]
Annotations = ['gene', 'transcript', 'exon', 'five_prime_utr', 'CDS', 'start_codon', 'stop_codon', 'three_prime_utr']


class Group:
    fts = []
    counter = 0

    def __init__(self,s ,c ):
        self.fts = s
        self.counter = c
    def getFts(self):
        return self.fts
    def getCount(self):
        return self.counter
    def isSameFts(self, fs):
        #print("s-------------")
        #print(self.fts)
        #print(fs)
        #print("f-------------")
        if self.fts.__len__() != fs.__len__():
            #print("Wrong")
            return False
        for f in fs:
            if not self.fts.__contains__(f):
                #print(" checking: " + self.fts.__str__() + "\t and "+ fs.__str__())
                #print("Wrong")
                return False
        #print("True")
        return True

class GroupList:
    size = 0
    list = []

    def __init__(self, s):
        self.size = s
        self.list=[]

    def addGroup(self, gp):
        if self.list.__len__() < self.size:
            self.list.append(gp)
            self.list.sort(key=lambda x: x.counter, reverse=True)
        elif gp.getCount() > self.list[self.list.__len__()-1].getCount() :
            self.list.pop()
            self.list.append(gp)
            self.list.sort(key=lambda x: x.counter, reverse=True)



    def getList(self):
        return self.list
    def getAllLists(self):
        ftsL = []
        cList = []
        for l in self.list:
            ftsL.append(l.getFts())
            cList.append(l.getCount())
        return ftsL, cList

    def IsInList(self, grp):
        for l in self.list:
            if l.isSameFts(grp.getFts()):
                return True
        return False
    def SortByLen(self):
        self.list.sort(key=lambda x: x.fts.__len__(), reverse=True)

class GroupWithAnno:
    fts = []
    repeat = 0
    anCounts = []

    def __init__(self, f,r):
        self.fts = f
        self.repeat = r
        self.anCounts = [0,0,0,0,0,0,0,0]

    def isSubGroupOf(self, grp):
        if len(grp)< self.fts.__len__():
            return False
        for f in self.fts:
            if not grp.__contains__(f):
                return False
        return True

    def addAnno(self, a):
        if (a!= "") and (a!= "-"):
            if Annotations.__contains__(a) :
                ind = Annotations.index(a)
                self.anCounts[ind] +=1
            else:
                print("Error! not an annotation ft" + a)

    def getAnnosCounts(self):
        return self.anCounts
    def getCount(self):
        return self.repeat
    def getFts(self):
        return self.fts


class Feature:
    type = ""
    startPos = 0
    endPos = 0

    def __init__(self, t, sp, ep):
        self.type = t
        self.startPos = sp
        self.endPos = ep
    def getFeatStr(self):
        return (self.type + "\t" + self.startPos.__str__() + "\t" + self.endPos.__str__())
    def getStartPos(self):
        return self.startPos
    def getEndPos(self):
        return self.endPos
    def getType(self):
        return self.type
    def isInTheDomain(self, sp, ep):
        if (self.startPos <= sp and self.endPos >= sp) or (self.startPos <= ep and self.endPos >= sp):
            return True
        else:
            return False

class FeatListPerWindow:
    startPos = 0
    WS = 200
    feats = []
    ftCount = 0
    entropy = 0
    fts = ""

    def __init__(self, startp , ws , ftC,e,ftstr):
        self.startPos = startp
        self.WS = ws
        self.feats.append(t)

    def AddFeat(self,f):
        self.feats.append(f)
    def isInTheDomain(self, sp, ep):
        if (self.startPos <= sp and (self.startPos+self.WS) >= sp) or ((self.startPos <= ep and (self.startPos+self.WS) >= sp)):
            return True
        else:
            return False

def ChromosomeSpecAnno(chr = "I"):

    featList = []

    annoFile = open("/home/boudela/mountboudela/annotation/Caenorhabditis_elegans.WBcel235.98.gtf","r")
    ChrIfile = open("/home/boudela/mountboudela/annotation/Caenorhabditis_elegans.WBcel235.chrI.txt","w")

    counter = 0
    counterAll =0
    line = annoFile.readline()
    while line != "":
        lparts = line.strip().split()
        if lparts[0] == chr:
            tempFeat = Feature(lparts[2], int(lparts[3]), int(lparts[4]))
            featList.append(tempFeat)
            #ChrIfile.write(lparts[2] + "\t" + lparts[3] + "\t" + lparts[4] + "\n")
            counter += 1
        line = annoFile.readline()
        counterAll+=1

    featList.sort(key=lambda x: x.startPos, reverse=False)

    for f in featList:
        ChrIfile.write(f.getFeatStr() + "\n")
    ChrIfile.close()
    annoFile.close()
    return featList

def loadAnno():
    featList = []

    annoFile = open("/home/boudela/mountboudela/annotation/Caenorhabditis_elegans.WBcel235.chrI.txt", "r")

    line = annoFile.readline()
    while line != "":
        lparts = line.strip().split()
        tempFeat = Feature(lparts[0], int(lparts[1]), int(lparts[2]))
        featList.append(tempFeat)
        line = annoFile.readline()

    featList.sort(key=lambda x: x.startPos, reverse=False)

    annoFile.close()
    return featList

def Main(chrFileName = "/home/boudela/mountboudela/HisMod/L3/chr:I_targetFeatures:C_Listed.txt"):

    #annoList = ChromosomeSpecAnno("I")
    annoList = loadAnno()
    output = open("/home/boudela/mountboudela/HisMod/L3/chr:I_targetFeatures:C_ListedWithAnnotation.txt","w")
    found = 0
    input = open(chrFileName,"r")
    header = input.readline()
    headerParts = header.strip().split()
    output.write(header)
    WS = int(headerParts[3])
    temp = input.readline()
    output.write(temp)
    temp = input.readline()
    tempParts = temp.strip().split()
    output.write(tempParts[0]+ "\t" +tempParts[1]+ "\t" +tempParts[2]+ "\t"+tempParts[3] +"\t" +"AnnotationFeature"+ "\n")
    temp = input.readline()

    i = 0
    while temp != "":

        tempParts = temp.strip().split()
        startP = int(tempParts[0])
        if tempParts.__len__() < 4:
            tempParts.append("-")

        if (startP+WS) < annoList[i].getStartPos():
            output.write(tempParts[0] + "\t" + tempParts[1] + "\t" + tempParts[2]  + "\t" + tempParts[3] + "\t" + "-"+ "\n")

        else:
            feats = ""
            while annoList[i].getEndPos() < startP:
                i+=1
            for j in range(i, annoList.__len__()):
                if annoList[j].isInTheDomain(startP, (startP+WS)):
                    feats += annoList[j].getType() +","
                    found+=1
                elif annoList[j].getStartPos() > (startP+WS):
                    break

            if feats == "":
                feats = "-"
            output.write(tempParts[0] + "\t" + tempParts[1] + "\t" + tempParts[2]  + "\t" + tempParts[3] + "\t" + feats+ "\n")

        temp = input.readline()
    '''
    print("tfs found = " + found.__str__())
    print("last pos in list = " + annoList[annoList.__len__()-1].getEndPos().__str__())
    print("list len = " +annoList.__len__().__str__())
    print(i)
    for j in range (i, annoList.__len__()):
        print(annoList[j].getFeatStr())
    '''

    output.close()

def annoPlotterofOneDomain():

    AnnoFile = open("/home/boudela/mountboudela/HisMod/Emb/chr:I_targetFeatures:C_ListedWithAnnotation.txt", "r")
    DomainFile = open ("/home/boudela/mountboudela/HisMod/Emb/chr:ItargetFeatures:C_MaxDomainLNoGaps_0.65.txt","r")

    positionsList = []
    featsList = []
    annoList = []

    header = DomainFile.readline()
    headerParts = header.strip().split()
    WS = int(headerParts[3])
    totalFeatCount = int(headerParts[9])
    temp = DomainFile.readline()
    temp = DomainFile.readline()
    temp = DomainFile.readline()

    temp = DomainFile.readline()
    tempParts = temp.strip().split()
    SP = int(tempParts[0])
    DS = int(tempParts[1])


    DomainFile.close()

    header = AnnoFile.readline()
    header = AnnoFile.readline()
    header = AnnoFile.readline()

    header = AnnoFile.readline()
    found = False
    while (header != "" and (not found)):
        hp = header.strip().split()
        positionsList.append(int(hp[0]))
        annoList.append(hp[3])
        featsList.append(hp[4])
        if int(hp[0]) == SP:
            for i in range (0, DS+4): # to keep 5 windows after domain
                header = AnnoFile.readline()
                hp = header.strip().split()
                positionsList.append(int(hp[0]))
                annoList.append(hp[3])
                featsList.append(hp[4])

            found = True
        else:
            # to keep 5 windows before domain
            if positionsList.__len__()>5:
                positionsList.remove(positionsList[0])
                annoList.remove(annoList[0])
                featsList.remove(featsList[0])

        header = AnnoFile.readline()
    AnnoFile.close()



    featsListCounts = []
    for i in range(0, featsList.__len__()):
        featsListCounts.append(len(featsList[i].split(",")) - 1)
        #print(i.__str__() +".\t" + positionsList[i].__str__() + "\t" + featsListCounts[i].__str__() + "\t"+ featsList[i].__str__() + "\t"+ annoList[i].__str__() )

    annoNames = []
    annoPos = []
    for i in range(0, annoList.__len__()):
        parts = annoList[i].split(",")
        parts = parts[0: parts.__len__()-1]
        for f in parts:
            if annoNames.__contains__(f):
                index = annoNames.index(f)
                if not annoPos[index].__contains__(positionsList[i]):
                    annoPos[index].append(positionsList[i])
            else:
                annoNames.append(f)
                annoPos.append([positionsList[i]])
    print(annoNames)
    print(annoPos)

    plt.figure()
    plt.plot(positionsList, featsListCounts, color=colors[0], label="Histone Modifications Count")
    plt.title("Max Domain found in -chr I-, VS number of (common)histone modifications in Embryos")
    plt.xlabel("positions in chrm I")
    plt.ylabel("Histone modifiations count")
    c = 1
    for i in range(0, annoNames.__len__()):
        y = [c for i in range(annoPos[i].__len__())]
        plt.plot(annoPos[i], y, color=colors[c], label=annoNames[i])
        c += 1
    plt.legend()
    plt.show()
    plt.close()

def AnnotationVSDomain(fileName = "/home/boudela/mountboudela/HisMod/L3/chr:ItargetFeatures:C_MaxDomAno_0.65.txt", fileName2 = "/home/boudela/mountboudela/HisMod/Emb/chr:ItargetFeatures:C_MaxDomAno_0.65.txt"):

    DomainFile = open (fileName,"r")
    threshold = fileName.split("_")[2]
    threshold = threshold.split(".txt")[0]
    stage = fileName.split("/")[5]

    DomainFile2 = open(fileName2, "r")
    threshold2 = fileName2.split("_")[2]
    threshold2 = threshold2.split(".txt")[0]
    stage2 = fileName2.split("/")[5]
    if threshold != threshold2:
        print("Error! files dont match in thresholds!!")
        return

    featsList = []
    featCountList = []
    featCountList2 = []
    counter = 0

    header = DomainFile.readline()
    #headerParts = header.strip().split()
    #WS = int(headerParts[3])
    #totalFeatCount = int(headerParts[9])
    temp = DomainFile.readline()
    temp = DomainFile.readline()
    DomainsCount = int(temp.strip().split("=")[1])
    temp = DomainFile.readline()

    temp = DomainFile.readline()
    while(temp != ""):
        tempParts = temp.strip().split()
        fts = tempParts[tempParts.__len__()-1].split(",")
        fts = fts[0:fts.__len__()-1]
        for f in fts:
            if featsList.__contains__(f):
                index = featsList.index(f)
                featCountList[index] += 1
            else:
                featsList.append(f)
                featCountList.append(1)
                featCountList2.append(0)
        temp = DomainFile.readline()

    DomainFile.close()

    header = DomainFile2.readline()
    # headerParts = header2.strip().split()
    # WS = int(headerParts[3])
    # totalFeatCount = int(headerParts[9])
    temp = DomainFile2.readline()
    temp = DomainFile2.readline()
    DomainsCount2 = int(temp.strip().split("=")[1])
    temp = DomainFile2.readline()

    temp = DomainFile2.readline()
    while (temp != ""):
        tempParts = temp.strip().split()
        fts = tempParts[tempParts.__len__()-1].split(",")
        fts = fts[0:fts.__len__() - 1]
        for f in fts:
            if featsList.__contains__(f):
                index = featsList.index(f)
                featCountList2[index] += 1
            else:
                featsList.append(f)
                featCountList2.append(1)
        temp = DomainFile2.readline()

    #print(featsList)
    #print(featCountList)
    #print(featCountList2)

    DomainFile2.close()



    ind = np.arange(len(featsList))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width / 2, featCountList, width,label=stage)
    rects2 = ax.bar(ind + width / 2, featCountList2, width,label=stage2)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Annotation features occurrences')
    plt.xlabel('Annotation features ')
    ax.set_title('Annotation features VS their occurrences in domains of ' + threshold + ' threshold in C-elegans')
    ax.set_xticks(ind)
    ax.set_xticklabels(featsList)
    ax.legend()

    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                        textcoords="offset points",  # in both directions
                        ha=ha[xpos], va='bottom')

    autolabel(rects1, "left")
    autolabel(rects2, "right")

    fig.tight_layout()

    plt.show()


    '''
    y_pos = np.arange(len(featsList))
    plt.bar(y_pos, featCountList, align='center', alpha=0.5)
    plt.xticks(y_pos, featsList)
    plt.ylabel('Annotation features occurrences')
    plt.xlabel('Annotation features ')
    plt.title('Annotation features VS their occurrences in ' + DomainsCount.__str__() + ' domains of ' +threshold + ' threshold in ' + stage )

    plt.show()
    '''

def AnnotationVSClasses(fileName = "/home/boudela/mountboudela/HisMod/Emb/chr:I_targetFeatures:C_ListedGroups.txt", fileName2 = "/home/boudela/mountboudela/HisMod/L3/chr:I_targetFeatures:C_ListedGroups.txt"):
    f1 = "/home/boudela/mountboudela/HisMod/Emb/chr:ItargetFeatures:C_MaxDomAno_0.65.txt"
    f2 = "/home/boudela/mountboudela/HisMod/L3/chr:ItargetFeatures:C_MaxDomAno_0.65.txt"
    dfile = open(f1,"r")
    dfile2 = open(f2,"r")
    threshold = f1.split("_")[2]
    threshold = threshold.split(".txt")[0]

    groupSize = 3
    Glist = GroupList(groupSize)
    DomainFile = open (fileName,"r")
    stage = fileName.split("/")[5]

    temp = DomainFile.readline()
    temp = DomainFile.readline()
    temp = DomainFile.readline()

    temp = DomainFile.readline()
    while temp !="":
        tparts = temp.strip().split()
        counter = int(tparts[1])
        for i in range(0, counter):
            line = DomainFile.readline()
            GroupCount = int(line.strip().split()[0])
            Groupfts = line.strip().split()[1]
            Groupfts = Groupfts.split(",")
            Groupfts = Groupfts[0:Groupfts.__len__()]
            tempG = Group(Groupfts, GroupCount)
            Glist.addGroup(tempG)

        temp = DomainFile.readline()

    DomainFile.close()

    repGroups1 = []
    lst = Glist.getList()
    for l in lst:
        print(l.getCount().__str__()+ " " +l.getFts().__str__())
        tempObj = GroupWithAnno( l.getFts(), l.getCount())
        repGroups1.append(tempObj)
    print("+++++++++++++++++++++++++++++++++++++++++++++++")

    Glist2 = GroupList(groupSize)
    DomainFile2 = open(fileName2, "r")
    stage2 = fileName2.split("/")[5]
    temp = DomainFile2.readline()
    temp = DomainFile2.readline()
    temp = DomainFile2.readline()

    temp = DomainFile2.readline()
    while temp != "":
        tparts = temp.strip().split()
        counter = int(tparts[1])
        for i in range(0, counter):
            line = DomainFile2.readline()
            GroupCount = int(line.strip().split()[0])
            Groupfts = line.strip().split()[1]
            Groupfts = Groupfts.split(",")
            tempG2 = Group(Groupfts, GroupCount)
            Glist2.addGroup(tempG2)

        temp = DomainFile2.readline()

    repGroups2 = []
    DomainFile2.close()
    lst2 = Glist2.getList()
    for l in lst2:
        #print("checking if : " + l.getFts().__str__() + "  is in list: " + lst2.__str__())
        if Glist.IsInList(l):
            print(l.getCount().__str__() + " *** " + l.getFts().__str__())
        else:
            print(l.getCount().__str__() + " --- " + l.getFts().__str__())
        tempObj = GroupWithAnno( l.getFts() , l.getCount())
        repGroups2.append(tempObj)
    print("========================")

    line = dfile.readline()
    line = dfile.readline()
    line = dfile.readline()
    line = dfile.readline()

    line = dfile.readline()
    while(line!=""):
        lparts = line.strip().split()
        SP = lparts[0]
        DS = lparts[1]
        FTS = lparts[2:lparts.__len__() - 1].__str__()
        Anos = lparts[lparts.__len__()-1].split(",")
        FTS = FTS.split("\", \"")
        for i in range(0, FTS.__len__()):
            FTS[i] = FTS[i].replace("[", "")
            FTS[i] = FTS[i].replace("]", "")
            FTS[i] = FTS[i].replace("\'", "")
            FTS[i] = FTS[i].replace("\"", "")

            tempFts = FTS[i].split(",")
            if tempFts[tempFts.__len__()-1] == "":
                tempFts = tempFts[0:tempFts.__len__()-1]
                for j in range (0, repGroups1.__len__()):
                    if repGroups1[j].isSubGroupOf(tempFts):
                        for k in range (0,Anos.__len__()):
                            repGroups1[j].addAnno(Anos[k])

        line = dfile.readline()
    dfile.close()

    '''
    for rg in repGroups1:
        print(rg.getFts())
        print(rg.getCount())
        print(rg.getAnnosCounts())
        print("------------------")
    '''


    line2 = dfile2.readline()
    line2 = dfile2.readline()
    line2 = dfile2.readline()
    line2 = dfile2.readline()

    line2 = dfile2.readline()
    while (line2 != ""):
        lparts = line2.strip().split()
        SP = lparts[0]
        DS = lparts[1]
        FTS = lparts[2:lparts.__len__() - 1].__str__()
        Anos = lparts[lparts.__len__() - 1].split(",")
        FTS = FTS.split("\", \"")
        for i in range(0, FTS.__len__()):
            FTS[i] = FTS[i].replace("[", "")
            FTS[i] = FTS[i].replace("]", "")
            FTS[i] = FTS[i].replace("\'", "")
            FTS[i] = FTS[i].replace("\"", "")

            tempFts = FTS[i].split(",")
            if tempFts[tempFts.__len__() - 1] == "":
                tempFts = tempFts[0:tempFts.__len__() - 1]
                for j in range(0, repGroups1.__len__()):
                    if repGroups2[j].isSubGroupOf(tempFts):
                        for k in range(0, Anos.__len__()):
                            repGroups2[j].addAnno(Anos[k])

        line2 = dfile2.readline()


    for rg in repGroups1:
        print(rg.getFts())
        print(rg.getCount())
        print(rg.getAnnosCounts())
        print("------------------")
    print(repGroups2[0].getAnnosCounts())
    print(repGroups2[1].getAnnosCounts())
    print(repGroups2[2].getAnnosCounts())

    ind = np.arange(len(Annotations))  # the x locations for the groups
    width = 0.250  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - 4*width / 6, repGroups2[0].getAnnosCounts(), width, label=repGroups2[0].getFts().__str__())
    rects2 = ax.bar(ind + 2*width / 6, repGroups2[1].getAnnosCounts(), width, label=repGroups2[1].getFts().__str__())
    rects3 = ax.bar(ind + 8*width / 6, repGroups2[2].getAnnosCounts(), width, label=repGroups2[2].getFts().__str__())

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Histone modifications occurrences in different annotation features')
    plt.xlabel('Annotation features ')
    ax.set_title('Most common histone modifications in '+ threshold + ' domains of C-elegance(' + stage2+') VS Annotation features ')
    ax.set_xticks(ind)
    ax.set_xticklabels(Annotations)
    ax.legend()

    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                        textcoords="offset points",  # in both directions
                        ha=ha[xpos], va='bottom')

    autolabel(rects1, "left")
    autolabel(rects2, "center")
    autolabel(rects3, "right")

    fig.tight_layout()

    plt.show()


#Main()
#annoPlotterofOneDomain()
#AnnotationVSDomain()
AnnotationVSClasses()
