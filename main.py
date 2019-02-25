# -*- coding: utf-8 -*-
import pygame as pg  
import pdb
import re
from decimal import getcontext, Decimal
import math
import os
from pathlib import Path
import rgb 

def parseRelKeys(keyVal, myPath, screen, colors): 
    if keyVal == 'm' : os.startfile(myPath + "\\menu.txt")
    if keyVal == 'r' : rgb.rgbHome(screen, colors)
    return

def lengthOfLine (x1, x2, y1, y2, isInt): 
    if not isInt:
        return (((x2 - x1)**2 + (y2 - y1) ** 2)**(1/2))
    else: 
        return int(round(((x2 - x1)**2 + (y2 - y1) ** 2)**(1/2), 0))

def anglesUpdate (distances): 
    """
    LAW OF COSINES
    cos(C) =  a^2 + b^2 − c^2/2ab

    cos(A) =  b^2 + c^2 − a^2/2bc

    cos(B) =  c^2 + a^2 − b^2/2ca
    """
    abc = [0.01 if x == 0 else x for x in [distances["L1"], distances["L2"], distances["L3"]]]
    a, b, c = abc[0], abc[1], abc[2]
    angles = {}
    angles["L1-L2"] = math.acos((a ** 2 + b ** 2 - c ** 2)/(2 * a * b))
    angles["L2-L3"] = math.acos((c ** 2 + a ** 2 - b ** 2)/(2 * c * a))
    angles["L3-L1"] = math.acos((b ** 2 + c ** 2 - a ** 2)/(2 * b * c))
    return angles


myPath = str(Path().absolute())

pg.init() 
#pdb.set_trace()
sizeXY = [0,0]
while not (sizeXY[0] >= 300 and sizeXY[1] >= 300):
    sizeXY = [int(x) for x in input("Please enter the dimensions of the screen you want to use [min: 300, 300] (ex: 300,400): ").split(',')]

size = (sizeXY[0], sizeXY[1])
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
pg.display.set_caption('Triangles: Press \'m\' for menu')

done = True

colors = {"White": (255, 255, 255), "Black": (0,0,0), "Red": (255, 0, 0),"Green": (0,255,0), "Blue" : (0, 0, 255), "User Color": (0, 0, 0)}

#creating default X and Y values
midpoint = (size[0]/2, size[1]/2)
x = [midpoint[0], midpoint[1] - (midpoint[1]/2)]
y = [midpoint[0], midpoint[1]]
z = [midpoint[0] + (midpoint[0]/2),midpoint[1]]
xyz = {"x": x,"y": y,"z": z}

lines = {"xy" : "L1", "yx" : "L1", "yz": "L2", "zy" : "L2", "zx" : "L3", "xz" : "L3"}

distances = {"L1" : lengthOfLine(xyz["x"][0], xyz["y"][0], xyz["x"][1], xyz["y"][1], isInt = False ),
             "L2" : lengthOfLine(xyz["y"][0], xyz["z"][0], xyz["y"][1], xyz["z"][1], isInt = False ),
             "L3" : lengthOfLine(xyz["z"][0], xyz["x"][0], xyz["z"][1], xyz["x"][1], isInt = False )}

#this dictionary will be used for giving ~values (useful for equilateral etc.)
intDistances = {"L1" : lengthOfLine(xyz["x"][0], xyz["y"][0], xyz["x"][1], xyz["y"][1], isInt = True),
                "L2" : lengthOfLine(xyz["y"][0], xyz["z"][0], xyz["y"][1], xyz["z"][1], isInt = True ),
                "L3" : lengthOfLine(xyz["z"][0], xyz["x"][0], xyz["z"][1], xyz["x"][1], isInt = True  )}

