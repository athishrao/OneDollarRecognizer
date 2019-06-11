import OneDollar
import ModifiedOneDollar
import random
import matplotlib
import time
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

def recognize(Xcoord, Ycoord):
    Candidate = candidate(Xcoord, Ycoord)
    symbols = ["triangle", "x", "rectangle", "circle", "check", "caret", "question_mark", "arrow", "left_sq_bracket", "right_sq_bracket", "v", "delete_mark", "left_curly_brace", "right_curly_brace", "star", "pigtail"]
    symbolList = list()
    for i in symbols:
        symbolList.append(symbol(i))
    # random.shuffle(symbolList)
    start = time.time()
    Final = Total(symbolList)
    end = time.time()
    print("Time elapsed: ", end - start)
    string = Final.recognize(Candidate)
    return string

def candidate(Xcoord, Ycoord):
    candidate = list()
    for i in range(len(Xcoord)):
        candidate.append(OneDollar.points(Xcoord[i], Ycoord[i]))
    candidate = OneDollar.stroke(pointsList=candidate)
    candidate.length = len(Xcoord)
    candidate.resample(32)
    candidate.rotToZero()
    candidate.scaleToSquare(100)
    candidate.translateToZero()
    return candidate

class Total:
    totalList = list()
    def __init__(self, symbolList):
        for i in symbolList:
            i.resample(32)
            self.totalList.append(i.strokeList[:])
    def getTrainingSet(self):
        traningSet = list()
        for i in range(len(self.totalList)):
            for k in ((self.totalList[i])):
                traningSet.append(k)
        return traningSet
    def recognize(self, candidate):
        templateList = self.getTrainingSet()
        K, score, j = candidate.recognize(templateList)
        print("The predicted shape is: ", K.name)
        print("The score is: ", score)
        return K.name, score

class symbol:
    strokeList = list()
    length = 10
    speed = ["fast", "medium", "slow"]
    def __init__(self, name):
        self.name = name
        self.strokeList = list()
        for i in range(1,self.length):
            filename = "./xmlFiles/"+str(self.name)+"0"+str(i)+".xml"
            self.strokeList.append(OneDollar.stroke(name, filename, False))
        filename = "./xmlFiles/"+str(self.name)+"10"+".xml"
        self.strokeList.append(OneDollar.stroke(name, filename, False))

    def resample(self, n):
        for i in range(len(self.strokeList)):
            # print("Resampling %s%d"%(self.strokeList[i].name,i))
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



    