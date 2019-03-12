from PIL import Image
#Deepcopy to copy 2d array
from copy import copy, deepcopy
import sys
import os


def brailleCheck(w, h):
    if lineGrid[w][h] == "X":
        return True 
    else:
        return False
                

def checkCol(w, h):
    colChange = False
    for p in range(w - thickness , w + thickness + 1):
        if p >= 0 and p < width:
           
            # Check to see if the numbers lie in the tolerance range. Numbers in this range are considerd to be the same colour
            if rGrid[w][h] - tolerance <= rGrid[p][h] <= rGrid[w][h] + tolerance and  gGrid[w][h] - tolerance <= gGrid[p][h] <= gGrid[w][h] + tolerance and  bGrid[w][h] - tolerance <= bGrid[p][h] <= bGrid[w][h] + tolerance:
                pass
            else:
                colChange = True

    for p in range(h - thickness , h + thickness + 1):
        if p >= 0 and p < height:

            if rGrid[w][h] - tolerance <= rGrid[w][p] <= rGrid[w][h] + tolerance and gGrid[w][h] - tolerance <= gGrid[w][p] <= gGrid[w][h] + tolerance and bGrid[w][h] - tolerance <= bGrid[w][p] <= bGrid[w][h] + tolerance:
                
                pass
            else:
                colChange = True
    return colChange


#imgToOpen = input("Image to Open: ")
if len(sys.argv) < 4:
    print("Usage {} /path/to/image [thickness] [tolerance]")
    sys.exit(1)


imgToOpen = sys.argv[1]

#how many tiles to check for a colour change
thickness = int(sys.argv[2]) 
#test param here
tolerance = int(sys.argv[3])

im = Image.open(imgToOpen)

rgb_im = im.convert("RGB")

width, height = im.size

# Get Terminal size in rows and cols
termRows, termCols= os.popen('stty size', 'r').read().split()
termRows = int(termRows)
termCols = int(termCols)

termOffsetX = 2
termOffsetY = 4
if width > termCols * 2:
    termOffsetX = 4
    print("offset 4")
    print(termCols * 2)
    print(width)
    termOffsetY = 8

rGrid = []
gGrid = []
bGrid = []

#Get RGB values of every pixel and form a grid

for w in range(width):
    
    rGrid.append([])
    gGrid.append([])
    bGrid.append([])

    for h in range(height):
    
        r, g, b = rgb_im.getpixel((w,h))
        rGrid[w].append(r)
        gGrid[w].append(g)
        bGrid[w].append(b)

#main logic with correct cords

#Line array creates lines by viewing relative colours on vert and hor
lineGrid = deepcopy(rGrid)


for h in range(height):
    for w in range(width):
        if checkCol(w,h):
            lineGrid[w][h] = "X"
        else:
            lineGrid[w][h] = " "
            
#Output Braille
BRAILLE_OFFSET = 0x2800

#Converting to braille skiping some pixels to make the image fit the screen

bOutput = []
for y in range(0, int(height / termOffsetY) * termOffsetY, termOffsetY):
    for x in range(0, int(width / termOffsetX) * termOffsetX, termOffsetX):

        p1 = brailleCheck(x,y)
        p2 = brailleCheck(x, y + 1)
        p3 = brailleCheck(x, y + 2)
        p4 = brailleCheck(x + 1, y)
        p5 = brailleCheck(x + 1, y + 1)
        p6 = brailleCheck(x + 1, y + 2)
        p7 = brailleCheck(x, y + 3)
        p8 = brailleCheck(x + 1, y + 3)
        n = 0

        n |= int(p1)
        n |= int(p2) << 1
        n |= int(p3) << 2
        n |= int(p4) << 3 
        n |= int(p5) << 4 
        n |= int(p6) << 5 
        n |= int(p7) << 6
        n |= int(p8) << 7

        bOutput.append(chr(BRAILLE_OFFSET + n))
    bOutput.append("\n")
print("".join(bOutput))
