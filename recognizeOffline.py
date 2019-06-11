import OneDollar
import random
import time
import csv

class log:
    userName, gestureType, E, sizeOfTraningSample, trainingContents, candidate, predicted, isCorrect, bestMatch, kBest = "", "", "", "", "", "", "", "", "", ""
    def __init__(self, userName, gestureType, E, sizeOfTraningSample, trainingContents, candidate, predicted, isCorrect, bestMatch, kBest):
        self.userName, self.gestureType, self.E, self.sizeOfTraningSample, self.trainingContents, self.candidate, self.predicted, self.isCorrect, self.bestMatch, self.kBest = userName, gestureType, E, sizeOfTraningSample, trainingContents, candidate, predicted, isCorrect, bestMatch, kBest
    
    def printLog(self):
        with open("log.csv", "a+") as csv_file:
            csv_file.write("%s, %s, %s, %s, %s, %s, %s, %s, \"%s\"\n" % (self.userName, self.gestureType, self.E, self.sizeOfTraningSample, self.candidate, self.predicted, self.isCorrect, self.bestMatch, self.kBest))


class Total:
    totalList = list()
    def __init__(self, symbolList):
        for i in symbolList:
            i.resample(32)
            self.totalList.extend(i.strokeList[:])
        self.totalList.sort()

    def printTotalStrokes(self):
        print("Tot Size: ", len(self.totalList))
        for i in self.totalList:
            print(i.name)

    def recognize(self):
        templateList, candidateList, userList = list(), list(), list()
        userAccNum, userAccDen = 0, 0
        counter, total, userCounter = 0, 0, 0
        trainer = self.totalList
        tempList = list()
        for i in range(len(trainer)):
            if (i==0):
                1==1
            elif (i % 160 == 0):
                userList.append(tempList)
                tempList = []
                tempList.append(trainer[i])
            else:
                tempList.append(trainer[i])
        # userName, gestureType, E, sizeOfTraningSample, trainingContents, candidate, predicted, isCorrect, bestMatch, kBest
        for i in userList:
            userCounter += 1
            for E in range(1,10):
                print("E: ", E)
                total, counter = 0, 0
                start = time.time()
                for _ in range(100):
                    # print("i: ", _)
                    templateList, candidateList = [], []
                    for j in range(16):
                        trainIndex, testIndex = self.chooseTestTrain(j, E+1)
                        templateList.extend([trainer[k] for k in trainIndex])
                        candidateList.append(trainer[testIndex])
                    
                    for candidate in candidateList:
                        total += 1
                        userAccDen += 1
                        # start1 = time.time()
                        # print("Len: ", len(templateList))
                        K, score, nBestList = candidate.recognize(templateList)
                        # end1 = time.time()
                        # print("Time candidate elapsed: ", end1-start1)
                        predicted = K.name[3:-2]
                        actual = candidate.name[3:-2]
                        # print("Actual: %s, Predicted: %s" % (actual, predicted))
                        if (predicted == actual):
                            counter += 1
                            userAccNum += 1
                        templateListNames = [i.name[3:] for i in templateList]
                        currentLog = (log(userCounter, actual, E, len(templateList), templateListNames, candidate.name, predicted, (predicted==actual), K.name, nBestList))
                        currentLog.printLog()
                        
                end = time.time()
                print("Time elapsed: ", end-start)
                print("Accuracy: ", counter/total)
            print("Accuracy for User %d: %d" % (userCounter, userAccNum/userAccDen))
        # for i in logList:
        #     i.printLog()
        return
    
    def chooseTestTrain(self, i, num):
        listJump = 10
        randList = set()
        while(len(randList) != num):
            randList.add(random.randint(i*listJump, (i+1)*listJump - 1))
        randList = list(randList)
        return randList[1:], randList[0]
        

class symbol:
    strokeList = list()
    length = 10
    # speed = ["fast", "medium", "slow"]
    
    people = ["s01", "s02","s03","s04","s05","s06","s07","s08","s09","s10", "s11"]
    def __init__(self, name):
        speedVal = "fast"
        self.name = name
        self.strokeList = list()
        for person in self.people:
            # for speedVal in self.speed:
            for i in range(1,self.length):
                Fname = str(name)+"0"+str(i)
                filename = "."+"/xml_logs1/"+person+"/"+speedVal+"/"+ Fname +".xml"
                self.name = person+Fname
                self.strokeList.append(OneDollar.stroke(self.name, filename, False))
            Fname = str(name)+"10"
            filename = "."+"/xml_logs1/"+person+"/"+speedVal+"/"+Fname+".xml"
            self.name = person+Fname
            self.strokeList.append(OneDollar.stroke(self.name, filename, False))
            

    def resample(self, n):
        for i in range(len(self.strokeList)):
            self.strokeList[i].resample(n)
            self.strokeList[i].rotToZero()
            self.strokeList[i].scaleToSquare(100)
            self.strokeList[i].translateToZero()

    def printSymbol(self):
        # random.shuffle(self.strokeList)
        # newlist = sorted(self.strokeList, key=lambda x: x.name[1:3], reverse=True)
        for i in range(len(self.strokeList)):
            print(self.strokeList[i].name)
    
    def printResampledSymbol(self):
        for i in range(self.length):
            print("Number: ", i)
            self.strokeList[i].printResampledStroke()


symbols = ["triangle", "x", "rectangle", "circle", "check", "caret", "question_mark", "arrow", "left_sq_bracket", "right_sq_bracket", "v", "delete_mark", "left_curly_brace", "right_curly_brace", "star", "pigtail"]
symbolList = list()
for i in symbols:
    symbolList.append(symbol(i))
# for i in symbolList:
#     i.printSymbol()

Final = Total(symbolList)
# Final.printTotalStrokes()
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