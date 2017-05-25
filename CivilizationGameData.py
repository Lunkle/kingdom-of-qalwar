from Tkinter import *



#Changeable Colours:
landColour = "#56b000"

#Changeable Sizes:
cWidth = 500
cHeight = 500

xTiles = 500
yTiles = 500

startingTileSize = 5.0

panLimitFactor = 1.05
panLimitSpeed = 0.5

#Lame Variables
gameStarted = False
gameOver = False

landPolygon = 0

tileSize = startingTileSize

currentX = (tileSize * xTiles * 2 ** 0.5 )/6 - cWidth/2
currentY = (tileSize * yTiles * 2 ** 0.5 )/8 - cHeight/2

previousCurrentX = currentX
previousCurrentY = currentY

originalDragMouseX = currentX
originalDragMouseY = currentY

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

RESIDENCE = "Residence"

myInterface = Tk()

s = Canvas(myInterface, width=cWidth, height=cHeight, background = "white")
s.master.title("Civilization Game") #To Change


#Coolest stuff
class Building():
    buildings = []
    buildingsX = []
    buildingsY = []
    
    def __init__(self, gridX, gridY, buildingType):
        self.x = gridX
        self.y = gridY
        self.type = buildingType
        self.number = len(Building.buildings)

    def add(self):
        Building.buildings.append(self.type)
        Building.buildingsX.append(self.x)
        Building.buildingsY.append(self.y)
        
    def destroy(self):
        del Building.buildings[self.number]
        del Building.buildingsX[self.number]
        del Building.buildingsY[self.number]


