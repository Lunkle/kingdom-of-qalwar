from PIL import Image
im = Image.open("Paper Down.png") #Can be many different formats.
pix = im.load()
xLength, yLength = im.size #Get the width and hight of the image for iterating over
##print pix[50, 50] #Get the RGBA Value of the a pixel of an image
##pix[50, 50] = 255,  0,  0 # Set the RGBA Value of the image (tuple)
##im.save("alive_parrot.png") # Save the modified pixels as png

##imageArray = []
##colours = ["#ffffff"]
##for i in range(yLength):
##    imageArray.append([])
##    for j in range(xLength):
##        r, g, b = pix[j, i]
##        hexCode = "#%02x%02x%02x" % (r, g, b)
##        if hexCode not in colours:
##            colours.append(hexCode)
##        if hexCode == "#ffffff":
##            imageArray[i].append( 0)
##        else:
##            imageArray[i].append(colours.index(hexCode) + 9)

imageArray = []
for i in range(yLength):
    imageArray.append([])
    for j in range(xLength):
        r, g, b, a = pix[j, i]
        hexCode = "#%02x%02x%02x" % (r, g, b)
        imageArray[i].append(hexCode)

for i in range(1, len(imageArray)):
    for j in range(len(imageArray[i]) - 1, -1, -1):
        if imageArray[i][j] == "#ffffff":
            del imageArray[i][j]
        else:
            break

print " = ["
for i in imageArray:    
    print('    ' + str(i) + ",")
print "]"
##print(imageArray)


##colours = ['#ffffff', '#512900', '#626262', '#353535', '#444444', '#535353', '#4f0000', '#bd4444', '#9f2626', '#810808', '#808080', '#835b2e', '#744c1f', '#a1794c', '#556d9b', '#738bb9', '#926a3d', '#91a9d7', '#a9afb4', '#ddb588', '#bf976a', '#013e00', '#6fac51', '#518e33', '#ded914', '#337015']
##
##for i in range(len(colours)):
##    print 'elif colourCode == ' + str(i + 9) + ':'
##    print '\tcolour = "' + colours[i] + '"'
>>>>>>> 65026c78443ed0bf77da7ed62560ed06460bca28
