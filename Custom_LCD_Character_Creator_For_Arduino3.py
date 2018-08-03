import pygame
from pygame.locals import *
import sys; sys.path.insert(0, "..")
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
    font = pygame.font.Font('freesansbold.ttf',TextSize)
    # returns the image rectangle
    screen_rect = screen.get_rect()
    # converts a text into a 'Surface' object
    text_surface = font.render(text, True, colour)
    # returns the text rectangle
    text_rect = text_surface.get_rect()
    # centers the text rectangle
    text_rect.center = (XPos,YPos)
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
    block = pygame.transform.scale(block,(BoxHeight/scaledAmount,BoxWidth/scaledAmount))
    boundingBox = block.get_rect(topleft=(0,0))
    H = boundingBox.topright[0]
    W = boundingBox.bottomright[1]
    return(block)

def Draw_Image(XPos,YPos,image):
    global H
    global W
    global pos
    global clickedArray
    mouseX = pos[0]
    mouseY = pos[1]
    image = Load_Image(image)
    screen.blit(image,(XPos-(W/2),YPos-(H/2)))

def in_Box(XPos,YPos,instance2,instance1):
    global H
    global W
    global pos
    global inboxArray
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
    
    #Button pressed Logic    
    if resultArray[instance1][instance2] == True and click == True and clickArray[instance1][instance2] >= 1:
        image = 'CheckBox1.png'
        BoxCheckedArray[instance1][instance2] = False
        click = False
        clickArray[instance1][instance2] = 0
        dataArray[instance1][instance2] = 0
        
    if resultArray[instance1][instance2]  == True and click == True or BoxCheckedArray[instance1][instance2] == True:
        image = 'CheckBox3.png'
        BoxCheckedArray[instance1][instance2] = True
        clickArray[instance1][instance2] = 1
        dataArray[instance1][instance2] = 1
    else:
        image = 'CheckBox1.png'
            
    if resultArray[instance1][instance2]  == False and BoxCheckedArray[instance1][instance2] == False:
        image = 'CheckBox1.png'

    Draw_Image(XPos,YPos,image)

def draw_box(XPos,YPos,height,width,background,boarderTh,borderColour,bgColour):
    input_box = pygame.Rect(XPos,YPos,width,height)

    if background == True:
        pygame.draw.rect(screen, bgColour, input_box, 0)
    
    pygame.draw.rect(screen, borderColour, input_box,boarderTh)

def button(XPos,YPos,height,width,background,boarderTh,borderColour,bgColour,caption,captionSize,captionColour):
    input_box = pygame.Rect(XPos,YPos,width,height)
    
    if background == True:
        pygame.draw.rect(screen, bgColour, input_box, 0)
    
    pygame.draw.rect(screen, borderColour, input_box,boarderTh)
    if(caption != ""):
        Text(caption,XPos+width/2,YPos+height/2,captionSize,captionColour)
        
def in_button(XPos,YPos,H,W):
    global pos
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
    
    #Button pressed Logic    
    if inButton == True and click == True and buttonClickCount >= 1:
        ButtonClicked = False
        click = False
        buttonClickCount = 0
        return ButtonClicked

    #if Clicked     
    if inButton == True and click == True and ButtonClicked == False:
        ButtonClicked = True
        buttonClickCount = 1
        #DisplayCode(XPos,YPos)
        return ButtonClicked
    
    else:
        ButtonClicked = False
        return ButtonClicked
    
    if inButton == False and ButtonClicked == False:
        ButtonClicked = False
        return ButtonClicked
   
