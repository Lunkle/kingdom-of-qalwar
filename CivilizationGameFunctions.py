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
    data.seasonIndicator = createText(data.cWidth / 2 - 100, 10, "Season " + str(data.seasonNumber), 2, addColour = [True, data.seasonTextHighlightColour, 50])
    data.gameStarted = True

def buyPanelGraphics(x1, y1, x2, y2, text, size):
    pixelsArray = []
    pixelsArray += [data.s.create_line(x1, y2 + (y1 - y2) / 4, x2, y2 + (y1 - y2) / 4)]
    pixelsArray += createText((x1 + x2 - getTextLength(text, size)) / 2, y2 + (y1 - y2) / 4 + 2, text, size)
    return pixelsArray

def buyPanelFunctions(buildingType):
    closeMenu()
    data.placingDownBuilding = True
    data.buildingBeingPlaced = buildingType
    data.temporaryBuilding = data.Building(-1000, -1000, data.buildingBeingPlaced)
    data.temporaryBuilding.add()

def showSettings():
    global doneButton
    createNotification(["Much is waiting", "to be done"])
    doneButton = Button(data.cWidth / 2 - 46, data.cHeight * (1 / data.notificationScreenBorderY - 1) * data.notificationScreenBorderY - 60, "Done", 2, doneReading)
##    data.resolution = 4
##    data.reload(sprites)

def showMenu():
    global menuButton, nextSeasonButton, menuScroller, backButton
    data.menuOpen = True
    menuButton.destroy()
    nextSeasonButton.destroy()
    for i in range(data.numOfMenuPanels):
        data.menuPanelObjects[i] = SelectablePanel(data.cWidth - 189, i * 100 + 10, data.cWidth - 17, (i + 1) * 100, buyPanelFunctions, buyPanelGraphics, pressedExtraArgs = (data.constructableBuildings[min(i, 3)],), graphicsExtraArgs = (data.constructableBuildings[min(i, 3)], 1.5), icon = [True, data.buildingTypeImages[data.constructableBuildings[min(i, 3)]], 3])
    data.menuFeatures.append(redrawMenu(0))
    menuScroller = Scroller(data.cWidth - 10, 10, 5, data.cHeight - 72, data.numOfMenuPanels * 90 + 20, data.scrollerPixelSize, redrawMenu)
    backButton = Button(data.cWidth - 104, data. cHeight - 42, "Back", 2, closeMenu)
    updateButtons()
    data.s.update()

def closeMenu():
    global menuButton, nextSeasonButton, menuScroller, backButton
    data.menuOpen = False
    menuButton = Button(data.cWidth - 110, 10, "Menu", 2, showMenu)
    nextSeasonButton = Button(data.cWidth - 200, data. cHeight - 42, "Next Season", 2, passTurn)
    for i in range(len(data.menuFeatures)):
        for j in range(len(data.menuFeatures[i])):
            if isinstance(data.menuFeatures[i][j], list):
                for k in range(len(data.menuFeatures[i][j])):
                    data.s.delete(data.menuFeatures[i][j][k])
            else:
                data.s.delete(data.menuFeatures[i][j])
    for i in range(data.numOfMenuPanels):
        data.menuPanelObjects[i].destroy()
    menuScroller.destroy()
    backButton.destroy()
    data.menuIndex = 0
    updateButtons()
    data.s.update()

