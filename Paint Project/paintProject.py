#***************************************************************
#   Samuel Xu 2016
#   Period 2
#   Star Wars Paint
#   
#   This paint program is perfect for the dedicated Star Wars fan,
#   filled with all the featurees of a normal paint program, and 
#   some extra features for the avid Star Wars Lover!!
#   
#   Features: Pencil and eraser tool of various sizes, fill 
#   bucket, backgrounds, stamps, new page, text with different 
#   fonts, shapes, and line tool.
#
#   For an enhanced experience, play the "textcrawl.mpeg" in the
#   paint folder -pygame doesn't play movies on windows :(
#****************************************************************

from pygame import *
from math import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

root = Tk()
root.withdraw()

init() #initiate and play star wars theme
mixer.music.load("music1.mp3")
mixer.music.play(-1)

font.init() #initiate fonts
timesFont = font.SysFont("Times New Roman", 20)
starFont = font.Font("Starjedi.ttf",20)
comicFont = font.Font("comicFont.ttf",20)

screen = display.set_mode((1024,768))#initiate screen resolution
screen.fill((255,255,255))
screen.blit(image.load("background.jpg"),(0,0))
screen.blit(image.load("starwars-logo.png"),(5,5))

#color variables
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,183,0)

c = black

# function to fill in gaps of white in the drawing
def fill(x,y,c):   
    pts = [(x,y)] #List of points to be replaced
    screen.set_clip(canvasRect)  
    col = tuple(screen.get_at((mx,my))) 
    if col != c:  #If current color is not same as selected color, begin replaceing pixels
        while len(pts) > 0:
            tx,ty = pts.pop()  #Temporary x and y values
            if screen.get_at((tx,ty)) == col and canvasRect.collidepoint((tx,ty)):
                screen.set_at((tx,ty),c)  #Begin branching out until another color is reached, 
                pts.append((tx+1,ty))     #while there are still points to be replaced
                pts.append((tx-1,ty))
                pts.append((tx,ty+1))
                pts.append((tx,ty-1))

#********************************Stamp Boxes****************************************

vaderRect = Rect(260,20,140,162)  #DarthVader stamp
screen.blit(image.load("vader.gif"),(260,20))
obiRect = Rect(400,10,100,166)    #Obi Wan Kenobi Stamp
screen.blit(image.load("obi.gif"),(400,10))
lukeRect = Rect(500,10,120,158)   #Luke Skywalker Stamp
screen.blit(image.load("luke.gif"),(500,10))
c3p0Rect = Rect(620,20,100,150)   #C3P0 Stamp
screen.blit(image.load("c3p0.gif"),(620,20))
r2d2Rect = Rect(720,55,90,113)    #R2D2 Stamp
screen.blit(image.load("r2d2.gif"),(720,55))
hanRect = Rect(800,45,130,122)    #Han Solo ***SPOILER ALERT*** Dies
screen.blit(image.load("han.gif"),(800,45))
yodaRect = Rect(910,60,100,106)   #Yoda Stamp
screen.blit(image.load("yoda.gif"),(910,60))

#********************************Background Icons*****************************************

icanvasbg1 = transform.scale(image.load("canvasbg1.jpg"),(150,90))
icanvasbg2 = transform.scale(image.load("canvasbg2.jpg"),(150,90))
icanvasbg3 = transform.scale(image.load("canvasbg3.jpg"),(150,90))

#******************************Menu, Canvas Rects and Borders************************************

pencilRect = Rect(20,130,40,40)
menuRect = Rect(20,175,225,300)
menuBorder = Rect(18,173,228,303)
descRect = Rect(20,480,225,100)
descBorder = Rect(18,478,228,103)
s1Rect = Rect(30,210,50,230)
s2Rect = Rect(80,210,50,230)
s3Rect = Rect(130,210,50,230)
s4Rect = Rect(180,210,50,230)
eraserRect = Rect(65,130,40,40)
brushRect = Rect(110,130,40,40)
textRect = Rect(155,130,40,40)
t1Rect = Rect(30,185,200,90)
t2Rect = Rect(30,275,200,90)
t3Rect = Rect(30,365,200,90)
f1Rect = Rect(30,180,100,65)
f2Rect = Rect(140,180,100,65)
f3Rect = Rect(30,255,100,65)
f4Rect = Rect(140,255,100,65)
f5Rect = Rect(30,330,210,65)
f6Rect = Rect(30,400,210,65)
shapeRect = Rect(200,130,40,40)

