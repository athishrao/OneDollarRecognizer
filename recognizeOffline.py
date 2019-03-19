import OneDollar
import random
import time


class Total:
    totalList = list()
    
    def __init__(self, symbolList):
        for i in symbolList:
            i.resample(32)
            self.totalList.append(i.strokeList[:])

    def getTrainingSet(self):
        traningSet, testingSet = list(), list()
        random.shuffle(self.totalList)
        for i in range(len(self.totalList)):
            if (i/5 != 0):
                for k in ((self.totalList[i])):
                    traningSet.append(k)
            else:
                for k in (self.totalList[i]):
                    testingSet.append(k)
        return traningSet, testingSet

    def getTrainingOnlySet(self):
        traningSet = list()
        for i in range(len(self.totalList)):
            for k in ((self.totalList[i])):
                traningSet.append(k)
        return traningSet

    def recognize(self):
        # templateList, candidateList = self.getTrainingSet()
        templateList, candidateList = list(), list()
        # print("len of template = %d candidate = %d" % (len(templateList), len(candidateList)))
        
        #     K, score = candidate.recognize(templateList)
            
        counter, total = 0, 0
        trainer = self.getTrainingOnlySet()
        # names = [(trainer[i].name, i) for i in range(len(self.getTrainingOnlySet()))]
        # print(names)
        for E in range(1,10):
            total, counter = 0, 0
            print("E = ", E)
            for _ in range(100):
                print("i = ", _)
                start = time.time()
                templateList, candidateList = [], []
                for i in range(16):
                    trainIndex, testIndex = self.chooseTestTrain(i, E+1)
                    templateList.extend([trainer[i] for i in trainIndex])
                    # print("Index: ", testIndex)
                    # print("candiate: ", trainer[testIndex].name)
                    candidateList.append(trainer[testIndex])
                end = time.time()
                # print("Looping through Candidates: ", end-start)
                start1 = time.time()
                # print("Length of CL: %d; Length of TL: %d" % (len(candidateList), len(templateList)))
                for candidate in candidateList:
                    total += 1
                    K, score = candidate.recognize(templateList)
                    # print("The predicted shape is: ", K.name)
                    # print("Actual shape is: ", candidate.name)
                    if (K.name == candidate.name):
                        counter += 1
                    # print("The score is: ", score)
                end1 = time.time()
                # print("Recognizing Candidate: ", end1-start1)
            print("Accuracy = ", counter/total)
        # print("Overall Accuracy = ", counter/total)
        return
    
    def chooseTestTrain(self, i, num):
        listJump = 330
        randList = set()
        while(len(randList) != num):
            randList.add(random.randint(i*listJump, (i+1)*listJump - 1))
        randList = list(randList)
        return randList[1:], randList[0]
        

class symbol:
    strokeList = list()
    length = 10
    speed = ["fast", "medium", "slow"]
    people = ["s01", "s02","s03","s04","s05","s06","s07","s08","s09","s10", "s11"]
    def __init__(self, name):
        self.name = name
        self.strokeList = list()
        for person in self.people:
            for speedVal in self.speed:
                for i in range(1,self.length):
                    filename = "."+"/xml_logs/"+person+"/"+speedVal+"/"+str(self.name)+"0"+str(i)+".xml"
                    self.strokeList.append(OneDollar.stroke(name, filename, False))
                filename = "."+"/xml_logs/"+person+"/"+speedVal+"/"+str(self.name)+"10"+".xml"
                self.strokeList.append(OneDollar.stroke(name, filename, False))
            

    def resample(self, n):
        for i in range(len(self.strokeList)):
            self.strokeList[i].resample(n)
            self.strokeList[i].rotToZero()
            self.strokeList[i].scaleToSquare(100)
            self.strokeList[i].translateToZero()

    def printSymbol(self):
        for i in range(self.length):
            print("Number: ", i)
            self.strokeList[i].printStroke()
    
    def printResampledSymbol(self):
        for i in range(self.length):
            print("Number: ", i)
            self.strokeList[i].printResampledStroke()


symbols = ["triangle", "x", "rectangle", "circle", "check", "caret", "question_mark", "arrow", "left_sq_bracket", "right_sq_bracket", "v", "delete_mark", "left_curly_brace", "right_curly_brace", "star", "pigtail"]
symbolList = list()
for i in symbols:
    symbolList.append(symbol(i))
Final = Total(symbolList)
Final.recognize()



# 0.89
# 0.92625
# 0.95125
# 0.968125
# 0.97625
# 0.976875
# 0.989375
# 0.988125
# 0.991875



# 0.8275
# 0.896875
# 0.93
# 0.941875
# 0.95375
# 0.9575
# 0.945625
# 0.955
# 0.959375