Titles = pg.font.SysFont('Times New Roman', 20)
onTriangle = pg.font.SysFont('Times New Roman', 10)
userColor = colors["Black"]
while done: 
    for event in pg.event.get(): 
        if event.type == pg.QUIT: 
            done = False
        if event.type == pg.KEYDOWN:
            keyPressed = event.__dict__["unicode"]
            parseRelKeys(keyPressed, myPath, screen, colors)
    #setting background
    screen.fill(colors['White'])
    x, y, z = (xyz["x"]), (xyz["y"]), (xyz["z"])
    
    #drawing lines for the triangle
    idx = pg.draw.line(screen, colors["User Color"], x, y, 2)
    idy = pg.draw.line(screen, colors["User Color"], y, z, 2)
    idz = pg.draw.line(screen, colors["User Color"], z, x, 2)

    #see if the mouse is pressed
    if (pg.mouse.get_pressed()[0]): 
        #if mouse press is within a 10x10 block surrounding each coordinate in triangle, set new point.
        Mcoor = [int(x) for x in re.sub(r'[(),]', "",str(pg.mouse.get_pos())).split()]
        if (x[0] + 10 > Mcoor[0] > x[0] - 10 and x[1] + 10 > Mcoor[1] > x[1] - 10): 
                xyz["x"] = Mcoor
        elif (y[0] + 10 > Mcoor[0] > y[0] - 10 and y[1] + 10 > Mcoor[1] > y[1] - 10): 
            xyz["y"] = Mcoor
        elif (z[0] + 10 > Mcoor[0] > z[0] - 10 and z[1] + 10 > Mcoor[1] > z[1] - 10): 
            xyz["z"] = Mcoor

        #Both should probably be replaced with an update function
        distances = {"L1" : lengthOfLine(xyz["x"][0], xyz["y"][0], xyz["x"][1], xyz["y"][1], isInt = False ),
             "L2" : lengthOfLine(xyz["y"][0], xyz["z"][0], xyz["y"][1], xyz["z"][1], isInt = False ),
             "L3" : lengthOfLine(xyz["z"][0], xyz["x"][0], xyz["z"][1], xyz["x"][1], isInt = False )}
        
        intDistances = {"L1" : lengthOfLine(xyz["x"][0], xyz["y"][0], xyz["x"][1], xyz["y"][1], isInt = True),
                "L2" : lengthOfLine(xyz["y"][0], xyz["z"][0], xyz["y"][1], xyz["z"][1], isInt = True ),
                "L3" : lengthOfLine(xyz["z"][0], xyz["x"][0], xyz["z"][1], xyz["x"][1], isInt = True  )}
    

    Mpos = pg.mouse.get_pos()
    
    #utilize midpoint formula to get L1, L2, L3 label positioning
    posL1 = tuple([int(xyz["x"][0] + ((xyz["y"][0] - xyz["x"][0])/2)) + 1, int(xyz["x"][1] + (xyz["y"][1] - xyz["x"][1])/2)])
    posL2 = tuple([int(xyz["y"][0] + ((xyz["z"][0] - xyz["y"][0])/2)) + 1, int(xyz["y"][1] + (xyz["z"][1] - xyz["y"][1])/2)])
    posL3 = tuple([int(xyz["z"][0] + ((xyz["x"][0] - xyz["z"][0])/2)) + 1, int(xyz["z"][1] + (xyz["x"][1] - xyz["z"][1])/2)])

    #print position of L1, L2, L3
    titleL1L2L3 = [onTriangle.render("L1", False, colors["Red"]), onTriangle.render("L2", False, colors["Red"]), onTriangle.render("L3", False, colors["Red"])]
    screen.blit(titleL1L2L3[0], posL1)
    screen.blit(titleL1L2L3[1], posL2)
    screen.blit(titleL1L2L3[2], posL3)

    Mcoordinate = Titles.render("Mouse Coordinates" + str(Mpos), False, colors["Black"])
    #print '{:.3f}'.format(x)
    L1, L2, L3 = Titles.render("L1(px): " + str('{:.3f}'.format(distances["L1"])) + ", ~" + str(intDistances["L1"]) , False, colors["Black"]), Titles.render("L2(px): " + str('{:.3f}'.format(distances["L2"])) + ", ~" + str(intDistances["L2"]) , False, colors["Black"]), Titles.render("L3(px): " + str('{:.3f}'.format(distances["L3"]))+ ", ~" + str(intDistances["L3"])  , False, colors["Black"])
    
    #General Top Left Data
    screen.blit(Mcoordinate,(0,0))
    screen.blit(L1, (0,20))
    screen.blit(L2, (0,40))
    screen.blit(L3, (0,60))
    

    #angular data
    angles  = anglesUpdate(distances)
    L1L2 = Titles.render("Angle L1L2: Rad:" + str('{:.3f}'.format(angles["L1-L2"])) + " Degree" + str(int(math.degrees(angles["L1-L2"]))), False, colors["Black"])
    L2L3 = Titles.render("Angle L2L3: Rad:" + str('{:.3f}'.format(angles["L2-L3"])) + " Degree" + str(int(math.degrees(angles["L2-L3"]))), False, colors["Black"])
    L3L1 = Titles.render("Angle L3L1: Rad:" + str('{:.3f}'.format(angles["L3-L1"])) + " Degree" + str(int(math.degrees(angles["L3-L1"]))), False, colors["Black"])
    screen.blit(L1L2, (0,80))
    screen.blit(L2L3, (0,100))
    screen.blit(L3L1, (0,120))


    pg.display.update()
    clock.tick(60)
