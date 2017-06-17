##from tkinter import *
from random import randint
import random
import colorsys
from time import sleep
from math import sin, cos, asin, acos, sqrt, ceil
import CivilizationGameData as data

def showStartPage():
    global title, startButton, aboutButton
    startButton = Button(data.cWidth / 2 - 62, data.cHeight / 2, "Start", data.startScreenButtonSize, startGame)
    startButton.createButton()
    aboutButton = Button(data.cWidth / 2 - 66, data.cHeight / 2 + 60, "About", data.startScreenButtonSize, startGame)
    aboutButton.createButton()
    title = createText(data.cWidth / 2 - 130, 120, "Kingdom of Qalwar", 2)

def initializeGame():
    testBuilding = data.Building(10, 10, data.RESIDENCE)
    testBuilding.add()

    townHallTop = data.Building(data.townHallStartingX, data.townHallStartingY, data.TOWN_HALL_TOP)
    townHallTop.add()
    townHallLeft = data.Building(data.townHallStartingX, data.townHallStartingY + 1, data.TOWN_HALL_LEFT)
    townHallLeft.add()
    townHallRight = data.Building(data.townHallStartingX + 1, data.townHallStartingY, data.TOWN_HALL_RIGHT)
    townHallRight.add()
    townHallBottom = data.Building(data.townHallStartingX + 1, data.townHallStartingY + 1, data.TOWN_HALL_BOTTOM)
    townHallBottom.add()

    enemyBaseTop = data.Building(data.enemyBaseStartingX, data.enemyBaseStartingY, data.ENEMY_BASE_TOP)
    enemyBaseTop.add()
    enemyBaseLeft = data.Building(data.enemyBaseStartingX, data.enemyBaseStartingY + 1, data.ENEMY_BASE_LEFT)
    enemyBaseLeft.add()
    enemyBaseRight = data.Building(data.enemyBaseStartingX + 1, data.enemyBaseStartingY, data.ENEMY_BASE_RIGHT)
    enemyBaseRight.add()
    enemyBaseBottom = data.Building(data.enemyBaseStartingX + 1, data.enemyBaseStartingY + 1, data.ENEMY_BASE_BOTTOM)
    enemyBaseBottom.add()


def startGame():
    global title, startButton, aboutButton, nextSeasonButton, menuButton, settingsButton
    for i in range(len(title)):
        data.s.delete(title[i])
    startButton.destroy()
    aboutButton.destroy()
    nextSeasonButton = Button(data.cWidth - 200, data. cHeight - 42, "Next Season", 2, passTurn)
    nextSeasonButton.createButton()
    menuButton = Button(data.cWidth - 110, 10, "Menu", 2, showMenu)
    menuButton.createButton()
    settingsButton = Button(10, 10, "Settings", 2, showSettings)
    settingsButton.createButton()
    updateResources()
    updateButtons()
    data.gameStarted = True

def showSettings():
    createNotification()
##    data.resolution = 4
##    data.reload(sprites)

def showMenu():
    global menuButton, nextSeasonButton, menuFeatures, backButton
    data.menuOpen = True
    menuButton.destroy()
    nextSeasonButton.destroy()
    menuFeatures = []
    menuFeatures.append(data.s.create_rectangle(data.cWidth - 200, 1, data.cWidth + 1, data.cHeight + 1, fill = "#d7d7d7", outline = "#7f7f7f", width = 3))
    menuFeatures.append(data.s.create_line(data.cWidth - 200, data.cHeight - 52, data.cWidth, data.cHeight - 52, fill = "#7f7f7f", width = 3))
    backButton = Button(data.cWidth - 104, data. cHeight - 42, "Back", 2, closeMenu)
    backButton.createButton()
    updateButtons()
    data.s.update()

def closeMenu():
    global menuButton, nextSeasonButton, menuFeatures, backButton
    data.menuOpen = False
    menuButton = Button(data.cWidth - 110, 10, "Menu", 2, showMenu)
    menuButton.createButton()
    nextSeasonButton = Button(data.cWidth - 200, data. cHeight - 42, "Next Season", 2, passTurn)
    nextSeasonButton.createButton()
    for i in range(len(menuFeatures)):
        data.s.delete(menuFeatures[i])
    backButton.destroy()
    updateButtons()
    data.s.update()

def passTurn():
    addResource([data.QALS, data.WOOD, data.GOLD, data.MANA], [100, 100, 5, 10])

