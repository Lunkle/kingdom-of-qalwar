from random import randint
import random
import colorsys
from time import sleep
from math import sqrt, ceil
import CivilizationGameData as data

def showStartPage():
    global title, startButton, aboutButton
    startButton = Button(data.cWidth / 2 - 62, data.cHeight / 2, "Start", data.startScreenButtonSize, startGame)
    aboutButton = Button(data.cWidth / 2 - 66, data.cHeight / 2 + 60, "About", data.startScreenButtonSize, startGame)
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
    menuButton = Button(data.cWidth - 110, 10, "Menu", 2, showMenu)
    settingsButton = Button(10, 10, "Settings", 2, showSettings)
    updateResources()
    updateButtons()
    data.gameStarted = True

def showSettings():
    global doneButton
    createNotification(["You Suck", "A Lot"])
    doneButton = Button(data.cWidth / 2 - 46, data.cHeight * (1 / data.notificationScreenBorderY - 1) * data.notificationScreenBorderY - 60, "Done", 2, doneReading)
##    data.resolution = 4
##    data.reload(sprites)

def showMenu():
    global menuButton, nextSeasonButton, menuFeatures, menuScroller, backButton
    data.menuOpen = True
    menuButton.destroy()
    nextSeasonButton.destroy()
    menuFeatures = []
    menuFeatures.append([data.s.create_rectangle(data.cWidth - 200, 1, data.cWidth + 1, data.cHeight + 1, fill = "#d7d7d7", outline = "#7f7f7f", width = 3)])
    for i in range(data.numOfMenuPanels):
        menuFeatures.append([data.s.create_rectangle(data.cWidth - 190, i * 100 + 10, data.cWidth - 17, (i + 1) * 100, fill = "#d7d7d7", outline = "#7f7f7f", width = 3)])
    menuFeatures.append([data.s.create_rectangle(data.cWidth - 200, data.cHeight - 52, data.cWidth, data.cHeight + 1, fill = "#d7d7d7", outline = "#7f7f7f", width = 3)])
    menuScroller = Scroller(data.cWidth - 10, 10, data.scrollerPixelSize, 5, data.cHeight - 72, data.numOfMenuPanels * 90 + 20)
    backButton = Button(data.cWidth - 104, data. cHeight - 42, "Back", 2, closeMenu)
    updateButtons()
    data.s.update()

def closeMenu():
    global menuButton, nextSeasonButton, menuFeatures, menuScroller, backButton
    data.menuOpen = False
    menuButton = Button(data.cWidth - 110, 10, "Menu", 2, showMenu)
    nextSeasonButton = Button(data.cWidth - 200, data. cHeight - 42, "Next Season", 2, passTurn)
    for i in range(len(menuFeatures)):
        for j in range(len(menuFeatures[i])):
            if isinstance(menuFeatures[i][j], list):
                for k in range(len(menuFeatures[i][j])):
                    data.s.delete(menuFeatures[i][j][k])
            else:
                data.s.delete(menuFeatures[i][j])
    menuScroller.destroy()
    backButton.destroy()
    updateButtons()
    data.s.update()

def doneReading():
    global doneButton
    deleteNotification()
    doneButton.destroy()

def passTurn():
    global doneButton
    addResource([data.QALS, data.WOOD, data.GOLD, data.MANA], [data.qalsEconomy, data.woodEconomy, data.goldEconomy, data.manaEconomy])
    createNotification(["You collected", str(data.qalsEconomy) + " " + data.QALS, str(data.woodEconomy) + " " + data.WOOD, str(data.goldEconomy) + " " + data.GOLD, str(data.manaEconomy) + " " + data.MANA])
    doneButton = Button(data.cWidth / 2 - 46, data.cHeight * (1 / data.notificationScreenBorderY - 1) * data.notificationScreenBorderY - 60, "Done", 2, doneReading)

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
    for i in range(len(Scroller.scrollerBounds)):
        if Scroller.scrollerBounds[i][0] <= data.clickedXMouse <= Scroller.scrollerBounds[i][2] and Scroller.scrollerBounds[i][1] <= data.clickedYMouse <= Scroller.scrollerBounds[i][3]:
            data.clickedScroller = True
            Scroller.scrollerObject[i].clickedScroller = True
            Scroller.scrollerObject[i].clickedY = event.y - Scroller.scrollerObject[i].y

