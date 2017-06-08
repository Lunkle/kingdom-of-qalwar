from tkinter import *
import CivilizationGameSprites as sprites
import CivilizationGameFont as font

#Changeable Colours:
landColour = "#56b000"

#Changeable Sizes:
cWidth = 800
cHeight = 600

xTiles = 40
yTiles = 40

panLimitFactor = 1.05
panLimitSpeed = 0.5

minTileSize = 15
maxTileSize = 250

#For the Button class
startScreenButtonSize = 2.0
buttonLetterSpacing = 0

startingTileSize = (minTileSize + maxTileSize) / 4

#Recommended-to-not-Change Variables:
townHallStartingX = xTiles/4 - 1
townHallStartingY = 3*yTiles/4 - 1

enemyBaseStartingX = 3 * xTiles/4 - 1
enemyBaseStartingX = yTiles/4 - 1

loadBuffer = 2 #In tiles

#Lame Variables:
gameStarted = False
gameOver = False

landPolygon = 0

tileSize = startingTileSize

currentX = (tileSize * xTiles * 2 ** 0.5 )/2 - cWidth/2
currentY = (tileSize * yTiles * 2 ** 0.5 )/4 - cHeight/2

previousCurrentX = currentX
previousCurrentY = currentY

clickedXMouse = currentX
clickedYMouse = currentY

previousXMouse = currentX
previousYMouse = currentY

xMouseClickedAt = currentX
yMouseClickedAt = currentY

xMouseReleasedAt = currentX
yMouseReleasedAt = currentY

panSlipX = 0 ## Maybe delete this
panSlipY = 0 ## Maybe delete this as well


BUTTON_LEFT = "ButtonLeft"
BUTTON_MIDDLE_TEMPLATE = "ButtonMiddle"
BUTTON_MIDDLE_0 = "ButtonMiddle0"
BUTTON_MIDDLE_1 = "ButtonMiddle1"
BUTTON_MIDDLE_2 = "ButtonMiddle2"
BUTTON_RIGHT = "ButtonRight"

TOWN_HALL_TOP = "TownHallTop"
TOWN_HALL_LEFT = "TownHallLeft"
TOWN_HALL_RIGHT = "TownHallRight"
TOWN_HALL_BOTTOM = "TownHallBotttom"
RESIDENCE = "Residence"

root = Tk()
root.resizable(False, False) #Set resizable to false
s = Canvas(root, width=cWidth, height=cHeight, background = "white")
s.master.title("Kingdom of Qalwar") #Yey  what a cool name

gameFontDictionary = {
    "a":font.letterA,
    "b":font.letterB,
    "c":font.letterC,
    "d":font.letterD,
    "e":font.letterE,
    "f":font.letterF,
    "g":font.letterG,
    "h":font.letterH,
    "i":font.letterI,
    "j":font.letterJ,
    "k":font.letterK,
    "l":font.letterL,
    "m":font.letterM,
    "n":font.letterN,
    "o":font.letterO,
    "p":font.letterP,
    "q":font.letterQ,
    "r":font.letterR,
    "s":font.letterS,
    "t":font.letterT,
    "u":font.letterU,
    "v":font.letterV,
    "w":font.letterW,
    "x":font.letterX,
    "y":font.letterY,
    "z":font.letterZ,
    "A":font.letterA,
    "B":font.letterB,
    "C":font.letterC,
    "D":font.letterD,
    "E":font.letterE,
    "F":font.letterF,
    "G":font.letterG,
    "H":font.letterH,
    "I":font.letterI,
    "J":font.letterJ,
    "K":font.letterK,
    "L":font.letterL,
    "M":font.letterM,
    "N":font.letterN,
    "O":font.letterO,
    "P":font.letterP,
    "Q":font.letterQ,
    "R":font.letterR,
    "S":font.letterS,
    "T":font.letterT,
    "U":font.letterU,
    "V":font.letterV,
    "W":font.letterW,
    "X":font.letterX,
    "Y":font.letterY,
    "Z":font.letterZ
}

#Coolest stuff
class Building():
    buildings = []
    buildingImages = []
    buildingTypes = []
    buildingsX = []
    buildingsY = []
    
    def __init__(self, gridX, gridY, buildingType):
        self.x = gridX
        self.y = gridY
        self.type = buildingType
        self.number = len(Building.buildings)

    def add(self):
        Building.buildings.append(0)
        Building.buildingImages.append([])
        Building.buildingTypes.append(self.type)
        Building.buildingsX.append(self.x)
        Building.buildingsY.append(self.y)
        
    def destroy(self):
        del Building.buildings[self.number]
        del Building.buildingTypes[self.number]
        del Building.buildingsX[self.number]
        del Building.buildingsY[self.number]

#Image Data
buttonSegments = {
    BUTTON_LEFT:sprites.buttonLeft,
    BUTTON_MIDDLE_0:sprites.buttonMiddle0,
    BUTTON_MIDDLE_1:sprites.buttonMiddle1,
    BUTTON_MIDDLE_2:sprites.buttonMiddle2,
    BUTTON_RIGHT:sprites.buttonRight
}

buildingTypeImages = {
    TOWN_HALL_TOP:sprites.townHallTop,
    TOWN_HALL_LEFT:sprites.townHallLeft,
    TOWN_HALL_RIGHT:sprites.townHallRight,
    TOWN_HALL_BOTTOM:sprites.townHallBottom,
    ENEMY_BASE_TOP:sprites.enemyBaseTop,
    ENEMY_BASE_LEFT:sprites.enemyBaseLeft,
    ENEMY_BASE_RIGHT:sprites.enemyBaseRight,
    ENEMY_BASE_BOTTOM:sprites.enemyBaseBottom,
    RESIDENCE:sprites.residence
}

#buildingTypeSizes should always be less than 1 unless special situations occur
#This is for cosmetics only -- does not affect gameplay
buildingTypeSizes = {
    TOWN_HALL_TOP:1,
    TOWN_HALL_LEFT:1,
    TOWN_HALL_RIGHT:1,
    TOWN_HALL_BOTTOM:1,
    RESIDENCE:0.8
}