def tutorial():
    ##
    ##
    ##
    pass

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
    pass

def keyReleaseDetector(event):
    k = event.keysym

def mousePressedDetector(event):
    data.clickedXMouse = event.x
    data.clickedYMouse = event.y
    data.previousCurrentX = data.currentX
    data.previousCurrentY = data.currentY
    for i in range(len(Button.buttonBounds)):
        try:
            if Button.buttonBounds[i][0] <= data.clickedXMouse <= Button.buttonBounds[i][2] and Button.buttonBounds[i][1] <= data.clickedYMouse <= Button.buttonBounds[i][3]:
                data.clickedButton = True
                Button.buttonFunctions[i]() #This runs the assigned function or procedure call
        except:
            pass

def mouseDragDetector(event):
    data.mouseDragged = True
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
    if data.gameStarted == True and data.mouseDragged == False and data.clickedButton == False:
        polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
        tileXLength, tileYLength = getTileXYLength()
        landClickedX = data.clickedXMouse + data.currentX
        landClickedY = data.clickedYMouse + data.currentY
        xB = landClickedY + landClickedX / 2 - polygonLandYLength / 2
        yB = -(landClickedY - landClickedX / 2 - polygonLandYLength / 2)
        tileClickedX = int(xB / tileYLength)
        tileClickedY = data.yTiles - int(yB / tileYLength) - 1
        if 0 <= tileClickedX < data.xTiles and 0 <= tileClickedY < data.yTiles:
            if data.highlightedTile != [tileClickedX, tileClickedY]:
                highlightSquare(tileClickedX, tileClickedY)
        print("Clicked at:", int(landClickedX), int(landClickedY), "Intercepts:", int(xB), int(yB), "Tiles:", tileClickedX, tileClickedY, tileYLength)
    data.mouseDragged = False
    data.clickedButton = False

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

def addResource(resources, amounts):
    for i in range(len(resources)):
        data.resourceAmounts[resources[i]] += amounts[i]
        if data.resourceAmounts[resources[i]] > data.resourceMaximum[resources[i]]:
           data.resourceAmounts[resources[i]] = data.resourceMaximum[resources[i]]
    updateResources()

def removeResource(resources, amounts):
    for i in range(len(resources)):
        if data.resourceAmounts[resources[i]] < 0:
            return False
    for i in range(len(resources)):
        data.resourceAmounts[resources[i]] -= amounts[i]
    updateResources()
    return True

def highlightSquare(x, y):
    polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
    tileXLength, tileYLength = getTileXYLength()
    data.s.delete(data.highlightedTileObject)
    data.highlightedTileObject = 0
    data.highlightedTile = [x, y]
    landShapeTopX = -data.currentX + polygonLandXLength / 2
    landShapeTopY = -data.currentY #Top boundary
    highlightX1 = landShapeTopX + ((x - y) / 2.0) * tileXLength
    highlightY1 = landShapeTopY + ((x + y) / 2.0) * tileYLength
    if highlightX1 > -tileXLength * data.loadBuffer and highlightX1 < data.cWidth + tileXLength * data.loadBuffer and highlightY1 > -tileYLength * data.loadBuffer and highlightY1 < data.cHeight + tileYLength * data.loadBuffer:
        highlightX2 = highlightX1 + tileXLength / 2
        highlightY2 = highlightY1 + tileYLength / 2
        highlightX3 = highlightX1
        highlightY3 = highlightY2 + tileYLength / 2
        highlightX4 = highlightX1 - tileXLength / 2
        highlightY4 = highlightY2
        data.highlightedTileObject = data.s.create_polygon(highlightX1, highlightY1, highlightX2, highlightY2, highlightX3, highlightY3, highlightX4, highlightY4, width = 0, fill = "yellow")

