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
data.s.bind("<ButtonRelease-1>", mouseReleaseDetector)
data.s.bind("<MouseWheel>", mouseWheelHandler)
data.s.pack()

data.s.update()

frame = 0
##while data.gameStarted == False:
##    pass

init()
while data.gameOver == False:
##for i in range(100):
    updateLand()
    data.s.update()
    sleep(0.01)
mainloop()
