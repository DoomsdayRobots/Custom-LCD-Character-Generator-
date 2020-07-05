"""
Program Name:          Custom_LCD_Character_Creator_For_Arduino.py
Written By:            David Metcalf
Date Written:          july, 5, 2020

Program Decription:    This python program generates code for use in the arduino IDE.
                       The code that is generated in this program is for the purpose
                       of displaying a custom character on an LCD. Something like a
                       a smiley face or a company logo is a good example.
                       That LCD is then physicaly connected to the arduino hardware.
                       Some examples of arduino hardware are...
                       an arduino UNO or arduino nano.

Notes:                 Sound Bits and Bobs found on the website soundbible.com

                            http://soundbible.com/1280-Click-On.html = clickOnSound
                            http://soundbible.com/1294-Button-Click-Off.html = clickOffSound
                            http://soundbible.com/1795-Electrical-Sweep.html = compileSound

                       As far as I know, these are royalty free sounds.
"""

import pygame
import sys
import os
import time

pygame.init()

# Window Display Stuff
windowSize = [500,400]
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('Custom LCD Character Creator For Arduino')

# Time
clock = pygame.time.Clock()

# colour Pallet
black = pygame.color.Color('#000000')
white = pygame.color.Color('#FFFFFF')
skyblue = pygame.color.Color('#bed6fd')
blue = pygame.color.Color('#699efc')
red = pygame.color.Color('#dd191d')
green = pygame.color.Color('#2baf2b')
yellow = pygame.color.Color('#F6FF00')
groseYellow = pygame.color.Color('#FFD300')
gray = pygame.color.Color('#808080')
lightGray = pygame.color.Color('#A0A0A0')
darkGray = pygame.color.Color('#404040')

def Text(text,XPos,YPos,TextSize,colour):
    XPos = int(XPos)
    YPos = int(YPos)
    font = pygame.font.Font('freesansbold.ttf',TextSize)
    # returns the image rectangle
    screen_rect = screen.get_rect()
    # converts a text into a 'Surface' object
    text_surface = font.render(text, True, colour)
    # returns the text rectangle
    text_rect = text_surface.get_rect()
    # centers the text rectangle
    text_rect.center = (int(XPos),int(YPos))
    # draws the text
    screen.blit(text_surface, text_rect)
    
# load the Images
def Load_Image(image):
    global H
    global W
    block = pygame.image.load(image)
    boundingBox = block.get_rect(topleft=(0,0))
    BoxHeight = boundingBox.topright[0]
    BoxWidth = boundingBox.bottomright[1]
    scaledAmount = 2
    block = pygame.transform.scale(block,(int(BoxHeight/scaledAmount),int(BoxWidth/scaledAmount)))
    boundingBox = block.get_rect(topleft=(0,0))
    H = boundingBox.topright[0]
    W = boundingBox.bottomright[1]
    return(block)

def Draw_Image(XPos,YPos,image,show = True):
    global H
    global W
    global pos
    global clickedArray
    XPos = int(XPos)
    YPos = int(YPos)
    mouseX = pos[0]
    mouseY = pos[1]

    if show == True:
        image = Load_Image(image)
        screen.blit(image,(int(XPos-(W/2)),int(YPos-(H/2))))

def in_Box(XPos,YPos,instance2,instance1):
    global H
    global W
    global pos
    global inboxArray
    XPos = int(XPos)
    YPos = int(YPos)
    mouseX = pos[0]
    mouseY = pos[1]

    if(mouseX >= XPos-(W/2) and mouseX < XPos+(W/2) and mouseY >= YPos-(H/2) and mouseY < YPos+(H/2)):
        inboxArray[instance1][instance2] = 1
        return inboxArray[instance1][instance2]
    else:
        inboxArray[instance1][instance2] = 0
        return inboxArray[instance1][instance2]