def updateLand():
    data.s.delete(data.landPolygon)
    data.s.delete(data.dirtLeft, data.dirtRight)

    polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
    tileXLength, tileYLength = getTileXYLength()

    landShapeX1 = -data.currentX #Left boundary
    landShapeY1 = polygonLandYLength / 2 - data.currentY #Middle of shape

    landShapeX2 = landShapeX1 + polygonLandXLength / 2
    landShapeY2 = -data.currentY #Top boundary

    landShapeX3 = landShapeX1 + polygonLandXLength
    landShapeY3 = landShapeY1 #Right boundary

    landShapeX4 = landShapeX2 #Bottom boundary
    landShapeY4 = landShapeY2 + polygonLandYLength

    data.landPolygon = data.s.create_polygon(landShapeX1, landShapeY1, landShapeX2, landShapeY2, landShapeX3, landShapeY3, landShapeX4, landShapeY4, fill = data.landColour, outline = data.landOutlineColour, width = 1)
    data.s.tag_lower(data.landPolygon)
    data.dirtLeft = data.s.create_polygon(landShapeX1, landShapeY1, landShapeX4, landShapeY4, landShapeX4, landShapeY4 + tileYLength * data.dirtThickness, landShapeX1, landShapeY1 + tileYLength * data.dirtThickness, fill = data.dirtColour, outline = data.dirtOutlineColour, width = 1)
    data.dirtRight = data.s.create_polygon(landShapeX3, landShapeY3, landShapeX4, landShapeY4, landShapeX4, landShapeY4 + tileYLength * data.dirtThickness, landShapeX3, landShapeY3 + tileYLength * data.dirtThickness, fill = data.dirtColour, outline = data.dirtOutlineColour, width = 1)
    data.s.tag_lower(data.dirtLeft)
    data.s.tag_lower(data.dirtRight)

def updateBuildings():
    for i in range(len(data.Building.buildingObject)):
        for j in range(len(data.Building.buildingImages[i])):
            data.s.delete(data.Building.buildingImages[i][j])

    polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
    tileXLength, tileYLength = getTileXYLength()
    landShapeTopX = -data.currentX + polygonLandXLength / 2
    landShapeTopY = -data.currentY
    for i in range(len(data.Building.buildingObject)):
        x = data.Building.buildingsX[i]
        y = data.Building.buildingsY[i]
        buildingX1 = landShapeTopX + ((x - y) / 2.0) * tileXLength # Top corner of
        buildingY1 = landShapeTopY + ((x + y) / 2.0) * tileYLength # quadrilateral
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

            data.Building.buildingImages[i] = makeBitmap(buildingX4 + tileXLength * (1 - bitmapTileRatio) / 2, buildingY3 - squareSize*len(bitmapImage), squareSize, bitmapImage, toBack = True)

def updateButtons():
    for i in range(len(Button.buttonObject)):
        Button.buttonObject[i].delete()
        Button.buttonObject[i].displayButton()

def updateResources():
    for i in range(len(data.resourceTypes) - 1, -1, -1):
        data.s.create_rectangle(10, data.cHeight - (len(data.resourceTypes) - i) * 30, data.resourceIndicatorLength, data.cHeight - 10 - (len(data.resourceTypes) - 1 - i) * 30)
        resource = data.resourceTypes[i]
        ratioOfResourceToMaximum = float(data.resourceAmounts[resource]) / data.resourceMaximum[resource]
        #Top Left x1 y1, Bottom Right x2 y2
        data.s.create_rectangle(10, data.cHeight - (len(data.resourceTypes) - i) * 30, data.resourceIndicatorLength * ratioOfResourceToMaximum, data.cHeight - 10 - (len(data.resourceTypes) - 1 - i) * 30, fill = data.resourceColours[resource])
        makeBitmap(8, data.cHeight - 3 - (len(data.resourceTypes) - i) * 30, 2, data.resourceIcons[resource])

def updateScreen():
    if data.menuOpen == False:
##        createText(data.cWidth / 2, 10, "Season ", 2)
        updateBuildings()
        updateLand()
        highlightSquare(data.highlightedTile[0], data.highlightedTile[1])
    data.s.update()
    sleep(0.01)