def redrawMenu(index):
    data.menuIndex = index
    for i in range(len(data.menuFeatures)):
        for j in range(len(data.menuFeatures[i])):
            if isinstance(data.menuFeatures[i][j], list):
                for k in range(len(data.menuFeatures[i][j])):
                    data.s.delete(data.menuFeatures[i][j][k])
            else:
                data.s.delete(data.menuFeatures[i][j])
    data.menuFeatures = []
    data.menuFeatures.append([data.s.create_rectangle(data.cWidth - 200, 1, data.cWidth + 1, data.cHeight + 1, fill = "#d7d7d7", outline = "#7f7f7f", width = 3)])
    for i in range(data.numOfMenuPanels):
        if i * 100 + 10 - data.menuIndex > data.cHeight - 52:
            break
        if (i + 1) * 100 - data.menuIndex >= -1:
            data.menuFeatures.append([data.s.create_rectangle(data.cWidth - 190, i * 100 + 10 - data.menuIndex, data.cWidth - 17, (i + 1) * 100 - data.menuIndex, fill = "#d7d7d7", outline = "#7f7f7f", width = 3)])
            data.menuPanelObjects[i].delete()
            data.menuPanelObjects[i].displayPanel(data.cWidth - 189, i * 100 + 11 - data.menuIndex, data.cWidth - 18, (i + 1) * 100 - data.menuIndex - 1)
            data.menuFeatures.append([data.s.create_rectangle(data.cWidth - 200, data.cHeight - 52, data.cWidth, data.cHeight + 1, fill = "#d7d7d7", outline = "#7f7f7f", width = 3)])
    updateButtons()

def placeDownBuilding():
    data.placingDownBuilding = False

def doneReading():
    global doneButton
    deleteNotification()
    doneButton.destroy()

def passTurn():
    global doneButton
    data.seasonNumber += 1
    for i in range(len(data.seasonIndicator)):
        data.s.delete(data.seasonIndicator[i])
    data.seasonIndicator = createText(data.cWidth / 2 - 100, 10, "Season " + str(data.seasonNumber), 2, addColour = [True, data.seasonTextHighlightColour, 50])
    addResource([data.QALS, data.WOOD, data.GOLD, data.MANA], [data.qalsEconomy, data.woodEconomy, data.goldEconomy, data.manaEconomy])
    createNotification(["You collected", str(data.qalsEconomy) + " " + data.QALS, str(data.woodEconomy) + " " + data.WOOD, str(data.goldEconomy) + " " + data.GOLD, str(data.manaEconomy) + " " + data.MANA])
    doneButton = Button(data.cWidth / 2 - 46, data.cHeight * (1 / data.notificationScreenBorderY - 1) * data.notificationScreenBorderY - 60, "Done", 2, doneReading)

def tutorial():
    ##
    ##
    ##
    pass

def drawBuildingIcon(x, y, building, size):
    pixels = []
    pixels.append(makeBitmap(x, y, size, data.buildingTypeImages[building]))
    return pixels

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
    alreadyPressedSomething = False
    data.clickedXMouse = event.x
    data.clickedYMouse = event.y
    data.previousCurrentX = data.currentX
    data.previousCurrentY = data.currentY
    for i in range(len(Button.buttonBounds)):
        if alreadyPressedSomething == True:
            break
        try: #This try except is for when a button aside from the one clicked is deleted within its function.
            if Button.buttonBounds[i][0] <= data.clickedXMouse <= Button.buttonBounds[i][2] and Button.buttonBounds[i][1] <= data.clickedYMouse <= Button.buttonBounds[i][3]:
                data.clickedButton = True
                Button.buttonFunctions[i]() #This runs the assigned function or procedure call
                alreadyPressedSomething = True
        except:
            pass
    for i in range(len(Scroller.scrollerBounds)):
        if alreadyPressedSomething == True:
            break
        if Scroller.scrollerBounds[i][0] <= data.clickedXMouse <= Scroller.scrollerBounds[i][2] and Scroller.scrollerBounds[i][1] <= data.clickedYMouse <= Scroller.scrollerBounds[i][3]:
            data.clickedScroller = True
            Scroller.scrollerObject[i].clickedScroller = True
            Scroller.scrollerObject[i].scrolledOriginalPercentage = Scroller.scrollerObject[i].scrolledPercentage
            Scroller.scrollerObject[i].clickedY = event.y - Scroller.scrollerObject[i].y
            alreadyPressedSomething = True
    for i in range(len(SelectablePanel.panelBounds)):
        if alreadyPressedSomething == True:
            break
        try: #Same reason as button's -- See above.
            if SelectablePanel.panelBounds[i][0] <= data.clickedXMouse <= SelectablePanel.panelBounds[i][2] and SelectablePanel.panelBounds[i][1] <= data.clickedYMouse <= SelectablePanel.panelBounds[i][3]:
                SelectablePanel.panelFunctions[i](*SelectablePanel.panelObject[i].pressedExtraArgs) #Run whatever it is that is assigned
                alreadyPressedSomething = True
        except:
            pass