def mouseDragDetector(event):
    data.mouseDragged = True
    if data.gameStarted == True and data.menuOpen == False and data.notificationOpen == False:
        rawCurrentX = data.previousCurrentX + data.clickedXMouse - event.x - data.panSlipX
        rawCurrentY = data.previousCurrentY + data.clickedYMouse - event.y - data.panSlipY
        polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
        fixPan()
        data.currentX = rawCurrentX
        data.currentY = rawCurrentY
    if data.clickedScroller == True and data.scrollerUpdated == True:
        data.scrollerUpdated = False
        for i in range(len(Scroller.scrollerObject)):
            if Scroller.scrollerObject[i].clickedScroller == True:
                scroller = Scroller.scrollerObject[i]
                break
        scroller.draggedY = event.y - scroller.y - scroller.clickedY
        scroller.scrolledPercentage = float(scroller.draggedY) / float(scroller.scrollableLength) * 100
        if scroller.scrolledPercentage < 0:
            scroller.scrolledPercentage = 0
        if scroller.scrolledPercentage > 100:
            scroller.scrolledPercentage = 100
        scroller.deleteScroller()
        data.s.update()
        scroller.displayScroller()
        data.scrollerUpdated = True

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
    if data.gameStarted == True and data.mouseDragged == False and data.clickedButton == False and data.notificationOpen == False:
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
##        print("Clicked at:", int(landClickedX), int(landClickedY), "Intercepts:", int(xB), int(yB), "Tiles:", tileClickedX, tileClickedY, tileYLength)
    data.mouseDragged = False
    data.clickedButton = False
    data.clickedScroller = False

def mouseWheelHandler(event):
    if data.notificationOpen == False:
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
        if data.resourceAmounts[resources[i]] - amounts[i] < 0:
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
        data.highlightedTileObject = data.s.create_polygon(highlightX1, highlightY1, highlightX2, highlightY2, highlightX3, highlightY3, highlightX4, highlightY4, width = 0, fill = "yellow", stipple = "gray50")

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
    for i in range(len(data.resourceObjects)):
        for j in range(len(data.resourceObjects[i])):
            data.s.delete(data.resourceObjects[i][j])
    data.resourceObjects = []
    for i in range(len(data.resourceTypes) - 1, -1, -1):
        data.resourceObjects.append([data.s.create_rectangle(10, data.cHeight - (len(data.resourceTypes) - i) * 30, 10 + data.resourceIndicatorLength, data.cHeight - 10 - (len(data.resourceTypes) - 1 - i) * 30)])
        resource = data.resourceTypes[i]
        ratioOfResourceToMaximum = float(data.resourceAmounts[resource]) / data.resourceMaximum[resource]
##        print(ratioOfResourceToMaximum)
        #Top Left x1 y1, Bottom Right x2 y2
        data.resourceObjects.append([data.s.create_rectangle(10, data.cHeight - (len(data.resourceTypes) - i) * 30, 10 + data.resourceIndicatorLength * ratioOfResourceToMaximum, data.cHeight - 10 - (len(data.resourceTypes) - 1 - i) * 30, fill = data.resourceColours[resource])])
        data.resourceObjects.append(makeBitmap(8, data.cHeight - 3 - (len(data.resourceTypes) - i) * 30, 2, data.resourceIcons[resource]))
        data.resourceObjects.append(createText(40, data.cHeight - (len(data.resourceTypes) - i) * 30 + 4, str(data.resourceAmounts[resource]), data.resourceTextSize, addColour = [True, data.resourceColours[resource], 80]))

def updateScreen():
    if data.menuOpen == False and data.notificationOpen == False:
##        createText(data.cWidth / 2, 10, "Season ", 2)
        updateBuildings()
        updateLand()
        highlightSquare(data.highlightedTile[0], data.highlightedTile[1])
    data.s.update()
    sleep(0.01)

