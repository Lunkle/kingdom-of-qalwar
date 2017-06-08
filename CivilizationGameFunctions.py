from tkinter import *
from random import randint
import random
import colorsys
from time import sleep
from math import sin, sqrt, ceil
import CivilizationGameData as data

def init():
    data.gameStarted = True
    townHallTop = data.Building(data.townHallStartingX, data.townHallStartingY, data.TOWN_HALL_TOP)
    townHallTop.add()
    townHallLeft = data.Building(data.townHallStartingX, data.townHallStartingY + 1, data.TOWN_HALL_LEFT)
    townHallLeft.add()
    townHallRight = data.Building(data.townHallStartingX + 1, data.townHallStartingY, data.TOWN_HALL_RIGHT)
    townHallRight.add()
    townHallBottom = data.Building(data.townHallStartingX + 1, data.townHallStartingY + 1, data.TOWN_HALL_BOTTOM)
    townHallBottom.add()
    newBuilding = data.Building(1, 20, data.RESIDENCE)
    newBuilding.add()

def startGame():
    global startButton#, testButton
##    data.gameStarted = True
    startButton.destroy()
##    testButton.destroy()

def showStartPage():
    global startButton#, testButton
    startButton = Button(100, 100, "Start", data.startScreenButtonSize, startGame)
    startButton.displayButton()
##    testButton = Button(100, 200, "Donny", 4, printHi)
##    testButton.displayButton()

def getLandPolygonXYLength():
    polygonLandXLength = int(((data.tileSize * data.xTiles) * 2 ** 0.5)/1)
    polygonLandYLength = int(((data.tileSize * data.yTiles) * 2 ** 0.5)/2)
    return polygonLandXLength, polygonLandYLength

def getTileXYLength():
    tileXLength = ((data.tileSize) * 2 ** 0.5)/1
    tileYLength = ((data.tileSize) * 2 ** 0.5)/2
    return tileXLength, tileYLength

def fixPan():
    #TODO
    pass

def getRandomColour():
    #random.random() is a random number between 0.0 and 1.0
    h = random.random()             #between 0.0 and 1.0
    s = 0.9 + random.random()/10    #between 0.9 and 1.0
    l = 0.4 + random.random()/5.0   #between 0.4 and 0.6
    r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
    return "#%02x%02x%02x" % (r, g, b)

def keyPressDetector(event):
    #To update
    k = event.keysym
    if data.gameStarted == False:
        if k == "Return":
            data.gameStarted = True
        elif k == "Left" and data.changedTheme == True:
            data.currentThemeNumber -= 1
            data.leftArrowSize = 0.5
            data.changedTheme = False
        elif k == "Right" and data.changedTheme == True:
            data.currentThemeNumber += 1
            data.rightArrowSize = 0.5
            data.changedTheme = False
        setThemes(data.themesColours[data.themesList[data.currentThemeNumber%len(data.themesList)]])
    else:
        if k == "Return":
            if data.wantToPause == True:
                data.wantToPause = False
            elif data.wantToPause == False:
                data.wantToPause = True
        if data.updatedValue == True:
            if k == "Up" and data.newDirection != "Down":
                data.newDirection = "Up"
            elif k == "Down" and data.newDirection != "Up":
                data.newDirection = "Down"
            elif k == "Left" and data.newDirection != "Right":
                data.newDirection = "Left"
            elif k == "Right" and data.newDirection != "Left":
                data.newDirection = "Right"
            data.updatedValue = False

def keyReleaseDetector(event):
    k = event.keysym
    
def mouseDragDetector(event):
    if data.gameStarted == True:
        rawCurrentX = data.previousCurrentX + data.clickedXMouse - event.x - data.panSlipX
        rawCurrentY = data.previousCurrentY + data.clickedYMouse - event.y - data.panSlipY
        polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
        fixPan()
        data.currentX = rawCurrentX
        data.currentY = rawCurrentY

def mouseReleaseDetector(event):
    currentXLess = False
    currentYLess = False
    currentXMore = False
    currentYMore = False
    polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
    if data.currentX < 0:
        currentXLess = True
    elif data.currentX > polygonLandXLength - data.cWidth:
        currentXMore = True
    if data.currentY < 0:
        currentYLess = True
    if data.currentY > polygonLandYLength - data.cHeight:
        currentYMore = True
    while currentXLess == True or currentYLess == True or currentXMore == True or currentYMore == True:
        break