def mouseMotionDetector(event):
    if data.placingDownBuilding == True:
        tileHoverX, tileHoverY = getTile(event.x, event.y)
        if data.gameStarted == True and 0 <= tileHoverX < data.xTiles and 0 <= tileHoverY < data.yTiles and data.menuOpen == False:
            data.temporaryBuilding.x = tileHoverX
            data.temporaryBuilding.y = tileHoverY
            data.temporaryBuilding.deleteBuilding()
            data.temporaryBuilding.destroy()
            data.temporaryBuilding.add()
            updateScreen()
            data.highlightedTile = [tileHoverX, tileHoverY]
            highlightSquare(data.highlightedTile[0], data.highlightedTile[1])
            print(tileHoverX, data.temporaryBuilding.x, tileHoverY, data.temporaryBuilding.y)

def mouseDragDetector(event):
    data.mouseDragged = True
    if data.gameStarted == True and data.clickedButton == False and data.menuOpen == False and data.notificationOpen == False:
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
        scroller.scrolledPercentage = scroller.scrolledOriginalPercentage + float(scroller.draggedY) / float(scroller.scrollableLength) * 100
        if scroller.scrolledPercentage < 0:
            scroller.scrolledPercentage = 0
        if scroller.scrolledPercentage > 100:
            scroller.scrolledPercentage = 100
        scroller.deleteScroller()
        scroller.displayScroller()
        data.s.update()
        data.scrollerUpdated = True

def mouseReleaseDetector(event):
    global menuScroller
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
        if data.menuOpen == True and event.x < data.cWidth - 199 or data.menuOpen == False:
            tileClickedX, tileClickedY = getTile(data.clickedXMouse, data.clickedYMouse)
            if 0 <= tileClickedX < data.xTiles and 0 <= tileClickedY < data.yTiles:
                if data.highlightedTile != [tileClickedX, tileClickedY]:
                    highlightSquare(tileClickedX, tileClickedY)
                    menuOpenOriginal = data.menuOpen
                    data.menuOpen = False
                    updateScreen()
                    if menuOpenOriginal == True:
                        redrawMenu(data.menuIndex)
                        menuScroller.deleteScroller()
                        menuScroller.displayScroller()
                    data.menuOpen = menuOpenOriginal
                else:
                    data.highlightedTile = [-1000, -1000]
    if data.mouseDragged == False and data.clickedButton == False:
        placeDownBuilding()
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

        data.currentX = (data.currentX + data.cWidth / 2) / oldPolygonLandXLength * newPolygonLandXLength - data.cWidth / 2
        data.currentY = (data.currentY + data.cHeight / 2) / oldPolygonLandYLength * newPolygonLandYLength - data.cHeight / 2

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
    highlightX1 = landShapeTopX + ((x - y) / 2.0) * tileXLength #x1 y1 is the top corner
    highlightY1 = landShapeTopY + ((x + y) / 2.0) * tileYLength
    if highlightX1 > -tileXLength * data.loadBuffer and highlightX1 < data.cWidth + tileXLength * data.loadBuffer and highlightY1 > -tileYLength * data.loadBuffer and highlightY1 < data.cHeight + tileYLength * data.loadBuffer:
        highlightX2 = highlightX1 + tileXLength / 2
        highlightY2 = highlightY1 + tileYLength / 2
        highlightX3 = highlightX1
        highlightY3 = highlightY2 + tileYLength / 2
        highlightX4 = highlightX1 - tileXLength / 2
        highlightY4 = highlightY2
        data.highlightedTileObject = data.s.create_polygon(highlightX1, highlightY1, highlightX2, highlightY2, highlightX3, highlightY3, highlightX4, highlightY4, width = 0, fill = "yellow", stipple = "gray50")