def clicked(XPos,YPos,instance2,instance1):
    global inBox
    global BoxCheckedArray
    global click
    global clickCounter
    global clickArray
    global clickResult
    global clickOnSound
    global clickOffSound
    XPos = int(XPos)
    YPos = int(YPos)

    image = 'CheckBox1.png'
    Draw_Image(XPos,YPos,image,False)
    
    #Button pressed Logic    
    if resultArray[instance1][instance2] == True and click == True and clickArray[instance1][instance2] >= 1: #original
        BoxCheckedArray[instance1][instance2] = False
        clickArray[instance1][instance2] = 0
        dataArray[instance1][instance2] = 0

        image = 'CheckBox1.png'
    
        #sound
        if clickResult[instance1][instance2] == 1:
            pygame.mixer.stop()
            clickOffSound.play()
            clickResult[instance1][instance2] = 2
        
    if resultArray[instance1][instance2]  == True and click == True or BoxCheckedArray[instance1][instance2] == True: #original    
        BoxCheckedArray[instance1][instance2] = True
        clickArray[instance1][instance2] = 1
        dataArray[instance1][instance2] = 1

        image = 'CheckBox3.png'
        
        #sound
        if clickResult[instance1][instance2] == 0 or clickResult[instance1][instance2] == 2:
            pygame.mixer.stop()
            clickOnSound.play()
            clickResult[instance1][instance2] = 1
            
    else:
        clickResult[instance1][instance2] = 0
    
    #if resultArray[instance1][instance2]  == False and BoxCheckedArray[instance1][instance2] == False:
    #    image = 'CheckBox1.png'
    #    clickResult[instance1][instance2] = 0
    
    Draw_Image(XPos,YPos,image,True)

def draw_box(XPos,YPos,height,width,background,boarderTh,borderColour,bgColour):
    XPos = int(XPos)
    YPos = int(YPos)
    input_box = pygame.Rect(XPos,YPos,width,height)

    if background == True:
        pygame.draw.rect(screen, bgColour, input_box, 0)
    
    pygame.draw.rect(screen, borderColour, input_box,boarderTh)

def button(XPos,YPos,height,width,background,boarderTh,borderColour,bgColour,caption,captionSize,captionColour):
    XPos = int(XPos)
    YPos = int(YPos)
    input_box = pygame.Rect(XPos,YPos,width,height)
    
    if background == True:
        pygame.draw.rect(screen, bgColour, input_box, 0)
    
    pygame.draw.rect(screen, borderColour, input_box,boarderTh)
    if(caption != ""):
        Text(caption,XPos+width/2,YPos+height/2,captionSize,captionColour)
        
def in_button(XPos,YPos,H,W):
    global pos
    XPos = int(XPos)
    YPos = int(YPos)
    mouseX = pos[0]
    mouseY = pos[1]

    if(mouseX >= XPos and mouseX < XPos+W and mouseY >= YPos and mouseY < YPos+H):
        return True
    else:
        return False

def button_click(XPos,YPos):
    global inButton
    global ButtonClicked
    global click
    global buttonClickCount
    XPos = int(XPos)
    YPos = int(YPos)
    
    #Button pressed Logic    
    if inButton == True and click == True and buttonClickCount >= 1:
        ButtonClicked = False
        click = False
        buttonClickCount = 0
        return 0

    #if Clicked     
    if inButton == True and click == True and ButtonClicked == False:
        ButtonClicked = True
        buttonClickCount = 1
        write_File()
        return 1
    
    else:
        ButtonClicked = False
        return 0
    
    if inButton == False and ButtonClicked == False:
        ButtonClicked = False
        return 0


def write_File():
    global exportCounter
    with open("CustomChar"+str(exportCounter)+".ino", "w") as f:
        f.write(str(code))
        #exportCounter += 1
   