def generateCode():
    global code
    global dataArray
    linenumber = 8
    codeLine = [0 for x in range(linenumber)]
    prefix = ("#include <LiquidCrystal.h> \nLiquidCrystal lcd(12, 11, 5, 4, 3, 2); \nbyte custom[8] = { \n  ")
    codeLine[0] = ("B")+str(dataArray[0][0])+str(dataArray[0][1])+str(dataArray[0][2])+str(dataArray[0][3])+str(dataArray[0][4])
    codeLine[1] = ("B")+str(dataArray[1][0])+str(dataArray[1][1])+str(dataArray[1][2])+str(dataArray[1][3])+str(dataArray[1][4])
    codeLine[2] = ("B")+str(dataArray[2][0])+str(dataArray[2][1])+str(dataArray[2][2])+str(dataArray[2][3])+str(dataArray[2][4])
    codeLine[3] = ("B")+str(dataArray[3][0])+str(dataArray[3][1])+str(dataArray[3][2])+str(dataArray[3][3])+str(dataArray[3][4])
    codeLine[4] = ("B")+str(dataArray[4][0])+str(dataArray[4][1])+str(dataArray[4][2])+str(dataArray[4][3])+str(dataArray[4][4])
    codeLine[5] = ("B")+str(dataArray[5][0])+str(dataArray[5][1])+str(dataArray[5][2])+str(dataArray[5][3])+str(dataArray[5][4])
    codeLine[6] = ("B")+str(dataArray[6][0])+str(dataArray[6][1])+str(dataArray[6][2])+str(dataArray[6][3])+str(dataArray[6][4])
    codeLine[7] = ("B")+str(dataArray[7][0])+str(dataArray[7][1])+str(dataArray[7][2])+str(dataArray[7][3])+str(dataArray[7][4])
    suffex = ("}; \n\nvoid setup()\n{\n  lcd.createChar(0, smiley);\n  lcd.begin(16, 2);\n  lcd.write(byte(0));\n}\n\nvoid loop()\n{\n}")
    code = (str(prefix) +str(codeLine[0])+"\n  " +str(codeLine[1])+"\n  "+str(codeLine[2])+"\n  "+str(codeLine[3])+"\n  "+str(codeLine[4])+"\n  "+str(codeLine[5])+"\n  "+str(codeLine[6])+"\n  "+str(codeLine[7])+"\n"+str(suffex))
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
    linenumber = 8
    codeLine = [0 for x in range(linenumber)]
    X = XPos
    Y = YPos
    F = windowSize[0]/45
    C = black
    S = 12
    scale = 0.65
    
    codeLine[0] = ("B")+str(dataArray[0][0])+str(dataArray[0][1])+str(dataArray[0][2])+str(dataArray[0][3])+str(dataArray[0][4])
    codeLine[1] = ("B")+str(dataArray[1][0])+str(dataArray[1][1])+str(dataArray[1][2])+str(dataArray[1][3])+str(dataArray[1][4])
    codeLine[2] = ("B")+str(dataArray[2][0])+str(dataArray[2][1])+str(dataArray[2][2])+str(dataArray[2][3])+str(dataArray[2][4])
    codeLine[3] = ("B")+str(dataArray[3][0])+str(dataArray[3][1])+str(dataArray[3][2])+str(dataArray[3][3])+str(dataArray[3][4])
    codeLine[4] = ("B")+str(dataArray[4][0])+str(dataArray[4][1])+str(dataArray[4][2])+str(dataArray[4][3])+str(dataArray[4][4])
    codeLine[5] = ("B")+str(dataArray[5][0])+str(dataArray[5][1])+str(dataArray[5][2])+str(dataArray[5][3])+str(dataArray[5][4])
    codeLine[6] = ("B")+str(dataArray[6][0])+str(dataArray[6][1])+str(dataArray[6][2])+str(dataArray[6][3])+str(dataArray[6][4])
    codeLine[7] = ("B")+str(dataArray[7][0])+str(dataArray[7][1])+str(dataArray[7][2])+str(dataArray[7][3])+str(dataArray[7][4])
    
    Text("include <LiquidCrystal.h>",X-35*scale,Y,F,C)
    Text("LiquidCrystal lcd(12, 11, 5, 4, 3, 2);",X+scale,Y+S*1,F,C)
    Text("nbyte custom[8] = {",X-60*scale,Y+S*2,F,C)
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
    Text("lcd.createChar(0, smiley);",X-15*scale,Y+S*15,F,C)
    Text("lcd.begin(16, 2);",X-55*scale,Y+S*16,F,C)
    Text("lcd.write(byte(0));",X-48*scale,Y+S*17,F,C)
    Text("}",X-140*scale,Y+S*18,F,C)
    Text("void loop()",X-100*scale,Y+S*20,F,C)
    Text("{",X-140*scale,Y+S*21,F,C)
    Text("}",X-140*scale,Y+S*23,F,C)
    
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
box1 = ('CheckBox1.png')
box2 = ('CheckBox2.png')
box3 = ('CheckBox3.png')
Load_Image(box1)
w = 5
h = 8
background = True
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

#for y in range(8):
#    print(dataArray[y])

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
    draw_box(windowSize[0]/2-20,windowSize[1]/2-140,300,250,True,3,blue,white)
        
    #generate code on the "click" of a button
    button(windowSize[0]-180,10,20,130,background,3,gray,lightGray,"Generate Code",windowSize[0]/28,black)
    inButton = in_button(windowSize[0]-180,10,20,130)
    buttonResult = button_click(windowSize[0]-180,10)
    #print(generateCode())

    generateCode()
    DisplayCode(windowSize[0]/2+80,windowSize[1]/2-128)

                  
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
