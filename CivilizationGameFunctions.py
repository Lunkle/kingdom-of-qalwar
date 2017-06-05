from Tkinter import *
from random import randint
import random
import colorsys
from math import sin, sqrt
import CivilizationGameData as data
from time import sleep

def init():
    newBuilding = data.Building(0, 0, data.RESIDENCE)
    newBuilding.add()
    newBuilding = data.Building(1, 15, data.RESIDENCE)
    newBuilding.add()

def getLandPolygonXYLength():
    polygonLandXLength = int(((data.tileSize * data.xTiles) * 2 ** 0.5)/3)
    polygonLandYLength = int(((data.tileSize * data.yTiles) * 2 ** 0.5)/4)
    return polygonLandXLength, polygonLandYLength

def getTileXYLength():
    tileXLength = int(((data.tileSize) * 2 ** 0.5)/3)
    tileYLength = int(((data.tileSize) * 2 ** 0.5)/4)
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
    

def mousePressedDetector(event):
    print "clicked at", event.x, event.y
    data.clickedXMouse = event.x
    data.clickedYMouse = event.y
    data.previousCurrentX = data.currentX
    data.previousCurrentY = data.currentY

def mouseDragDetector(event):
##    print data.currentX, data.currentY
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
##        print("fixing...")
##        sleep(0.01)
##        if currentXLess == True or currentXMore == True:
##            if data.currentX < 0:
##                data.currentX += int(abs(data.currentX) ** data.panLimitFactor / data.panLimitSpeed)
##            elif data.currentX > polygonLandXLength - data.cWidth:
##                data.currentX -= int(abs(data.currentX - polygonLandXLength - data.cWidth) ** data.panLimitFactor / data.panLimitSpeed)
##            else:
##                currentXLess = False
##                currentXMore = False
##        if currentYLess == True or currentYMore == True:
##            if data.currentY < 0:
##                data.currentY += int(abs(data.currentY) ** data.panLimitFactor / data.panLimitSpeed)
##            elif data.currentY > polygonLandYLength - data.cHeight:
##                data.currentY -= int(abs(data.currentY - polygonLandYLength - data.cHeight) ** data.panLimitFactor / data.panLimitSpeed)
##            else:
##                currentYLess = False
##                currentYMore = False
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

    xDifferencePolygonLandLength = newPolygonLandXLength - oldPolygonLandXLength
    yDifferencePolygonLandLength = newPolygonLandYLength - oldPolygonLandYLength

    data.currentX += xDifferencePolygonLandLength/2
    data.currentY += yDifferencePolygonLandLength/2


def makeBitmap(x, y, squareSize, bitmap, screen):
    squaresPixelsArray = []
    for i in range(len(bitmap)):
        for j in range(len(bitmap[i])):
            colourCode = bitmap[i][j]
            if colourCode != "#ffffff":
                colour = colourCode
                squaresPixelsArray.append(screen.create_rectangle(x + squareSize * j, y + squareSize * i, x + squareSize * (j + 1), y + squareSize * (i + 1), fill = colour, width = 0))
    return squaresPixelsArray


def showStartPage():
    pass

def updateLand():
    data.s.delete(data.landPolygon)
    for i in range(len(data.Building.buildings)):
        data.s.delete(data.Building.buildings[i])
        for j in range(len(data.Building.buildingImages[i])):
            data.s.delete(data.Building.buildingImages[i][j])
    polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
    tileXLength, tileYLength = getTileXYLength()

    landShapeX1 = -data.currentX #Right boundary
    landShapeY1 = polygonLandYLength / 2 - data.currentY
    
    landShapeX2 = landShapeX1 + polygonLandXLength / 2
    landShapeY2 = -data.currentY #Top boundary
    
    landShapeX3 = landShapeX1 + polygonLandXLength
    landShapeY3 = landShapeY1
    
    landShapeX4 = landShapeX2
    landShapeY4 = landShapeY2 + polygonLandYLength
    
    data.landPolygon = data.s.create_polygon(landShapeX1, landShapeY1, landShapeX2,
 landShapeY2, landShapeX3, landShapeY3, landShapeX4, landShapeY4, fill =
 data.landColour, width = 0)
 
    for i in range(len(data.Building.buildings)):
        x = data.Building.buildingsX[i]
        y = data.Building.buildingsY[i]
        
        buildingX1 = landShapeX2 + ((x - y) / 2) * tileXLength # Top corner of
        buildingY1 = landShapeY2 + ((x + y) / 2) * tileYLength # quadrilateral
        buildingX2 = buildingX1 + tileXLength / 2
        buildingY2 = buildingY1 + tileYLength / 2
        buildingX3 = buildingX1
        buildingY3 = buildingY2 + tileYLength / 2
        buildingX4 = buildingX1 - tileXLength / 2
        buildingY4 = buildingY2
        
        data.Building.buildings[i] = data.s.create_polygon(buildingX1, buildingY1, buildingX2, buildingY2, buildingX3, buildingY3, buildingX4, buildingY4, fill = "black", width = 0)
        bitmapImage = data.buildingTypeImages[data.Building.buildingTypes[i]]
        len(bitmapImage)
        data.Building.buildingImages[i] = makeBitmap(buildingX4, buildingY3, tileXLength/len(bitmapImage[0]), bitmapImage, data.s)
##        print(int(buildingX1 - 245), int(buildingY1 - 245), int(buildingX2 - 245), int(buildingY2 - 245), int(buildingX3 - 245), int(buildingY3 - 245), int(buildingX4 - 245), int(buildingY4 - 245)