def createNotification():
    data.s.create_rectangle(0, 0, data.cWidth + 2, data.cHeight + 2, fill = "black", width = 0, stipple = "gray75")
    makeBitmap(int(data.cWidth * data.notificationScreenBorderX), int(data.cHeight * data.notificationScreenBorderY), data.notificationPixelSize, data.paperPieces[data.PAPER_TOP_LEFT])
    makeBitmap(int(data.cWidth * data.notificationScreenBorderX), int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_LEFT]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_BOTTOM_LEFT])
    makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_TOP_RIGHT][0]) * data.notificationPixelSize, int(data.cHeight * data.notificationScreenBorderY), data.notificationPixelSize, data.paperPieces[data.PAPER_TOP_RIGHT])
    makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_BOTTOM_RIGHT])
    #Top Edge
    for i in range(int(data.cWidth * data.notificationScreenBorderX) + len(data.paperPieces[data.PAPER_TOP_LEFT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_TOP_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_UP][0]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_UP][0]) * data.notificationPixelSize):
        makeBitmap(i, int(data.cHeight * data.notificationScreenBorderY), data.notificationPixelSize, data.paperPieces[data.PAPER_UP])
    makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_TOP_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_UP][0]) * data.notificationPixelSize, int(data.cHeight * data.notificationScreenBorderY), data.notificationPixelSize, data.paperPieces[data.PAPER_UP])
    #Left Edge
    for i in range(int(data.cHeight * data.notificationScreenBorderY) + len(data.paperPieces[data.PAPER_TOP_LEFT]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_LEFT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize):
        makeBitmap(int(data.cWidth * data.notificationScreenBorderX), i, data.notificationPixelSize, data.paperPieces[data.PAPER_LEFT])
    makeBitmap(int(data.cWidth * data.notificationScreenBorderX), int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_LEFT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_LEFT])
    #Right Edge
    for i in range(int(data.cHeight * data.notificationScreenBorderY) + len(data.paperPieces[data.PAPER_TOP_RIGHT]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_RIGHT]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_RIGHT]) * data.notificationPixelSize):
        makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_RIGHT][0]) * data.notificationPixelSize, i, data.notificationPixelSize, data.paperPieces[data.PAPER_RIGHT])
    makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_RIGHT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_RIGHT]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_RIGHT])
    #Bottom Edge
    for i in range(int(data.cWidth * data.notificationScreenBorderX) + len(data.paperPieces[data.PAPER_BOTTOM_LEFT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_DOWN][0]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_DOWN][0]) * data.notificationPixelSize):
        makeBitmap(i, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_DOWN])
    makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_DOWN][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_DOWN])
    #Middle
    for i in range(int(data.cWidth * data.notificationScreenBorderX) + len(data.paperPieces[data.PAPER_LEFT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE][0]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_MIDDLE][0]) * data.notificationPixelSize):
        for j in range(int(data.cHeight * data.notificationScreenBorderY) + len(data.paperPieces[data.PAPER_UP]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_MIDDLE]) * data.notificationPixelSize):
            makeBitmap(i, j, data.notificationPixelSize, data.paperPieces[data.PAPER_MIDDLE])
            makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE][0]) * data.notificationPixelSize, j, data.notificationPixelSize, data.paperPieces[data.PAPER_MIDDLE])
        makeBitmap(i, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_MIDDLE])
    makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_MIDDLE])

def makeBitmap(x, y, squareSize, bitmap, toBack = False):
    skip = int(1/squareSize)
    if skip < 1:
        skip = 1
    squaresPixelsArray = []
    for i in range(0, len(bitmap), skip):
        for j in range(0, len(bitmap[i]), skip):
            colourCode = bitmap[i][j]
            if colourCode != "#ffffff":
                colour = colourCode
                pixel = data.s.create_rectangle(x + squareSize * j, y + squareSize * i, x + squareSize * (j + 1), y + squareSize * (i + 1), fill = colour, width = 0)
                squaresPixelsArray.append(pixel)
                if toBack == True:
                    data.s.tag_lower(pixel)
    return squaresPixelsArray

def createText(x, y, text, size, center = False):
    letterIndex = x
    letterArray = []
    for character in text:
            if character == " ":
                letterIndex += 20 * size / 4.0
            else:
                bitmapImage = data.font.fontDictionary[character]
                if center == True:
                    letterArray += makeBitmap(letterIndex, y + (size * len(data.buttonSegments[data.BUTTON_MIDDLE_0]) - len(bitmapImage) * size / 4.0) / 2, size / 4.0, bitmapImage)
                else:
                    letterArray += makeBitmap(letterIndex, y, size / 4.0, bitmapImage)
                letterIndex += (len(data.font.fontDictionary[character][0]) + data.buttonLetterSpacing ) * size / 4.0
                if character == "q" or character == "Q":
                    letterIndex -= 10 * size / 4.0
    return letterArray