def createNotification(text):
    data.notificationOpen = True
    data.notificationPage.append([data.s.create_rectangle(0, 0, data.cWidth + 2, data.cHeight + 2, fill = "black", width = 0, stipple = "gray75")])
    data.s.update()
    data.notificationPage.append(makeBitmap(int(data.cWidth * data.notificationScreenBorderX), int(data.cHeight * data.notificationScreenBorderY), data.notificationPixelSize, data.paperPieces[data.PAPER_TOP_LEFT]))
    data.notificationPage.append(makeBitmap(int(data.cWidth * data.notificationScreenBorderX), int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_LEFT]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_BOTTOM_LEFT]))
    data.notificationPage.append(makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_TOP_RIGHT][0]) * data.notificationPixelSize, int(data.cHeight * data.notificationScreenBorderY), data.notificationPixelSize, data.paperPieces[data.PAPER_TOP_RIGHT]))
    data.notificationPage.append(makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_BOTTOM_RIGHT]))
    #Top Edge
    for i in range(int(data.cWidth * data.notificationScreenBorderX) + len(data.paperPieces[data.PAPER_TOP_LEFT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_TOP_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_UP][0]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_UP][0]) * data.notificationPixelSize):
        data.notificationPage.append(makeBitmap(i, int(data.cHeight * data.notificationScreenBorderY), data.notificationPixelSize, data.paperPieces[data.PAPER_UP]))
    data.notificationPage.append(makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_TOP_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_UP][0]) * data.notificationPixelSize, int(data.cHeight * data.notificationScreenBorderY), data.notificationPixelSize, data.paperPieces[data.PAPER_UP]))
    #Left Edge
    for i in range(int(data.cHeight * data.notificationScreenBorderY) + len(data.paperPieces[data.PAPER_TOP_LEFT]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_LEFT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize):
        data.notificationPage.append(makeBitmap(int(data.cWidth * data.notificationScreenBorderX), i, data.notificationPixelSize, data.paperPieces[data.PAPER_LEFT]))
    data.notificationPage.append(makeBitmap(int(data.cWidth * data.notificationScreenBorderX), int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_LEFT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_LEFT]))
    #Right Edge
    for i in range(int(data.cHeight * data.notificationScreenBorderY) + len(data.paperPieces[data.PAPER_TOP_RIGHT]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_RIGHT]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_RIGHT]) * data.notificationPixelSize):
        data.notificationPage.append(makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_RIGHT][0]) * data.notificationPixelSize, i, data.notificationPixelSize, data.paperPieces[data.PAPER_RIGHT]))
    data.notificationPage.append(makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_RIGHT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_RIGHT]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_RIGHT]))
    #Bottom Edge
    for i in range(int(data.cWidth * data.notificationScreenBorderX) + len(data.paperPieces[data.PAPER_BOTTOM_LEFT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_DOWN][0]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_DOWN][0]) * data.notificationPixelSize):
        data.notificationPage.append(makeBitmap(i, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_DOWN]))
    data.notificationPage.append(makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_BOTTOM_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_DOWN][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_DOWN]))
    #Middle
    for i in range(int(data.cWidth * data.notificationScreenBorderX) + len(data.paperPieces[data.PAPER_LEFT][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_RIGHT][0]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE][0]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_MIDDLE][0]) * data.notificationPixelSize):
        for j in range(int(data.cHeight * data.notificationScreenBorderY) + len(data.paperPieces[data.PAPER_UP]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE]) * data.notificationPixelSize, len(data.paperPieces[data.PAPER_MIDDLE]) * data.notificationPixelSize):
            data.notificationPage.append(makeBitmap(i, j, data.notificationPixelSize, data.paperPieces[data.PAPER_MIDDLE]))
            data.notificationPage.append(makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE][0]) * data.notificationPixelSize, j, data.notificationPixelSize, data.paperPieces[data.PAPER_MIDDLE]))
        data.notificationPage.append(makeBitmap(i, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_MIDDLE]))
    data.notificationPage.append(makeBitmap(int((1 / data.notificationScreenBorderX - 1) * data.cWidth * data.notificationScreenBorderX) - len(data.paperPieces[data.PAPER_LEFT]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE][0]) * data.notificationPixelSize, int((1 / data.notificationScreenBorderY - 1) * data.cHeight * data.notificationScreenBorderY) - len(data.paperPieces[data.PAPER_DOWN]) * data.notificationPixelSize - len(data.paperPieces[data.PAPER_MIDDLE]) * data.notificationPixelSize, data.notificationPixelSize, data.paperPieces[data.PAPER_MIDDLE]))
    for i in range(len(text)):
        textLength = getTextLength(text[i], data.notificationTextSize)
        data.notificationPage.append(createText((data.cWidth - textLength) / 2, 2 * data.cHeight / 3 + (i - len(text)) * 30, text[i], data.notificationTextSize))

