from Tkinter import *
import PIL
from PIL import Image

#Changeable Colours:
landColour = "#56b000"

#Changeable Sizes:
cWidth = 500
cHeight = 500

xTiles = 40
yTiles = 40

panLimitFactor = 1.05
panLimitSpeed = 0.5

minTileSize = 15
maxTileSize = 250

startingTileSize = (minTileSize + maxTileSize) /2

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
residence = Image.open("Resources/Residence.png")
s.create_image(0, 0, residence)
s.update()
residence = Tkinter.PhotoImage(Image.open("Resources/Residence.png"))

buildingTypeImages = {
    RESIDENCE:residence
}