#Button Class
class Button():
    buttonObject = [] #Stores every button object
    buttons = [] #This stores the entire scope of buttons and each of their pixels
                 #3D array --> the primary array stores each button
                 #         --> the secondary array stores each component of said button
                 #         --> the tertiary array stores each pixels of component
    buttonBounds = [] #This stores the boudaries of each button.
                      #Used in the mouse click function
    buttonSegments = [] #2D array that stores each of the button's segments
    buttonFunctions = [] #Stores the function called when clicked
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
                textLength = len(data.font.fontDictionary[character][0])
                if character == "q" or character == "Q":
                    textLength -= 10
            self.length += (textLength + data.buttonLetterSpacing) * self.size / 4.0
        self.number = len(Button.buttons)
        self.numOfMiddleSectionsRequired = ceil(self.length / Button.BUTTON_MIDDLE_WIDTH)
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.size * Button.BUTTON_ENDS_WIDTH + Button.BUTTON_MIDDLE_WIDTH * self.numOfMiddleSectionsRequired
        y2 = self.y + self.size * Button.BUTTON_HEIGHT
        Button.buttonObject.append(self)
        Button.buttons.append([])
        Button.buttonSegments.append([])
        Button.buttonBounds.append([x1, y1, x2, y2])
        Button.buttonFunctions.append(function)

    def createButton(self):
        xValue = self.x #Index for where to place next segment of button
        remainingLength = self.length #Variable to notify when to stop
        #First Left Button Segment
        bitmapImage = data.buttonSegments[data.BUTTON_LEFT]
        Button.buttons[self.number].append(makeBitmap(xValue, self.y, self.size, bitmapImage))
        xValue += self.size * len(bitmapImage[0])
        letterIndex = xValue #This is where the letters start showing up
        while remainingLength > 0:
            randomSegmentNumber = random.randint(0, len(data.buttonSegments) - 3)
            Button.buttonSegments[self.number].append(randomSegmentNumber)
            bitmapImage = data.buttonSegments[data.BUTTON_MIDDLE_TEMPLATE + str(randomSegmentNumber)]
            Button.buttons[self.number].append(makeBitmap(xValue, self.y, self.size, bitmapImage))
            xValue += self.size * len(bitmapImage[0])
            remainingLength -= self.size * len(bitmapImage[0])
        bitmapImage = data.buttonSegments[data.BUTTON_RIGHT]
        Button.buttons[self.number].append(makeBitmap(xValue, self.y, self.size, bitmapImage))
        Button.buttons[self.number].append(createText(letterIndex, self.y, self.text, self.size, center = True))

    def displayButton(self):
        xValue = self.x #Index for where to place next segment of button
        remainingLength = self.length #Variable to notify when to stop
        #First Left Button Segment
        bitmapImage = data.buttonSegments[data.BUTTON_LEFT]
        Button.buttons[self.number][0] = makeBitmap(xValue, self.y, self.size, bitmapImage)
        xValue += self.size * len(bitmapImage[0])
        letterIndex = xValue #This is where the letters start showing up
        segmentNumber = 0
        while remainingLength > 0:
            bitmapImage = data.buttonSegments[data.BUTTON_MIDDLE_TEMPLATE + str(Button.buttonSegments[self.number][segmentNumber])]
            segmentNumber += 1
            Button.buttons[self.number][segmentNumber] = makeBitmap(xValue, self.y, self.size, bitmapImage)
            xValue += self.size * len(bitmapImage[0])
            remainingLength -= self.size * len(bitmapImage[0])
        bitmapImage = data.buttonSegments[data.BUTTON_RIGHT]
        Button.buttons[self.number][segmentNumber + 1] = (makeBitmap(xValue, self.y, self.size, bitmapImage))
        Button.buttons[self.number][segmentNumber + 2] = createText(letterIndex, self.y, self.text, self.size, center = True)

    def delete(self):
        for i in range(len(Button.buttons[self.number])):
            for j in range(len(Button.buttons[self.number][i])):
                data.s.delete(Button.buttons[self.number][i][j])

    def destroy(self):
        try:
            for i in range(len(Button.buttons[self.number])):
                for j in range(len(Button.buttons[self.number][i])):
                    data.s.delete(Button.buttons[self.number][i][j])
        except:
            pass
        del Button.buttonBounds[self.number]
        del Button.buttons[self.number]
        del Button.buttonFunctions[self.number]
        del Button.buttonObject[self.number]
        del Button.buttonSegments[self.number]
        for i in range(self.number, len(Button.buttonObject)):
            Button.buttonObject[i].number -= 1