canvasRect = Rect(270,200,720,550)
canvasBorder = Rect(268,198,723,553)
draw.rect(screen,white,canvasRect)

#*****************************Tool Selection Rects and Icons**********************************

colorRect = Rect(20,595,200,170)
screen.blit(image.load("colormap.gif"),(20,595))
draw.rect(screen,white,pencilRect)
screen.blit(image.load("pencil.png"),(20,130))
draw.rect(screen,white,eraserRect)
screen.blit(image.load("eraser.png"),(65,130))
draw.rect(screen,white,brushRect)
screen.blit(image.load("Paintbucket.png"),(110,130))
draw.rect(screen,white,textRect)
screen.blit(image.load("text.png"),(155,130))
draw.rect(screen,white,shapeRect)
screen.blit(image.load("shapeicon.png"),(200,130))
redoRect = Rect(900,10,40,22)
screen.blit(image.load("redo.png"),(900,10))
undoRect = Rect(950,10,40,22)
screen.blit(image.load("undo.png"),(950,10))
saveRect = Rect(870,10,30,30)
screen.blit(image.load("save.png"),(870,10))
loadRect = Rect(840,10,30,30)
screen.blit(image.load("upload.png"),(840,10))

#*******************************Initializing Various Variables*******************

redo = []
undo = []
polypoints = []
running = True
txt = "times" #start font as times new roman
tool = "pencil" #start tool as pencil
words = ""
cpos = (0,0)
r = 20
sz = 1
oldw = 10
down = True
odown = True
mx = 0
my = 0
shape = ""
wid = 1
undo.append(screen.subsurface(canvasRect).copy()) #Add first screen copy to undo

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONUP:
            tx,ty = e.pos  
            if down == True:    #if the mouse is up, and it was down before, then down is False
                down = False    #if mosue is on the canvas while this happens, add a screen copy to undo
                if canvasRect.collidepoint(mx,my):
                    undo.append(screen.subsurface(canvasRect).copy())
        if e.type == KEYDOWN:
            if tool == "shapes":
                wid = 4
                if e.key == K_LEFT:
                    wid -= 2
                    wid = max(wid,1)
                elif e.key == K_RIGHT:
                    wid += 2 
                    wid = min(20,wid)   
                elif e.key == K_RETURN and polypoints: #If return key is pressed, and polypoints is not empty
                    for i in range (len(polypoints)-1):#draw lines connecting all dots, and clear polypoints[]
                        draw.line(screen,c,polypoints[i],polypoints[i-1],5)
                draw.line(screen,c,polypoints[len(polypoints)-1],polypoints[0])      
                polypoints = []            
            if e.key == K_ESCAPE: 
                running = False
            if e.key == K_BACKSPACE and tool == "text":    #if tool is text and presses backspace, take one letter off 
                words = words[:-1]
            elif e.key == K_RETURN: #if return key is pressed, erase words, and start writing 20 pixels down
                ty += 20
                words = ""
                screenPic = screen.subsurface(canvasRect).copy()
            else:
                words += e.unicode #if not, add to existing string
            if tool == "text":  #blits picture of the text on the screen
                screen.set_clip(canvasRect)
                screen.blit(screenPic,(270,200)) 
                if txt == "times":
                    screen.blit(timesFont.render(words,True,c),(tx,ty))
                elif txt == "starw":
                    screen.blit(starFont.render(words,True,c),(tx,ty))
                elif txt == "comic":
                    screen.blit(comicFont.render(words,True,c),(tx,ty))
                    
        if e.type == MOUSEBUTTONDOWN:
            cpos = (mx,my) 
            if tool == "text": #wipes all words if the mouse is clicked elsewhere
                words = ""
            if tool == "shapes":
                stx = mx  #start and ending positions for line tool
                sty = my
            screenPic = screen.subsurface(canvasRect).copy()
            if undoRect.collidepoint(mx,my) and len(undo)>0: #blits previous picture of undo onto the screen,
                screen.blit(undo[len(undo)-1],(270,200))     #and adds it to redo
                temp = undo[len(undo)-1]
                undo.remove(temp)
                redo.append(temp)
            if redoRect.collidepoint(mx,my) and len(redo)>0:
                screen.blit(redo[len(redo)-1],(270,200))     #blits previous picture of redo onto the screen,
                temp = redo[len(redo)-1]                     #and adds it to undo
                redo.remove(temp)
                undo.append(temp)
            if down == False: #if mouse was up before, change to down
                down = True
        
    mb = mouse.get_pressed()
    mx, my = mouse.get_pos()
                
    #***************************Tool Boxes and Borders***********************************
    #Draws borders, canvas, menu, and description rects

    draw.rect(screen,yellow,canvasBorder,2)
    draw.rect(screen,yellow,menuBorder,2)
    draw.rect(screen,yellow,descBorder,2)
    draw.rect(screen,yellow,pencilRect,2)
    draw.rect(screen,yellow,eraserRect,2)
    draw.rect(screen,yellow,brushRect,2)
    draw.rect(screen,yellow,textRect,2)
    draw.rect(screen,yellow,shapeRect,2)
    draw.rect(screen,white,menuRect)
    draw.rect(screen,white,descRect)

    #********************Drawing RED borders if mouse is over the tool box******************
    #Draws red indicators over the selected item if the mouse is over it

    if canvasRect.collidepoint(mx,my):
        draw.rect(screen,red,canvasBorder,2)
    elif menuRect.collidepoint(mx,my):
        draw.rect(screen,red,menuBorder,2)
    elif descRect.collidepoint(mx,my):
        draw.rect(screen,red,descBorder,2)

    if tool == "pencil":
        if s1Rect.collidepoint(mx,my): 
            draw.rect(screen,red,(44,210,3,230),1)
        elif s2Rect.collidepoint(mx,my): 
            draw.rect(screen,red,(90,210,10,230),4)
        elif s3Rect.collidepoint(mx,my):
            draw.rect(screen,red,(135,210,20,230),4)
        elif s4Rect.collidepoint(mx,my):
            draw.rect(screen,red,(180,210,30,230),4)

    if tool == "eraser":
        if f6Rect.collidepoint(mx,my):
            draw.rect(screen,red,f6Rect,2)
        elif s1Rect.collidepoint(mx,my):
            draw.circle(screen,red,(45,210),12,4)
        elif s2Rect.collidepoint(mx,my):
            draw.circle(screen,red,(95,230),22,4)
        elif s3Rect.collidepoint(mx,my):
            draw.circle(screen,red,(145,270),32,4)
        elif s4Rect.collidepoint(mx,my):
            draw.circle(screen,red,(195,350),42,4)

    if tool == "bucket":
        if t1Rect.collidepoint(mx,my):
            draw.rect(screen,red,(59,179,152,92),3)
        elif t2Rect.collidepoint(mx,my):
            draw.rect(screen,red,(59,279,152,92),3)
        elif t3Rect.collidepoint(mx,my):
            draw.rect(screen,red,(59,379,152,92),3)

    if tool == "text":
        if t1Rect.collidepoint(mx,my):
            draw.rect(screen,red,t1Rect,2)
        elif t2Rect.collidepoint(mx,my):
            draw.rect(screen,red,t2Rect,2)
        elif t3Rect.collidepoint(mx,my):
            draw.rect(screen,red,t3Rect,2)

    if tool == "shapes":
        if f1Rect.collidepoint(mx,my):
            draw.ellipse(screen,red,(29,179,102,67),2)
        if f2Rect.collidepoint(mx,my):
            draw.ellipse(screen,red,(139,179,102,67),2)
        if f3Rect.collidepoint(mx,my):
            draw.rect(screen,red,(29,254,102,67),2)
        if f4Rect.collidepoint(mx,my):
            draw.rect(screen,red,(139,254,102,67),2)
        elif f5Rect.collidepoint(mx,my):
            draw.circle(screen,red,(50,350),6)
            draw.circle(screen,red,(200,350),6)
            draw.line(screen,red,(50,350),(200,350),5)
        elif f6Rect.collidepoint(mx,my):        #draws a line and circle 2 pixels wider than 
            draw.circle(screen,red,(50,400),6)  #the actual image under the polygon
            draw.circle(screen,red,(70,450),6)
            draw.circle(screen,red,(150,460),6)
            draw.circle(screen,red,(165,390),6)
            draw.circle(screen,red,(210,430),6)
            draw.line(screen,red,(50,400),(70,450),5)
            draw.line(screen,red,(70,450),(150,460),5)
            draw.line(screen,red,(50,400),(165,390),5)
            draw.line(screen,red,(165,390),(210,430),5)
            draw.line(screen,red,(210,430),(150,460),5)

    #**********************************Color Selector*****************************************
                
    if colorRect.collidepoint(mx,my):
        draw.line(screen,screen.get_at((mx,my)),(235,600),(235,760),7) #displays current color 
        if mb[0] == 1:
            c = screen.get_at((mx,my)) #sets the current color as the one in the color box 
    else:
        draw.line(screen,c,(235,600),(235,760),7)

    #**********************************TOOL SELECTION***********************************************

    if cpos == (mx,my): #checks to make sure the mouse was not dragged onto the tool button                       
        if pencilRect.collidepoint(mx,my):      #Pencil tool
            draw.rect(screen,red,pencilRect,2)
            if mb[0] == 1:
                tool = "pencil"
        elif eraserRect.collidepoint(mx,my):
            draw.rect(screen,red,eraserRect,2)  #Eraser tool
            if mb[0] == 1:
                tool = "eraser"
        elif brushRect.collidepoint(mx,my):
            draw.rect(screen,red,brushRect,2)   #Bucket tool
            if mb[0] == 1:
                tool = "bucket"
        elif textRect.collidepoint(mx,my):
            draw.rect(screen,red,textRect,2)    #Text tool
            if mb[0] == 1:
                tool = "text"
        elif shapeRect.collidepoint(mx,my):
            draw.rect(screen,red,shapeRect,2)   #Shape Tool
            if mb[0] == 1:
                tool = "shapes"
        elif vaderRect.collidepoint(mx,my) and mb[0] == 1:  #Darth vader
            tool = "vader.gif"
        elif obiRect.collidepoint(mx,my) and mb[0] == 1:    #Obi Wan Kenobi
            tool = "obi.gif"
        elif lukeRect.collidepoint(mx,my) and mb[0] == 1:   #Luke Skywalker
            tool = "luke.gif"
        elif c3p0Rect.collidepoint(mx,my) and mb[0] == 1:   #C3PO
            tool = "c3p0.gif"
        elif r2d2Rect.collidepoint(mx,my) and mb[0] == 1:   #R2D2
            tool = "r2d2.gif"
        elif hanRect.collidepoint(mx,my) and mb[0] == 1:    #Han Solo
            tool = "han.gif"
        elif yodaRect.collidepoint(mx,my) and mb[0] == 1:   #Yoda
            tool = "yoda.gif"
        if saveRect.collidepoint(mx,my) and mb[0] == 1:                            # Save tool
            fileName = asksaveasfilename(parent=root,title="Save The Image As...") # gets the directory the image is to be saved to
            if fileName != "":
                image.save(screen.subsurface(canvasRect),fileName)
        elif loadRect.collidepoint(mx,my) and mb[0] == 1:
            screen.set_clip(canvasRect)                                 # Upload tool
            fileName = askopenfilename(parent=root,title="Open Image:") # gets which directory it needs to open the image from
            screen.blit(image.load(fileName), canvasRect)

    #*************************** DRAW TOOLS *********************************
        
    if tool == "pencil":
        screen.blit(timesFont.render("Click on the canvas to",True,black),(25,500))  #Writes in description rect
        screen.blit(timesFont.render("draw, and select the ",True,black),(25,520))
        screen.blit(timesFont.render("desired width on the menu!",True,black),(25,540))
        draw.line(screen,c,(45,210),(45,440),1) #draws lines of various sizes for selection
        draw.line(screen,c,(95,210),(95,440),10)
        draw.line(screen,c,(145,210),(145,440),20)
        draw.line(screen,c,(195,210),(195,440),30)
        if mb[0] == 1:                      #Each size is selected from the menu    
            if s1Rect.collidepoint(mx,my):
                sz = 1
            elif s2Rect.collidepoint(mx,my):
                sz = 5
            elif s3Rect.collidepoint(mx,my):
                sz = 10
            elif s4Rect.collidepoint(mx,my):
                sz = 15
            if (canvasRect.collidepoint(mx, my) or canvasRect.collidepoint(oldmx, oldmy)):
                screen.set_clip(canvasRect)
                if sz == 1:
                    draw.line(screen,c,(oldmx,oldmy),(mx,my),1) #If the size is 1, then draw line from old cords to new
                else:
                    dist = ((mx-oldmx)**2+(my-oldmy)**2)**(1/2) #Draws a line of circles from old coords to new
                    dist = max(1,dist)                          #by using similar triangles and a for loop to draw
                    ix = (mx - oldmx)/dist                      #circles along a line
                    iy = (my - oldmy)/dist
                    for j in range (int(dist)):                  
                        draw.circle(screen, c, (int(oldmx+ix*j), int(oldmy+iy*j)), sz)
    elif tool == "eraser":
        screen.blit(timesFont.render("Click the canvas to erase,",True,black),(25,500))  #Writes in description Rect
        screen.blit(timesFont.render("select the desired width on",True,black),(25,520))
        screen.blit(timesFont.render("the menu, or clear it all!",True,black),(25,540))
        draw.circle(screen,black,(45,210),10,1)  #Draws circles displaying eraser width
        draw.circle(screen,black,(95,230),20,1)
        draw.circle(screen,black,(145,270),30,1)
        draw.circle(screen,black,(195,350),40,1)
        screen.blit(image.load("clear.jpg"),(35,410))  #Draws the "new page" icon
        if mb[0] == 1:
            if f6Rect.collidepoint(mx,my):  #Prioritize the new page rect over others
                draw.rect(screen,white,canvasRect)
            elif s1Rect.collidepoint(mx,my):
                sz = 10
            elif s2Rect.collidepoint(mx,my):
                sz = 20
            elif s3Rect.collidepoint(mx,my):
                sz = 30
            elif s4Rect.collidepoint(mx,my):
                sz = 40
            if (canvasRect.collidepoint(mx, my) or canvasRect.collidepoint(oldmx, oldmy)):
                screen.set_clip(canvasRect)                 #Using same method as pencil, draws a continuous line 
                dist = ((mx-oldmx)**2+(my-oldmy)**2)**(1/2) #of white circles along a line
                dist = max(1,dist)
                ix = (mx - oldmx)/dist
                iy = (my - oldmy)/dist
                for j in range (int(dist)):
                    draw.circle(screen, white, (int(oldmx+ix*j), int(oldmy+iy*j)), sz)
    elif tool == "bucket":
        screen.blit(timesFont.render("Select a background,",True,black),(25,500))  #Writes in description rect
        screen.blit(timesFont.render("or use the fill tool to",True,black),(25,520))
        screen.blit(timesFont.render("fill in a select area!",True,black),(25,540))
        screen.blit(icanvasbg1,(60,180))  #blits background icons
        screen.blit(icanvasbg2,(60,280))
        screen.blit(icanvasbg3,(60,380))
        if mb[0] == 1:                    #Blits background examples onto the menu
            if t1Rect.collidepoint(mx,my):
                screen.blit(image.load("canvasbg1.jpg"),(270,200))    
            elif t2Rect.collidepoint(mx,my):
                screen.blit(image.load("canvasbg2.jpg"),(270,200))
            elif t3Rect.collidepoint(mx,my):
                screen.blit(image.load("canvasbg3.jpg"),(270,200))
            elif canvasRect.collidepoint(mx,my):
                fill(mx,my,c)             #If the mouse is clicked down on the canvas, use fill tool
    elif tool == "text":
        screen.blit(timesFont.render("Choose from a variety",True,black),(25,500))  #Writes in description rect
        screen.blit(timesFont.render("of fonts, which includes",True,black),(25,520))
        screen.blit(timesFont.render("our unique Star Wars font!",True,black),(25,540))
        screen.blit(image.load("timesfontpic.png"),(35,190))    #blits font examples onto the menu
        screen.blit(image.load("starfontpic.png"),(35,278))
        screen.blit(image.load("sans.gif"),(35,390))
        if mb[0] == 1:    #Selecting fonts
            if t1Rect.collidepoint(mx,my):
                txt = "times"
            elif t2Rect.collidepoint(mx,my):
                txt = "starw"
            elif t3Rect.collidepoint(mx,my):
                txt = "comic"     
    elif tool == "shapes":
        screen.blit(timesFont.render("Select shape, or polygon",True,black),(25,500)) #..You get the point
        screen.blit(timesFont.render("to draw on canvas. (press",True,black),(25,520))
        screen.blit(timesFont.render("enter to draw polygon)",True,black),(25,540))
        draw.ellipse(screen,c,f1Rect)  #Draws example rectangles, ellipses, and lines on the menu
        draw.ellipse(screen,c,f2Rect,1)
        draw.rect(screen,c,f3Rect)
        draw.rect(screen,c,f4Rect,1)
        draw.circle(screen,c,(50,350),5)
        draw.circle(screen,c,(200,350),5)
        draw.line(screen,c,(50,350),(200,350),3)
        draw.circle(screen,c,(50,400),5)  #I was to lazy to find a picture but ended up putting 
        draw.circle(screen,c,(70,450),5)  #more work in drawing an actual polygon :P
        draw.circle(screen,c,(150,460),5) 
        draw.circle(screen,c,(165,390),5)
        draw.circle(screen,c,(210,430),5)
        draw.line(screen,c,(50,400),(70,450),3)
        draw.line(screen,c,(70,450),(150,460),3)
        draw.line(screen,c,(50,400),(165,390),3)
        draw.line(screen,c,(165,390),(210,430),3)
        draw.line(screen,c,(210,430),(150,460),3)
        if f1Rect.collidepoint(mx,my) and mb[0] == 1: #shape selector
            shape = "FillEllipse"
        elif f2Rect.collidepoint(mx,my) and mb[0] == 1:
            shape = "EmptyEllipse"
        elif f3Rect.collidepoint(mx,my) and mb[0] == 1:
            shape = "FillRect"
        elif f4Rect.collidepoint(mx,my) and mb[0] == 1:
            shape = "EmptyRect"
        elif f5Rect.collidepoint(mx,my) and mb[0] == 1:
            shape = "line"
        elif f6Rect.collidepoint(mx,my) and mb[0] == 1:
            shape = "polygon"
        if canvasRect.collidepoint(mx,my):
            screen.set_clip(canvasRect)
            if (mb[2] == 1 or mb[1] == 1) and shape == "polygon" and polypoints:
                for i in range (len(polypoints)-1): #draws lines connecting all the polypoints
                    draw.line(screen,c,polypoints[i],polypoints[i-1],5)
                draw.line(screen,c,polypoints[len(polypoints)-1],polypoints[0])
                polypoints = []
            elif mb[0] == 1: 
                screen.blit(screenPic, (270,200))
                screen.set_clip(canvasRect)
                l = mx-stx
                h = my-sty
                if shape == "FillEllipse":  #Draws a filled ellipse   
                    ellipse = Rect(stx,sty,l,h)
                    ellipse.normalize()
                    draw.ellipse(screen,c,ellipse,0)
                elif shape == "EmptyEllipse":#Draws an empty ellipse
                    ellipse = Rect(stx,sty,l,h)
                    ellipse.normalize()
                    if abs(l)<6 or abs(h)<6: #If the width is greater than ellipse radius, draw a filled ellipse
                        draw.ellipse(screen,c,ellipse,0)
                    else:
                        draw.ellipse(screen,c,ellipse,3)
                elif shape == "FillRect":    #Draws a filled rectangle
                    rect = Rect(stx,sty,l,h)
                    rect.normalize()
                    draw.rect(screen,c,rect,0)
                elif shape == "EmptyRect":   #Draws an empty rectangle
                    rect = Rect(stx,sty,l,h)
                    rect.normalize()
                    draw.rect(screen,c,rect,3)
                elif shape == "line":   #Draws a straight line from start to current mouse position
                    if mb[0] ==1 and canvasRect.collidepoint(mx,my):
                        screen.set_clip(canvasRect)
                        screen.blit(screenPic, (270,200))
                        draw.line(screen,c,(stx,sty),(mx,my),4)
                elif shape == "polygon":
                    polypoints.append((mx,my))
                    draw.circle(screen,c,(mx,my),2) #If clicked, then add the mouse position to polypoints

    #If the tool is not any of the above, use sticker tool
    if tool != "shapes" and tool != "pencil" and tool != "bucket" and tool != "eraser" and tool != "text":
        screen.blit(image.load(tool),(50,230))  #blit a sticker image onto the menu rect
        screen.blit(timesFont.render("Select a star wars",True,black),(25,500))
        screen.blit(timesFont.render("character and bring them",True,black),(25,520))
        screen.blit(timesFont.render("to life on the canvas!",True,black),(25,540))
        if mb[0] == 1 and canvasRect.collidepoint(mx,my): #Blit tool at the mouse position
            screen.set_clip(canvasRect)  
            screen.blit(screenPic,(270,200)) 
            screen.blit(image.load(tool),(mx-50,my-70))
    screen.set_clip(None)    
       
    oldmx = mx #old mx and my for draw and erase tools
    oldmy = my
    display.flip()

quit()

