#This file will handle the optional RGB slider that the user will have access to
import pygame as pg 
import pdb
import re 
def rgbHome(screen, colors): 
     done = True
     w, h = pg.display.get_surface().get_size()
     #pdb.set_trace()
     #how long are the bars?
     barLength =  int(w/2)

     #barlength = 300
     #bar 0...300
     #each increment on the bar, is equal to ? increment out of 255
     #current value of x

     #how far apart will they be? 50 will be the buffer space, 
     #so between first bar and screen top, there will be 25px
     barSpacing = int((h - 50) / 3)
     
     #bar start and end coordinates
     redSE = [[0,25], [barLength, 25]]
     greenSE = [[0, 25 + barSpacing], [barLength, 25 + barSpacing]]
     blueSE = [[0, 25 + (2 * barSpacing)], [barLength, 25 + (2 * barSpacing)]]
     #'SB' = 'Slider Bar'
     SBRed, SBGreen, SBBlue = redSE[0][:], greenSE[0][:], blueSE[0][:]
     
     ratio = barLength/255
     #we will now create a dictionary for the slider values (based on user color (r, g, b))
     ratio = barLength/255
     Titles = pg.font.SysFont('Times New Roman', 20)
     while done: 
         for event in pg.event.get(): 
             if event.type == pg.QUIT:
                 done = False
             if event.type == pg.KEYDOWN: 
                 keyPressed = event.__dict__["unicode"]
                 if keyPressed == 'b': return
         
         if(pg.mouse.get_pressed()[0]): 
             Mcoor = [int(x) for x in re.sub(r'[(),]', "",str(pg.mouse.get_pos())).split()]
             if (SBRed[0] + barLength> Mcoor[0] > SBRed[0] - barLength and SBRed[1] + 20 > Mcoor[1] > SBRed[1] - 20 and Mcoor[0] <= barLength):
                 SBRed[0] = Mcoor[0]
             elif (SBGreen[0] + barLength> Mcoor[0] > SBGreen[0] - barLength and SBGreen[1] + 20 > Mcoor[1] > SBGreen[1] - 20 and Mcoor[0] <= barLength):
                 SBGreen[0] = Mcoor[0]
             elif (SBBlue[0] + barLength> Mcoor[0] > SBBlue[0] - barLength and SBBlue[1] + 20 > Mcoor[1] > SBBlue[1] - 20 and Mcoor[0] <= barLength):
                 SBBlue[0] = Mcoor[0]
             
         
         red, green, blue = int((SBRed[0]/barLength) * 255), int((SBGreen[0]/ barLength) * 255), int((SBBlue[0] /barLength) * 255)
         
         #update user color
         colors["User Color"] = (red, green, blue)

         screen.fill(colors["White"])
         pg.draw.line(screen, colors["Red"], redSE[0], redSE[1], 5)
         pg.draw.line(screen, colors["Green"], greenSE[0], greenSE[1], 5)
         pg.draw.line(screen, colors["Blue"], blueSE[0], blueSE[1], 5)
         pg.draw.circle(screen, colors["Black"], SBRed, 10, 0)
         pg.draw.circle(screen, colors["Black"], SBGreen, 10, 0)
         pg.draw.circle(screen, colors["Black"], SBBlue, 10, 0)
         
         pg.draw.polygon(screen, colors["User Color"], [(w, 0), (w - 100, 0),(w - 100, h) , (w, h)], 0)
         
         Mpos = pg.mouse.get_pos()
         Mcoordinate = Titles.render("Mouse Coordinates" + str(Mpos), False, colors["Black"])
         screen.blit(Mcoordinate,(0,0))

         #Begin Bliting the values
         REDS = Titles.render("Red: " + str(red), False, colors["Black"])
         GREENS = Titles.render("Green: " + str(green), False, colors["Black"])
         BLUES = Titles.render("Blue: " + str(blue), False, colors["Black"])
         screen.blit(REDS, (barLength + 5, SBRed[1]))
         screen.blit(GREENS, (barLength + 5, SBGreen[1]))
         screen.blit(BLUES, (barLength + 5, SBBlue[1]))
        

         
         pg.display.update()