def getTile(mouseX, mouseY):
    polygonLandXLength, polygonLandYLength = getLandPolygonXYLength()
    tileXLength, tileYLength = getTileXYLength()
    landClickedX = mouseX + data.currentX
    landClickedY = mouseY + data.currentY
    xB = landClickedY + landClickedX / 2 - polygonLandYLength / 2
    yB = -(landClickedY - landClickedX / 2 - polygonLandYLength / 2)
    tileOnX = int(xB / tileYLength)
    tileOnY = data.yTiles - int(yB / tileYLength) - 1
    return tileOnX, tileOnY

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
            squareSize = tileXLength/len(bitmapImage[0])

            data.Building.buildingImages[i] = makeBitmap(buildingX4, buildingY3 - squareSize*len(bitmapImage), squareSize, bitmapImage, toBack = True)

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
        #Top Left x1 y1, Bottom Right x2 y2
        data.resourceObjects.append([data.s.create_rectangle(10, data.cHeight - (len(data.resourceTypes) - i) * 30, 10 + data.resourceIndicatorLength * ratioOfResourceToMaximum, data.cHeight - 10 - (len(data.resourceTypes) - 1 - i) * 30, fill = data.resourceColours[resource])])
        data.resourceObjects.append(makeBitmap(8, data.cHeight - 3 - (len(data.resourceTypes) - i) * 30, 2, data.resourceIcons[resource]))
        data.resourceObjects.append(createText(40, data.cHeight - (len(data.resourceTypes) - i) * 30 + 4, str(data.resourceAmounts[resource]), data.resourceTextSize, addColour = [True, data.resourceColours[resource], 80]))

