from xml.etree import ElementTree as ET
import math
import random
# Compute Euclidian Distance B/w any two Points Objects
def euclideanDist(pointA, pointB):
    return math.sqrt((pointA.x - pointB.x)**2 + (pointA.y - pointB.y)**2)

def l2Norm(vector):
    sumV = 0
    for i in vector:
        sumV += (i.distance())**2
    return  math.sqrt(sumV)

class points:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def distance(self):
        return math.sqrt((self.x)**2 + (self.y)**2)

class stroke:
    pointsList = list()
    resampledPointsList = list()
    differnceVector = list()
    length = 0
    name = ""
    nBestList = list()
    
    def __init__(self, name="candidate", pathname="na", candidate=True, pointsList = list()):
        if (candidate==False):
            self.name = name
            self.pointsList = list()
            self.resampledPointsList = list()
            tree = ET.parse(pathname)
            root = tree.getroot()
            for p in root.findall('.//Point'):
                self.pointsList.append(points(int(p.get('X')), int(p.get('Y'))))
                self.length += 1
        else:
            self.resampledPointsList = list()
            self.pointsList = pointsList
            self.nBestList = []
    
    def __lt__(self, other):
        # print("LT My: %s  Other: %s Result: %s" %(self.name, other.name, (self.name < other.name)))
        return self.name < other.name

    def __eq__(self, other):
        # print("EQ My: %s  Other: %s" %(self.name, other.name))
        return self.name == other.name

    def __sub__(self, strokeObject):
        tempList = list()
        for i in range(len(self.differnceVector)):
            tempList.append(points(self.differnceVector[i].x-strokeObject.differnceVector[i].x, self.differnceVector[i].y-strokeObject.differnceVector[i].y))
        return tempList

    def printStroke(self):
        for i in range(self.length):
            print(self.pointsList[i].x, self.pointsList[i].y)
    
    def printResampledStroke(self):
        for i in range(len(self.resampledPointsList)):
            print(self.resampledPointsList[i].x, self.resampledPointsList[i].y)
    
    # Compute the path length of a given stroke
    def pathlegth(self):
        distance = 0
        for i in range(1,self.length):
            distance += euclideanDist(self.pointsList[i-1], self.pointsList[i])
        return distance

    # Resample the given points
    def resample(self, n):
        # print("Stroke resample being called by: ", self.name)
        I = self.pathlegth()/(n - 1)
        D, i, counter = 0, 1, 1
        self.resampledPointsList = list()
        self.resampledPointsList.append(self.pointsList[0])
        while ((self.length > 0) and (i < len(self.pointsList))):
            d = euclideanDist(self.pointsList[i], self.pointsList[i-1])
            if (d+D >= I):
                counter += 1
                xcord = self.pointsList[i-1].x + ((I - D) / d) * (self.pointsList[i].x - self.pointsList[i-1].x)
                ycord = self.pointsList[i-1].y + ((I - D) / d) * (self.pointsList[i].y - self.pointsList[i-1].y)
                newPoint = points(xcord, ycord)
                self.resampledPointsList.append(newPoint)
                self.pointsList.insert(i, newPoint)
                self.length += 1
                D = 0
            else:
                D += d
            self.length -= 1
            i += 1
        self.length = len(self.resampledPointsList)
        if (len(self.resampledPointsList) == n - 1):
            newPoint = points(self.pointsList[len(self.pointsList) - 1].x, self.pointsList[len(self.pointsList) - 1].y)
            self.resampledPointsList.append(newPoint)
        return

    #  Rotate to zero
    def rotToZero(self):
        c = self.centroid()
        theta = math.atan2(c.y-self.resampledPointsList[0].y, c.x-self.resampledPointsList[0].x)
        newPoints = self.rotateBy(-1*theta)
        return newPoints

    #  Rotate by angle theta  
    def rotateBy(self, theta):
        # print("In rotateBy stroke, length = ",  len(self.resampledPointsList))
        c = self.centroid()
        newPoints = list()
        for i in self.resampledPointsList:
            x = (i.x - c.x)*(math.cos(theta)) - (i.y - c.y)*(math.sin(theta)) + c.x
            y = (i.x - c.x)*(math.sin(theta)) + (i.y - c.y)*(math.cos(theta)) + c.y
            newPoints.append(points(x,y))
        return newPoints
    
    # Calculate the centroid of the set of points
    def centroid(self):
        cx = sum([i.x for i in self.resampledPointsList])/len(self.resampledPointsList)
        cy = sum([i.y for i in self.resampledPointsList])/len(self.resampledPointsList)
        return points(cx, cy)
    
    # Scale the stroke to a bounding box
    def scaleToSquare(self, size):
        # print("Scaling to square of size = ", size)
        minB, maxB = self.boundingBox()
        bWidth = maxB.x - minB.x
        bHeight = maxB.y - minB.y
        for i in self.resampledPointsList:
            i.x *= size/bWidth
            i.y *= size/bHeight
        return

    # Translate Centroid to origin
    def translateToZero(self):
        c = self.centroid()
        for i in self.resampledPointsList:
            i.x -= c.x
            i.y -= c.y
        return

    # Define a common bounding box for all symbols
    def boundingBox(self):
        return points(0,0), points(100,100)

    def newRecognize(self, template):
        size = 100
        bestTemplate, b = self.findResultantVector(template)
        score = (1 - (b/(0.5*(2*size**2))))
        return bestTemplate, score

    def createDiffernceVector(self):
        centroid = self.centroid()
        self.differnceVector = list()
        for i in self.resampledPointsList:
            self.differnceVector.append(points(centroid.x - i.x, centroid.y - i.y))
        return 
     
    def findResultantVector(self, template):
        self.createDiffernceVector()
        minDist = 10**3
        bestTemplate = template[0]
        for T in template:
            resultantVector = self - T
            d = l2Norm(resultantVector)
            if (minDist > d):
                minDist = d
                bestTemplate = T
        return bestTemplate, d