def deleteNotification():
    data.notificationOpen = False
    for i in range(len(data.notificationPage)):
        for j in range(len(data.notificationPage[i])):
            data.s.delete(data.notificationPage[i][j])
    data.notificationPage = []

def makeBitmap(x, y, squareSize, bitmap, toBack = False, colourAdd = [False, "#ffffff", 50], onlyDarker = False):
    #Try not to use toBack, colourAdd, and onlyDarker all together because that will be very slow.
    #Actually only darker doesn't take up that much time to process. colourAdd is the real killer.
    skip = int(1/squareSize)
    if skip < 1:                #This is is to reduce how many pixels need to be drawn when zoomed out.
        skip = 1                #i.e. when each pixel only takes up half a square, you can skip a pixel every other time
    squaresPixelsArray = [] #This is the array that stores each pixel so they can be deleted.
    for i in range(0, len(bitmap), skip):
        for j in range(0, len(bitmap[i]), skip):
            colourCode = bitmap[i][j]
            if colourCode != "#ffffff":
                colour = colourCode
                if colourAdd[0] == True:
                    percentage = colourAdd[2] / 100.0
                    originalColour = colour
                    originalRGB = originalColour.lstrip('#')
                    oR, oG, oB = tuple(int(originalRGB[i:i+2], 16) for i in (0, 2 ,4))              #o = Original
                    addColour = colourAdd[1]
                    addRGB = addColour.lstrip('#')
                    aR, aG, aB = tuple(int(addRGB[i:i+2], 16) for i in (0, 2 ,4))                   #a = Added
                    dR, dG, dB = aR - oR, aG - oG, aB - oB                                          #d = Difference
                    if onlyDarker == True:
                        dR, dG, dB = [min(w, 0) for w in [dR, dG, dB]]
##                        print("original colour is darker")
                    nR, nG, nB = oR + dR * percentage, oG + dG * percentage, oB + dG * percentage   #n = New
                    nR, nG, nB = [min(w, 255) for w in [nR, nG, nB]]
                    nR, nG, nB = [max(w, 0) for w in [nR, nG, nB]]
                    colour = "#%02x%02x%02x" % (nR, nG, nB)
##                    print("Original =", oR, oG, oB, "    Added =", aR, aG, aB, "    Difference =", dR, dG, dB, "    New =", nR, nG, nB)
##                    print(originalColour, colour, percentage)
                pixel = data.s.create_rectangle(x + squareSize * j, y + squareSize * i, x + squareSize * (j + 1), y + squareSize * (i + 1), fill = colour, width = 0)
                squaresPixelsArray.append(pixel)
                if toBack == True:
                    data.s.tag_lower(pixel)
    return squaresPixelsArray #Return the aray so the pixels can be deleted

def createText(x, y, text, size, center = False, onButton = False, addColour = [False, "#ffffff", 0]):
    letterIndex = x
    letterArray = []
    for character in text:
            if character == " ":
                letterIndex += 20 * size / 4.0
            else:
                bitmapImage = data.font.fontDictionary[character]
                if onButton == True:
                    addColour = [True, "#af622d", 100]
                    letterArray += makeBitmap(letterIndex, y + (size * len(data.buttonSegments[data.BUTTON_MIDDLE_0]) - len(bitmapImage) * size / 4.0) / 2, size / 4.0, bitmapImage, colourAdd = addColour, onlyDarker = True)
                else:
                    letterArray += makeBitmap(letterIndex, y, size / 4.0, bitmapImage, colourAdd = addColour, onlyDarker = True)
                letterIndex += (len(data.font.fontDictionary[character][0]) + data.buttonLetterSpacing ) * size / 4.0
                if character == "q" or character == "Q":
                    letterIndex -= 10 * size / 4.0
    return letterArray