def updateScreen():
    if data.menuOpen == False and data.notificationOpen == False:
        highlightSquare(data.highlightedTile[0], data.highlightedTile[1])
        updateBuildings()
        updateLand()

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
    scrollerFunctions = [] #Array stores each page that the scroller is assigned to

    topBitmapImage = data.scrollerSegments[data.SCROLLER_TOP]
    bottomBitmapImage = data.scrollerSegments[data.SCROLLER_BOTTOM]

    def __init__(self, scrollerX, scrollerY, scrollerWidth, scrollerHeight, displayedActualHeight, scrollerPixelSize, function):
        self.number = len(Scroller.scrollerObject)
        self.x = scrollerX
        self.y = scrollerY
        self.pixelSize = float(scrollerPixelSize)
        self.scrollerWidth = scrollerWidth
        self.scrollerHeight = scrollerHeight #Scroller height is the entire thing's height
        self.actualHeight = displayedActualHeight
        self.scrolledPercentage = 0
        self.scrolledOriginalPercentage = 0
        self.scrollerXValue = self.x - (len(data.scrollerSegments[data.SCROLLER_MIDDLE_0][0]) * self.pixelSize - self.scrollerWidth) / 2
        self.clickedY = 0
        self.draggedY = 0
        self.clickedScroller = False
        self.actualDisplayIndex = 0

        Scroller.scrollerObject.append(self)
        Scroller.scrollerFunctions.append(function)
        Scroller.scrollerSegments.append([])
        Scroller.scrollerPixels.append([])

        Scroller.scrollerPixels[self.number].append([data.s.create_rectangle(self.x, self.y, self.x + self.scrollerWidth, self.y + self.scrollerHeight, fill = "#7f7f7f", width = 0)])
        fractionOfActualThatsSeen = (self.scrollerHeight + 20.0) / self.actualHeight

        #The size of the tab
        self.scrollerTabSize = fractionOfActualThatsSeen * self.scrollerHeight
        #How much you can actually scroll
        self.scrollableLength = self.scrollerHeight - self.scrollerTabSize

        #The top and bottom segments are additional to the actual scrolling part, which are the middle segments
        Scroller.scrollerPixels[self.number].append(makeBitmap(self.scrollerXValue, self.y - len(Scroller.topBitmapImage) * self.pixelSize, self.pixelSize, Scroller.topBitmapImage))

        Scroller.scrollerPixels[self.number].append(makeBitmap(self.scrollerXValue, self.y + self.scrollerTabSize, self.pixelSize, Scroller.bottomBitmapImage))

        #These segments actually show where the thing is
        for i in range(int(self.y), self.y + int(self.scrollerTabSize), int(len(data.scrollerSegments[data.SCROLLER_MIDDLE_0]) * self.pixelSize)):
            randomSegmentNumber = randint(0, len(data.scrollerSegments) - 3)
            Scroller.scrollerSegments[self.number].append(randomSegmentNumber)
            bitmapImage = data.scrollerSegments[data.SCROLLER_MIDDLE_TEMPLATE + str(randomSegmentNumber)]
            Scroller.scrollerPixels[self.number].append(makeBitmap(self.scrollerXValue, i, self.pixelSize, bitmapImage))

        Scroller.scrollerBounds.append([self.scrollerXValue, self.y - len(Scroller.topBitmapImage) * self.pixelSize, self.scrollerXValue + len(data.scrollerSegments[data.SCROLLER_MIDDLE_0][0]) * self.pixelSize, self.y + self.scrollerTabSize + len(Scroller.bottomBitmapImage) * self.pixelSize])

    def displayScroller(self):
        yIndex = self.scrolledPercentage / 100.0 * self.scrollableLength
        self.actualDisplayIndex = self.scrolledPercentage / 100 * (self.actualHeight - self.scrollerHeight + 20)

        Scroller.scrollerFunctions[self.number](self.actualDisplayIndex)

        Scroller.scrollerPixels[self.number].append([data.s.create_rectangle(self.x, self.y, self.x + self.scrollerWidth, self.y + self.scrollerHeight, fill = "#7f7f7f", width = 0)])
        Scroller.scrollerPixels[self.number][1] = makeBitmap(self.scrollerXValue, self.y - len(Scroller.topBitmapImage) * self.pixelSize + yIndex, self.pixelSize, Scroller.topBitmapImage)
        Scroller.scrollerPixels[self.number][2] = makeBitmap(self.scrollerXValue, self.y + self.scrollerTabSize + yIndex, self.pixelSize, Scroller.bottomBitmapImage)

        segmentIndex = 0
        for i in range(len(Scroller.scrollerSegments[self.number])):
            segmentNumber = Scroller.scrollerSegments[self.number][i]
            bitmapImage = data.scrollerSegments[data.SCROLLER_MIDDLE_TEMPLATE + str(segmentNumber)]
            Scroller.scrollerPixels[self.number][3 + segmentIndex] = makeBitmap(self.scrollerXValue, self.y + i * self.pixelSize + yIndex, self.pixelSize, bitmapImage)
            segmentIndex += 1

        Scroller.scrollerBounds[self.number] = [self.scrollerXValue, self.y - len(Scroller.topBitmapImage) * self.pixelSize + yIndex, self.scrollerXValue + len(data.scrollerSegments[data.SCROLLER_MIDDLE_0][0]) * self.pixelSize, self.y + self.scrollerTabSize + len(Scroller.bottomBitmapImage) * self.pixelSize + yIndex]

    def deleteScroller(self): #For updating the screen
        for i in range(len(Scroller.scrollerPixels[self.number])):
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