def mouseWheelHandler(event):
    oldPolygonLandXLength, oldPolygonLandYLength = getLandPolygonXYLength()
    
    if event.num == 5 or event.delta == -120:
        data.tileSize *= 0.90
    if event.num == 4 or event.delta == 120:
        data.tileSize *= 1.11
    if data.tileSize > data.maxTileSize:
        data.tileSize = data.maxTileSize
    elif data.tileSize < data.minTileSize:
        data.tileSize = data.minTileSize

    newPolygonLandXLength, newPolygonLandYLength = getLandPolygonXYLength()

    data.currentX = (data.currentX + data.cWidth/2)/oldPolygonLandXLength*newPolygonLandXLength - data.cWidth/2
    data.currentY = (data.currentY + data.cHeight/2)/oldPolygonLandYLength*newPolygonLandYLength - data.cHeight/2

def mousePressedDetector(event):
    data.clickedXMouse = event.x
    data.clickedYMouse = event.y
    data.previousCurrentX = data.currentX
    data.previousCurrentY = data.currentY
    for i in range(len(Button.buttonBounds)):
        if Button.buttonBounds[i][0] <= data.clickedXMouse <= Button.buttonBounds[i][2] and Button.buttonBounds[i][1] <= data.clickedYMouse <= Button.buttonBounds[i][3]:
            Button.buttonFunctions[i]() #This runs the assigned function or procedure call

def makeBitmap(x, y, squareSize, bitmap):
    skip = int(1/squareSize)
    if skip < 1:
        skip = 1
    squaresPixelsArray = []
    for i in range(0, len(bitmap), skip):
        for j in range(0, len(bitmap[i]), skip):
            colourCode = bitmap[i][j]
            if colourCode != "#ffffff":
                colour = colourCode
                squaresPixelsArray.append(data.s.create_rectangle(x + squareSize * j, y + squareSize * i, x + squareSize * (j + 1), y + squareSize * (i + 1), fill = colour, width = 0))
    return squaresPixelsArray

class Button():
    buttons = [] #This stores the entire scope of buttons and each of their pixels
                 #3D array --> the primary array stores each button
                 #         --> the secondary array stores each component of said button
                 #         --> the tertiary array stores each pixels of component
    buttonBounds = [] #This stores the boudaries of each button.
                      #Used in the mouse click function
    buttonFunctions = []
    BUTTON_ENDS_WIDTH = len(data.buttonSegments[data.BUTTON_LEFT][0]) + len(data.buttonSegments[data.BUTTON_RIGHT][0])
    BUTTON_MIDDLE_WIDTH = len(data.buttonSegments[data.BUTTON_MIDDLE_0][0])
    BUTTON_HEIGHT = len(data.buttonSegments[data.BUTTON_MIDDLE_0])
    def __init__(self, buttonX, buttonY, text, size, function):
        self.x = buttonX
        self.y = buttonY
        self.size = float(size)
        self.text = text
        self.length = 0
        for character in self.text:
            if character == " ":
                textLength = 10
            else:
                textLength = len(data.gameFontDictionary[character][0])
                if character == "q" or character == "Q":
                    textLength -= 10
            self.length += (textLength + data.buttonLetterSpacing) * self.size / 4.0
        self.number = len(Button.buttons)
        self.numOfMiddleSectionsRequired = ceil(self.length / Button.BUTTON_MIDDLE_WIDTH)
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.size * Button.BUTTON_ENDS_WIDTH + Button.BUTTON_MIDDLE_WIDTH * self.numOfMiddleSectionsRequired
        y2 = self.y + self.size * Button.BUTTON_HEIGHT
        Button.buttons.append([])
        Button.buttonBounds.append([x1, y1, x2, y2])
        Button.buttonFunctions.append(function)

    def displayButton(self):
        xValue = self.x #Index for where to place next segment of button
        remainingLength = self.length #Variable to notify when to stop
        #First Left Button Segment
        bitmapImage = data.buttonSegments[data.BUTTON_LEFT]
        Button.buttons[self.number].append(makeBitmap(xValue, self.y, self.size, bitmapImage))
        xValue += self.size * len(bitmapImage[0])
        letterIndex = xValue #This is where the letters start showing up
        while remainingLength > 0:
            bitmapImage = data.buttonSegments[data.BUTTON_MIDDLE_TEMPLATE + str(random.randint(0, len(data.buttonSegments) - 3))]
            Button.buttons[self.number].append(makeBitmap(xValue, self.y, self.size, bitmapImage))
            xValue += self.size * len(bitmapImage[0])
            remainingLength -= self.size * len(bitmapImage[0])
        bitmapImage = data.buttonSegments[data.BUTTON_RIGHT]
        Button.buttons[self.number].append(makeBitmap(xValue, self.y, self.size, bitmapImage))
        for character in self.text:
            if character == " ":
                letterIndex += 10 * self.size / 4.0
            else:
                bitmapImage = data.gameFontDictionary[character]
                Button.buttons[self.number].append(makeBitmap(letterIndex, self.y + (self.size * len(data.buttonSegments[data.BUTTON_MIDDLE_0]) - len(bitmapImage) * self.size / 4.0) / 2, self.size / 4.0, bitmapImage))
                letterIndex += (len(data.gameFontDictionary[character][0]) + data.buttonLetterSpacing ) * self.size / 4.0
        data.s.update()

    def destroy(self):
        for i in range(len(Button.buttons[self.number])):
            for j in range(len(Button.buttons[self.number][i])):
                data.s.delete(Button.buttons[self.number][i][j])