def getTextLength(text, size):
    stringLength = 0
    for character in text:
        if character == " ":
            stringLength += 20 * size / 4.0
        else:
            bitmapImage = data.font.fontDictionary[character]
            stringLength += (len(data.font.fontDictionary[character][0]) + data.buttonLetterSpacing) * size / 4.0
            if character == "q" or character == "Q":
                stringLength -= 10 * size / 4.0
    return stringLength

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
        Button.buttons[self.number].append(createText(letterIndex, self.y, self.text, self.size, onButton = True))

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
        Button.buttons[self.number][segmentNumber + 2] = createText(letterIndex, self.y, self.text, self.size, onButton = True)

    def delete(self): #For updating the screen
        for i in range(len(Button.buttons[self.number])):
            for j in range(len(Button.buttons[self.number][i])):
                data.s.delete(Button.buttons[self.number][i][j])

    def destroy(self):
        try: #Try to delete everything if it hasn't already been deleted
            for i in range(len(Button.buttons[self.number])):
                for j in range(len(Button.buttons[self.number][i])):
                    data.s.delete(Button.buttons[self.number][i][j])
        except:
            pass
        #Then delete all the data
        del Button.buttonBounds[self.number]    #Delete the bounds check
        del Button.buttons[self.number]         #Delete the pixels STORER (not the pixels themselves)
        del Button.buttonFunctions[self.number] #Delete the function
        del Button.buttonObject[self.number]    #Delete the object HOLDER (again, not the class instance itself)
        del Button.buttonSegments[self.number]  #Delete the button segment data (not each segment -- its data)
        for i in range(self.number, len(Button.buttonObject)):
            Button.buttonObject[i].number -= 1          #Reduce all numbers of following buttons by 1 to fill up the gap.