def generateCode():
    global code
    global dataArray
    linenumber = 8
    codeLine = [0 for x in range(linenumber)]
    prefix = ("#include <LiquidCrystal.h> \nLiquidCrystal lcd(12, 11, 5, 4, 3, 2); \nbyte customChar[8] = { \n  ")
    codeLine[0] = ("B")+str(dataArray[0][0])+str(dataArray[0][1])+str(dataArray[0][2])+str(dataArray[0][3])+str(dataArray[0][4])+","
    codeLine[1] = ("B")+str(dataArray[1][0])+str(dataArray[1][1])+str(dataArray[1][2])+str(dataArray[1][3])+str(dataArray[1][4])+","
    codeLine[2] = ("B")+str(dataArray[2][0])+str(dataArray[2][1])+str(dataArray[2][2])+str(dataArray[2][3])+str(dataArray[2][4])+","
    codeLine[3] = ("B")+str(dataArray[3][0])+str(dataArray[3][1])+str(dataArray[3][2])+str(dataArray[3][3])+str(dataArray[3][4])+","
    codeLine[4] = ("B")+str(dataArray[4][0])+str(dataArray[4][1])+str(dataArray[4][2])+str(dataArray[4][3])+str(dataArray[4][4])+","
    codeLine[5] = ("B")+str(dataArray[5][0])+str(dataArray[5][1])+str(dataArray[5][2])+str(dataArray[5][3])+str(dataArray[5][4])+","
    codeLine[6] = ("B")+str(dataArray[6][0])+str(dataArray[6][1])+str(dataArray[6][2])+str(dataArray[6][3])+str(dataArray[6][4])+","
    codeLine[7] = ("B")+str(dataArray[7][0])+str(dataArray[7][1])+str(dataArray[7][2])+str(dataArray[7][3])+str(dataArray[7][4])+","
    suffex = ("}; \n\nvoid setup()\n{\n  lcd.createChar(0,customChar);\n  lcd.begin(16, 2);\n  lcd.write(byte(0));\n}\n\nvoid loop()\n{\n}")
    code = (str(prefix) +str(codeLine[0])+"\n  " +str(codeLine[1])+"\n  "+str(codeLine[2])+"\n  "+str(codeLine[3])+"\n  "+str(codeLine[4])+"\n  "+str(codeLine[5])+"\n  "+str(codeLine[6])+"\n  "+str(codeLine[7])+"\n"+str(suffex)+"\n  "+"\n  ")
    # print(code)
 
    """
    byte smiley[8] = {
      B00000,
      B10001,
      B00000,
      B00000,
      B10001,
      B01110,
      B00000,
    };
    """


def DisplayCode(XPos,YPos):
    global code
    global dataArray
    XPos = int(XPos)
    YPos = int(YPos)
    linenumber = 8
    codeLine = [0 for x in range(linenumber)]
    X = int(XPos)
    Y = int(YPos)
    F = int(windowSize[0]/45)
    C = black
    S = 12
    scale = 0.65
    
    codeLine[0] = ("B")+str(dataArray[0][0])+str(dataArray[0][1])+str(dataArray[0][2])+str(dataArray[0][3])+str(dataArray[0][4])+","
    codeLine[1] = ("B")+str(dataArray[1][0])+str(dataArray[1][1])+str(dataArray[1][2])+str(dataArray[1][3])+str(dataArray[1][4])+","
    codeLine[2] = ("B")+str(dataArray[2][0])+str(dataArray[2][1])+str(dataArray[2][2])+str(dataArray[2][3])+str(dataArray[2][4])+","
    codeLine[3] = ("B")+str(dataArray[3][0])+str(dataArray[3][1])+str(dataArray[3][2])+str(dataArray[3][3])+str(dataArray[3][4])+","
    codeLine[4] = ("B")+str(dataArray[4][0])+str(dataArray[4][1])+str(dataArray[4][2])+str(dataArray[4][3])+str(dataArray[4][4])+","
    codeLine[5] = ("B")+str(dataArray[5][0])+str(dataArray[5][1])+str(dataArray[5][2])+str(dataArray[5][3])+str(dataArray[5][4])+","
    codeLine[6] = ("B")+str(dataArray[6][0])+str(dataArray[6][1])+str(dataArray[6][2])+str(dataArray[6][3])+str(dataArray[6][4])+","
    codeLine[7] = ("B")+str(dataArray[7][0])+str(dataArray[7][1])+str(dataArray[7][2])+str(dataArray[7][3])+str(dataArray[7][4])+","
    
    Text("include <LiquidCrystal.h>",X-35*scale,Y,F,C)
    Text("LiquidCrystal lcd(12, 11, 5, 4, 3, 2);",X+scale,Y+S*1,F,C)
    Text("nbyte customChar[8] = {",X-38*scale,Y+S*2,F,C)
    Text(str(codeLine[0]),X-90*scale,Y+S*3,F,C)
    Text(str(codeLine[1]),X-90*scale,Y+S*4,F,C)
    Text(str(codeLine[2]),X-90*scale,Y+S*5,F,C)
    Text(str(codeLine[3]),X-90*scale,Y+S*6,F,C)
    Text(str(codeLine[4]),X-90*scale,Y+S*7,F,C)
    Text(str(codeLine[5]),X-90*scale,Y+S*8,F,C)
    Text(str(codeLine[6]),X-90*scale,Y+S*9,F,C)
    Text(str(codeLine[7]),X-90*scale,Y+S*10,F,C)
    Text("};",X-135*scale,Y+S*11,F,C)
    Text("void setup()",X-95*scale,Y+S*13,F,C)
    Text("{",X-140*scale,Y+S*14,F,C)
    Text("lcd.createChar(0, customChar);",X-15*scale,Y+S*15,F,C)
    Text("lcd.begin(16, 2);",X-55*scale,Y+S*16,F,C)
    Text("lcd.write(byte(0));",X-48*scale,Y+S*17,F,C)
    Text("}",X-140*scale,Y+S*18,F,C)
    Text("void loop()",X-100*scale,Y+S*20,F,C)
    Text("{",X-140*scale,Y+S*21,F,C)
    Text("}",X-140*scale,Y+S*23,F,C)