def updateLand():
    data.s.delete(data.landPolygon)
    for i in range(len(data.Building.buildings)):
        data.s.delete(data.Building.buildings[i])
        for j in range(len(data.Building.buildingImages[i])):
            data.s.delete(data.Building.buildingImages[i][j])
    polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
    tileXLength, tileYLength = getTileXYLength()

    landShapeX1 = -data.currentX #Left boundary
    landShapeY1 = polygonLandYLength / 2 - data.currentY #Middle of shape
    
    landShapeX2 = landShapeX1 + polygonLandXLength / 2
    landShapeY2 = -data.currentY #Top boundary
    
    landShapeX3 = landShapeX1 + polygonLandXLength
    landShapeY3 = landShapeY1
    
    landShapeX4 = landShapeX2
    landShapeY4 = landShapeY2 + polygonLandYLength
    
    data.landPolygon = data.s.create_polygon(landShapeX1, landShapeY1, landShapeX2, landShapeY2, landShapeX3, landShapeY3, landShapeX4, landShapeY4, fill = data.landColour, width = 0)
 
    for i in range(len(data.Building.buildings)):
        x = data.Building.buildingsX[i]
        y = data.Building.buildingsY[i]
        buildingX1 = landShapeX2 + ((x - y) / 2.0) * tileXLength # Top corner of
        buildingY1 = landShapeY2 + ((x + y) / 2.0) * tileYLength # quadrilateral
        if buildingX1 > -tileXLength * data.loadBuffer and buildingX1 < data.cWidth + tileXLength * data.loadBuffer and buildingY1 > -tileYLength * data.loadBuffer and buildingY1 < data.cHeight + tileYLength * data.loadBuffer:
            buildingX2 = buildingX1 + tileXLength / 2
            buildingY2 = buildingY1 + tileYLength / 2
            buildingX3 = buildingX1
            buildingY3 = buildingY2 + tileYLength / 2
            buildingX4 = buildingX1 - tileXLength / 2
            buildingY4 = buildingY2
            bitmapImage = data.buildingTypeImages[data.Building.buildingTypes[i]]
            bitmapTileRatio = data.buildingTypeSizes[data.Building.buildingTypes[i]]
            squareSize = tileXLength/len(bitmapImage[0]) * bitmapTileRatio

            data.Building.buildings[i] = data.s.create_polygon(buildingX1, buildingY1, buildingX2, buildingY2, buildingX3, buildingY3, buildingX4, buildingY4, width = 0, fill = "#ffffff")#data.landColour)
            data.Building.buildingImages[i] = makeBitmap(buildingX4 + tileXLength * (1 - bitmapTileRatio) / 2, buildingY3 - squareSize*len(bitmapImage), squareSize, bitmapImage)

def display():
    updateLand()
    data.s.update()