#Scroller Class
class Scroller():
    scrollerObject = [] #Stores every scroller object
    scrollerPixels = [] #This stores the entire scope of scrollers and each of their pixels
                 #3D array --> the primary array stores each scroller
                 #         --> the secondary array stores each component of said scroller
                 #         --> the tertiary array stores each pixels of component
    scrollerBounds = [] #This stores the boudaries of each scroller.
                      #Used in the mouse click function
    scrollerSegments = [] #2D array that stores each of the scroller's segments

    def __init__(self, scrollerX, scrollerY, scrollerPixelSize, scrollerWidth, scrollerHeight, displayedActualHeight):
        self.number = len(Scroller.scrollerObject)
        self.x = scrollerX
        self.y = scrollerY
        self.pixelSize = float(scrollerPixelSize)
        self.scrollerWidth = scrollerWidth
        self.scrollerHeight = scrollerHeight #Scroller height is the entire thing's height
        self.actualHeight = displayedActualHeight
        self.scrolledPercentage = 0
        self.scrollerXValue = self.x - (len(data.scrollerSegments[data.SCROLLER_MIDDLE_0][0]) * self.pixelSize - self.scrollerWidth) / 2
        self.clickedY = 0
        self.draggedY = 0
        self.clickedScroller = False

        Scroller.scrollerObject.append(self)

        Scroller.scrollerSegments.append([])
        Scroller.scrollerPixels.append([])

        Scroller.scrollerPixels[self.number].append([data.s.create_rectangle(self.x, self.y, self.x + self.scrollerWidth, self.y + self.scrollerHeight, fill = "#7f7f7f", width = 0)])
        fractionOfActualThatsSeen = (self.scrollerHeight + 20.0) / self.actualHeight

        #The size of the tab
        self.scrollerTabSize = fractionOfActualThatsSeen * self.scrollerHeight
        #How much you can actually scroll
        self.scrollableLength = self.scrollerHeight - self.scrollerTabSize

        #The top and bottom segments are additional to the actual scrolling part, which are the middle segments
        topBitmapImage = data.scrollerSegments[data.SCROLLER_TOP]
        Scroller.scrollerPixels[self.number].append(makeBitmap(self.scrollerXValue, self.y - len(topBitmapImage) * self.pixelSize, self.pixelSize, topBitmapImage))

        bottomBitmapImage = data.scrollerSegments[data.SCROLLER_BOTTOM]
        Scroller.scrollerPixels[self.number].append(makeBitmap(self.scrollerXValue, self.y + self.scrollerTabSize - 1, self.pixelSize, bottomBitmapImage))

        #These segments actually show where the thing is
        for i in range(int(self.y), self.y + int(self.scrollerTabSize), len(data.scrollerSegments[data.SCROLLER_MIDDLE_0]) * self.pixelSize):
            randomSegmentNumber = randint(0, len(data.scrollerSegments) - 3)
            Scroller.scrollerSegments[self.number].append(randomSegmentNumber)
            bitmapImage = data.scrollerSegments[data.SCROLLER_MIDDLE_TEMPLATE + str(randomSegmentNumber)]
            Scroller.scrollerPixels[self.number].append(makeBitmap(self.scrollerXValue, self.y + i * self.pixelSize, self.pixelSize, bitmapImage))

        Scroller.scrollerBounds.append([self.scrollerXValue, self.y - len(topBitmapImage) * self.pixelSize, self.scrollerXValue + len(data.scrollerSegments[data.SCROLLER_MIDDLE_0][0]) * self.pixelSize, self.y + self.scrollerTabSize + len(bottomBitmapImage) * self.pixelSize])

    def displayScroller(self):
        yIndex = self.scrolledPercentage / 100.0 * self.scrollableLength
        print("Display at yvalue ", self.scrolledPercentage / 100.0 * self.scrollerHeight + 10)

        topBitmapImage = data.scrollerSegments[data.SCROLLER_TOP]
        Scroller.scrollerPixels[self.number][1] = makeBitmap(self.scrollerXValue, self.y - len(topBitmapImage) * self.pixelSize + yIndex, self.pixelSize, topBitmapImage)

        bottomBitmapImage = data.scrollerSegments[data.SCROLLER_BOTTOM]
        Scroller.scrollerPixels[self.number][2] = makeBitmap(self.scrollerXValue, self.y + self.scrollerTabSize + yIndex - 1, self.pixelSize, bottomBitmapImage)

        segmentIndex = 0
        for i in range(len(Scroller.scrollerSegments[self.number])):
            segmentNumber = Scroller.scrollerSegments[self.number][i]
            bitmapImage = data.scrollerSegments[data.SCROLLER_MIDDLE_TEMPLATE + str(segmentNumber)]
            Scroller.scrollerPixels[self.number][3 + segmentIndex] = makeBitmap(self.scrollerXValue, self.y + i * self.pixelSize + yIndex, self.pixelSize, bitmapImage)
            segmentIndex += 1
            
        Scroller.scrollerBounds[self.number] = [self.scrollerXValue, self.y - len(topBitmapImage) * self.pixelSize + yIndex, self.scrollerXValue + len(data.scrollerSegments[data.SCROLLER_MIDDLE_0][0]) * self.pixelSize, self.y + self.scrollerTabSize + len(bottomBitmapImage) * self.pixelSize + yIndex]
        print(Scroller.scrollerBounds[self.number])

    def deleteScroller(self): #For updating the screen
        for i in range(1, len(Scroller.scrollerPixels[self.number])):
            for j in range(len(Scroller.scrollerPixels[self.number][i])):
                data.s.delete(Scroller.scrollerPixels[self.number][i][j])

    def destroy(self):
        try: #Try to delete everything if it hasn't already been deleted
            for i in range(len(Scroller.scrollerPixels[self.number])):
                for j in range(len(Scroller.scrollerPixels[self.number][i])):
                    data.s.delete(Scroller.scrollerPixels[self.number][i][j])
        except:
            pass
        #Then delete all the data
        del Scroller.scrollerBounds[self.number]    #Delete the bounds check
        del Scroller.scrollerPixels[self.number]    #Delete the pixels STORER (not the pixels themselves)
        del Scroller.scrollerObject[self.number]    #Delete the object HOLDER (again, not the class instance itself)
        del Scroller.scrollerSegments[self.number]  #Delete the scroller segment data (not each segment -- its data)
        for i in range(self.number, len(Scroller.scrollerObject)):
            Scroller.scrollerObject[i].number -= 1          #Reduce all numbers of following scrollers by 1 to fill up the gap.
