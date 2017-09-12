from Tkinter import *

resolution = 3 #Change to higher for faster game
               #Must be a whole number

import CivilizationGameSprites as sprites
import CivilizationGameFont as font

#Changeable Colours ////////////////////////////////////////////////////////////
landColour = "#56b000"
landOutlineColour = "#6bdb00"
allyOutlineColour = "#8df100"
allyAreaColour = "#74d400"
enemyOutlineColour = "#b72000"
enemyAreaColour = "#965000"
neutralOutlineColour = "#656d5d"
neutralAreaColour = "#627a4a"
seasonTextHighlightColour = "#128000"
dirtColour = "#b08257"
dirtOutlineColour = "#cdaf94"

buildingPanelColour = "#e1e7e9"

#Changeable Sizes ////////////////////////////////////////////////////////////
cWidth = 600
cHeight = 400

xTiles = 32
yTiles = 32

panLimitFactor = 1.05
panLimitSpeed = 0.5

minTileSize = 15
maxTileSize = 250

dirtThickness = 1.5

notificationPixelSize = 3
notificationScreenBorderX = 1.0/6.0 #The smaller these are (or bigger the denominator)
notificationScreenBorderY = 1.0/6.0 #the smaller the border and bigger the notification
notificationTextSize = 2

startingQalsEconomy = 10    #Economy is the amount of each resource
startingWoodEconomy = 10    #the player gains each week
startingGoldEconomy = 2     #This can be increaesed through
startingManaEconomy = 5     #building and upgrading buildings.

#For the Button class ////////////////////////////////////////////////////////////
startScreenButtonSize = 2.5
buttonLetterSpacing = 0

#For the Scroller ////////////////////////////////////////////////////////////
scrollerPixelSize = 3
scrollerUpdated = True

#Recommended-to-not-Change Variables ////////////////////////////////////////////////////////////
menuFeatures = []
numOfMenuPanels = 4
menuIndex = 0
menuPanelObjects = [0] * numOfMenuPanels

startingTileSize = 30

townHallStartingX = xTiles/4 - 1
townHallStartingY = 3*yTiles/4 - 1

enemyBaseStartingX = 3 * xTiles/4 - 1
enemyBaseStartingY = yTiles/4 - 1

loadBuffer = 0 #In tiles

resourceIndicatorLength = 2 * cWidth / 5 - 10
resourceTextSize = 2

#Lame Variables ////////////////////////////////////////////////////////////
gameStarted = False
menuOpen = False
gameOver = False
placingDownBuilding = False #Should start at False
temporaryBuilding = 0 #Holds the building class instance
buildingBeingPlaced = ""

landPolygon = 0 #Stores land object
dirtLeft = 0    #Stores left dirt object
dirtRight = 0   #Stores right dirt object

seasonNumber = 1
seasonIndicator = 0

notificationOpen = False
notificationPage = []

highlightedTile = [-1000, -1000] #Set it off the screen
highlightedTileObject = 0

resourceObjects = [[]]

tileSize = startingTileSize

currentX = (tileSize * xTiles * 2 ** 0.5 )/2 - cWidth/2
currentY = (tileSize * yTiles * 2 ** 0.5 )/4 - cHeight/2

mouseDragged = False
clickedButton = False
clickedScroller = False

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

SCROLLER_TOP = "ScrollerTop"
SCROLLER_MIDDLE_TEMPLATE = "ScrollerMiddle"
SCROLLER_MIDDLE_0 = "ScrollerMiddle0"
SCROLLER_MIDDLE_1 = "ScrollerMiddle1"
SCROLLER_MIDDLE_2 = "ScrollerMiddle2"
SCROLLER_BOTTOM = "ScrollerBottom"

TOWN_HALL_TOP = "TownHallTop"
TOWN_HALL_LEFT = "TownHallLeft"
TOWN_HALL_RIGHT = "TownHallRight"
TOWN_HALL_BOTTOM = "TownHallBotttom"

ENEMY_BASE_TOP = "EnemyBaseTop"
ENEMY_BASE_LEFT = "EnemyBaseLeft"
ENEMY_BASE_RIGHT = "EnemyBaseRight"
ENEMY_BASE_BOTTOM = "EnemyBaseBotttom"

RESIDENCE = "Residence"
TEEPEE = "Teepee"
BARRACKS = "Barracks"
LUMBER_HOUSE = "LumberHouse"
OPEN_LAND = "OpenLand"

