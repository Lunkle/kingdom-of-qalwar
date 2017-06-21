from time import sleep
from random import randint
import random
import colorsys
import CivilizationGameData as data
from CivilizationGameFunctions import *

data.s.focus_set()
data.s.bind("<Key>", keyPressDetector)
data.s.bind("<KeyRelease>", keyReleaseDetector)
data.s.bind("<Button-1>", mousePressedDetector)
data.s.bind("<B1-Motion>", mouseDragDetector)
data.s.bind('<Motion>', mouseMotion)
data.s.bind("<ButtonRelease-1>", mouseReleaseDetector)
data.s.bind("<MouseWheel>", mouseWheelHandler)
data.s.pack()

data.s.update()


showStartPage()
#On the start page the start button will start the game

while data.gameStarted == False:
    data.s.update()#While the start button is not pressed, keep on updating

initializeGame() #When game starts, initialize the game

tutorial() #Currently has nothing, but might be added later

while data.gameOver == False:
    updateScreen() #Updates game screen (land, buildings, higlighted tile, etc.)
    data.s.update()
    sleep(0.01)

mainloop()