# Load music and sound
clickOnSound = pygame.mixer.Sound("click_on.wav")
clickOffSound = pygame.mixer.Sound("click_off.wav")
compileSound = pygame.mixer.Sound("compile.wav")

#clickSound.play()
    
# Main Loop Variables
H = 0
W = 0
space = 5
code = ""
textSpace = 20
pos = [0,0]
click = False
inBox = False
buttonClick = False
inButton = False
buttonClickCount = 0
ButtonClicked = False
boxChecked = False
buttonResult = False
exportCounter = 0
box1 = ('CheckBox1.png')
box2 = ('CheckBox2.png')
box3 = ('CheckBox3.png')
Load_Image(box1)
w = 5
h = 8
background = True
clickResult = [[False for x in range(w)] for y in range(h)] 
BoxCheckedArray = [[False for x in range(w)] for y in range(h)]
clickArray = [[0 for x in range(w)] for y in range(h)]
inboxArray = [[0 for x in range(w)] for y in range(h)]
resultArray = [[False for x in range(w)] for y in range(h)]
dataArray = [[0 for x in range(w)] for y in range(h)]
input_box = pygame.Rect(10,10,5,5)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
keycount = 0
active = False
textbox_text = ''


# Main loop
done = False
while not done:
    screen.fill(skyblue)

    
    # starting point
    X = windowSize[0]/2-200
    Y = windowSize[1]/2-140

    for col in range (8):
        for row in range (5):
            Draw_Image(X+(W+space)*row,Y+(H+space)*col,'CheckBox1.png')
            resultArray[col][row] = in_Box(X+(W+space)*row,Y+(H+space)*col,row,col)
            clicked(X+(W+space)*row,Y+(H+space)*col,row,col)
                
    #draw a window for displaying the generated code
    draw_box(int(windowSize[0]/2-20),int(windowSize[1]/2-140),300,250,True,3,blue,white)
        
    #generate code on the "click" of a button
    button(int(windowSize[0]-180),10,20,130,background,3,gray,lightGray,"Generate Code",int(windowSize[0]/28),black)
    inButton = in_button(windowSize[0]-180,10,20,130)
    buttonResult = button_click(int(windowSize[0]-180),10)
    if buttonResult == True:
        generateCode()
        write_File()
        exportCounter += 1
        print("generating code...")
        print("")
        #print(code)
        pygame.mixer.stop()
        compileSound.play()
        buttonResult = False
        


    
    DisplayCode(int(windowSize[0]/2+80),int(windowSize[1]/2-128))

                  
    #check for a mouse click
    for event in pygame.event.get():
        
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
            # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False
            # Change the current color of the input box.
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:    
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    keycount = keycount -1
                else:
                    keycount += 1
                    text += event.unicode
                    
            print(keycount)
            
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip()
    clock.tick(20)
pygame.quit()
print("Bye...")
exit