root = Tk()
root.resizable(False, False) #Set resizable to false
s = Canvas(root, width=cWidth, height=cHeight, background = "white")
s.master.title("Kingdom of Qalwar") #Yey  what a cool name

QALS = "Qal"
WOOD = "Wood"
GOLD = "Gold"
MANA = "Mana"

resourceTypes = [
    QALS,
    WOOD,
    GOLD,
    MANA
]

resourceAmounts = {
    QALS:500,
    WOOD:500,
    GOLD:100,
    MANA:100
}

resourceMaximum = {
    QALS:1000,
    WOOD:1000,
    GOLD:250,
    MANA:100
}

economy = {
    QALS:startingQalsEconomy,
    WOOD:startingWoodEconomy,
    GOLD:startingGoldEconomy,
    MANA:startingManaEconomy
}

resourceColours = {
    QALS:"#ca5c37",
    WOOD:"#a07b54",
    GOLD:"#e5c100",
    MANA:"#02bfd2"
}

#Image Data ////////////////////////////////////////////////////////////
resourceIcons = {
    QALS:sprites.qals,
    WOOD:sprites.wood,
    GOLD:sprites.gold,
    MANA:sprites.mana
}

buttonSegments = {
    BUTTON_LEFT:sprites.buttonLeft,
    BUTTON_MIDDLE_0:sprites.buttonMiddle0,
    BUTTON_MIDDLE_1:sprites.buttonMiddle1,
    BUTTON_MIDDLE_2:sprites.buttonMiddle2,
    BUTTON_RIGHT:sprites.buttonRight
}

scrollerSegments = {
    SCROLLER_TOP:sprites.scrollerTop,
    SCROLLER_MIDDLE_0:sprites.scrollerMiddle0,
    SCROLLER_MIDDLE_1:sprites.scrollerMiddle1,
    SCROLLER_MIDDLE_2:sprites.scrollerMiddle2,
    SCROLLER_BOTTOM:sprites.scrollerBottom
}

PAPER_TOP_LEFT = "PaperTopLeft"
PAPER_TOP_RIGHT = "PaperTopRight"
PAPER_BOTTOM_LEFT = "PaperBottomLeft"
PAPER_BOTTOM_RIGHT = "PaperBottomRight"
PAPER_UP = "PaperUp"
PAPER_LEFT = "PaperLeft"
PAPER_RIGHT = "PaperRight"
PAPER_DOWN = "PaperDown"
PAPER_MIDDLE = "PaperMiddle"

paperPieces = {
    PAPER_TOP_LEFT:sprites.paperTopLeft,
    PAPER_TOP_RIGHT:sprites.paperTopRight,
    PAPER_BOTTOM_LEFT:sprites.paperBottomLeft,
    PAPER_BOTTOM_RIGHT:sprites.paperBottomRight,
    PAPER_UP:sprites.paperUp,
    PAPER_LEFT:sprites.paperLeft,
    PAPER_RIGHT:sprites.paperRight,
    PAPER_DOWN:sprites.paperDown,
    PAPER_MIDDLE:sprites.paperMiddle
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
    OPEN_LAND:sprites.openLand,
    TEEPEE:sprites.teepee,
    RESIDENCE:sprites.residence,
    BARRACKS:sprites.barracks,
    LUMBER_HOUSE:sprites.lumberHouse
}

constructableBuildings = [
    RESIDENCE,
    TEEPEE,
    BARRACKS,
    LUMBER_HOUSE
]

buildingCosts = {
    RESIDENCE:[[QALS, WOOD], [100, 100], QALS, 5],
    BARRACKS:[[QALS, WOOD], [300, 50], GOLD, 1],
    LUMBER_HOUSE:[[QALS, WOOD], [50, 300], WOOD, 5],
    TEEPEE:[[QALS, WOOD], [200, 200], MANA, 2]
}

#Stored Data
ALLY = "Ally"
ENEMY = "Enemy"
NEUTRAL = "Neutral"

allianceHighlightObjects = []
allianceOutlineObjects = [0] * (xTiles * yTiles * 12 / 9)

#Stores each building of each alliance in form of [[gridX1, gridY1], [gridX2, gridY2]]
allianceDictionary = {ALLY:[], ENEMY:[], NEUTRAL:[]}

#[Area colours, outline colours]
allianceColours = {ALLY:[allyAreaColour, allyOutlineColour], ENEMY:[enemyAreaColour, enemyOutlineColour], NEUTRAL:[neutralAreaColour, neutralOutlineColour]}

#Coolest stuff ////////////////////////////////////////////////////////////