#Selectable Panel Class
class SelectablePanel():
    panelObject = [] #Stores every panel object
    panelPixels = [] #This stores the entire scope of panels and each of their pixels
                 #3D array --> the primary array stores each panel
                 #         --> the secondary array stores each component of said panel
                 #         --> the tertiary array stores each pixels of component
    panelBounds = [] #This stores the boudaries of each panel.
                      #Used in the mouse click function
    panelFunctions = [] #Stores the function called when clicked

    def __init__(self, panelX1, panelY1, panelX2, panelY2, pressedFunction, graphicsFunction, pressedExtraArgs = (), graphicsExtraArgs = (), icon = [False, "", 0]):
        self.number = len(SelectablePanel.panelObject)
        self.x1 = panelX1
        self.y1 = panelY1
        self.x2 = panelX2
        self.y2 = panelY2
        self.graphics = graphicsFunction
        self.hasIcon = False

        SelectablePanel.panelObject.append(self)
        SelectablePanel.panelPixels.append([])
        SelectablePanel.panelBounds.append([self.x1, self.y1, self.x2, self.y2])
        SelectablePanel.panelFunctions.append(pressedFunction)
        self.graphicsExtraArgs = graphicsExtraArgs
        self.pressedExtraArgs = pressedExtraArgs
        
        SelectablePanel.panelPixels[self.number].append([data.s.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = data.buildingPanelColour)])
        SelectablePanel.panelPixels[self.number].append(self.graphics(self.x1, self.y1, self.x2, self.y2, *self.graphicsExtraArgs))
        if icon[0] == True:
            self.hasIcon = True
            self.bitmapImage = icon[1]
            self.pixelSize = icon[2]
            SelectablePanel.panelPixels[self.number].append(makeBitmap((self.x2 + self.x1 - len(self.bitmapImage[0]) * self.pixelSize) / 2, self.y1 + 2 * (self.y2 - self.y1) / 5 - len(self.bitmapImage) * self.pixelSize / 2, self.pixelSize, self.bitmapImage))
        
    def displayPanel(self, panelX1, panelY1, panelX2, panelY2):
        self.x1 = panelX1
        self.y1 = panelY1
        self.x2 = panelX2
        self.y2 = panelY2
        SelectablePanel.panelBounds[self.number] = [self.x1, self.y1, self.x2, self.y2]
        SelectablePanel.panelPixels[self.number][0] = [data.s.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = data.buildingPanelColour)]
        SelectablePanel.panelPixels[self.number][1] = self.graphics(self.x1, self.y1, self.x2, self.y2, *self.graphicsExtraArgs)
        if self.hasIcon == True:
            SelectablePanel.panelPixels[self.number][2] = (makeBitmap((self.x2 + self.x1 - len(self.bitmapImage[0]) * self.pixelSize) / 2, self.y1 + 2 * (self.y2 - self.y1) / 5 - len(self.bitmapImage) * self.pixelSize / 2, self.pixelSize, self.bitmapImage))


    def delete(self): #For updating the screen
        for i in range(len(SelectablePanel.panelPixels[self.number])):
            for j in range(len(SelectablePanel.panelPixels[self.number][i])):
                data.s.delete(SelectablePanel.panelPixels[self.number][i][j])

    def destroy(self):
        try: #Try to delete everything if it hasn't already been deleted
            for i in range(len(SelectablePanel.panelPixels[self.number])):
                for j in range(len(SelectablePanel.panelPixels[self.number][i])):
                    data.s.delete(SelectablePanel.panelPixels[self.number][i][j])
        except:
            pass
        #Then delete all the data
        del SelectablePanel.panelBounds[self.number]    #Delete the bounds check
        del SelectablePanel.panelPixels[self.number]         #Delete the pixels STORER
        del SelectablePanel.panelFunctions[self.number] #Delete the function
        del SelectablePanel.panelObject[self.number]    #Delete the object HOLDER
        for i in range(self.number, len(SelectablePanel.panelObject)):
            SelectablePanel.panelObject[i].number -= 1          #Reduce all numbers of following panels by 1 to fill up the gap.
