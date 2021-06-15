print("Playing Snake")

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

import sys
sys.path.append("../")
from aiModules import aiScript

rows = 54
width = 1080
height = 1080

longest = 0
loseMsg = f"ERROR NO_END_MSG"

aiCon, testmd = bool(), bool()
class cube(object):
    global width

    w = height
    rows = 54
    def __init__(self, start, dirnx=1, dirny=0, color=(132,169,140)):

        #Initializes a cube object.
        #This constructor is used for both the snake's tail and the snack.
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color


    def move(self, dirnx, dirny):

        #Sets the object's direction variable equal to this method's arguments.
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0] #Row
        j = self.pos[1] #Column

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis, dis))
        if eyes:    #This part is optional. It just draws the eyes.
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):

        #Sets the color of the snake
        self.color = color

        #Sets the head to be a cube in the starting position.
        self.head = cube(pos)

        #Adds the head to the list.
        self.body.append(self.head)

        #Keeps track of the position the snake is moving.
        #At least one of them has to be 0 at any given time.
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        global dirx, diry, headPosX, headPosY
        #---------------INPUT CONTROLS---------------

        #I don't know what this does -Rus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if aiCon == False:
            #---------------PLAYER CONTROLS---------------

            #A list of all keys usable in pygame.
            #It returns true to the key being pressed.
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    #Sets the x direction to -1.
                    #The snake will start moving to the left.
                    self.dirnx = -1
                    self.dirny = 0

                    #Stores its current turn into the turns list.
                    #This is for the snake's tail.
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        else:
            #---------------AI CONTROLS---------------
            print()

            #Auto controls
            aiScript.check()
            self.dirnx = dirx
            self.dirny = diry
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            aiScript.hdX = self.head.pos[0]
            aiScript.hdY = self.head.pos[1]


            plist = []
            #For debugging:
            if True:# testmd == True:
                direction = str()
                if dirx == 1:
                    direction = "Right"
                elif dirx == -1:
                    direction = "Left"
                elif diry == 1:
                    direction = "Down"
                elif diry == -1:
                    direction = "Up"
                for i, c in enumerate(self.body):
                    plist.append(c.pos[:])
                print(f"Dir: {direction} (X: {dirx}, Y: {diry}); Parts: {plist}")



        #---------------MOVEMENT----------------

        for i, c in enumerate(self.body):
        #Variable "i" is the index, "c" is the cube (refers to the individual snake tail chunk as cubes).
        #These variables are copied from "body" in this object.

            #Copy of the [current] position.
            p = c.pos[:]

            #Checks if the [current] position is in the "turns" list.
            if p in self.turns:
                #"turn" = the value of the index in the "turns" list.
                turn = self.turns[p]

                #Tells the cube to move
                c.move(turn[0], turn[1])

                #Checks if the current index is pointing at the last cube.
                if i == len(self.body)-1:
                    #Removes the current cube from the list "turns".
                    self.turns.pop(p)
            else:
                #Checks if the snake reached the edge of the screen.
                #If it returns true, it will move the head to the opposite side of the screen.
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)

                #If all are false, simply move the cube forward once.
                else: c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        global headPosX, headPosY
        """
        Called when the snake collides with itself.
        Resets the game to its starting conditions.
        """
        headPosX = pos[0]
        headPosY = pos[1]
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        """
        Creates a new cube object.
        """
        #Assigns the tail to the last object of the "body" list.
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny

        #Checks the current direction of the tail then adds a new cube object.
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        #Loops through each cube of the snake.
        for i, c in enumerate(self.body):
            #Checks if the cube referenced is the head of the snake.
            if i == 0:
                #Draws the snake on the surface with eyes.
                c.draw(surface, True)
            else:
                #Draws the snake on the surface.
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows    #sizeBtwn is 25
    x = 0
    y = 0

    for l in range(rows):
        #This loop will repeat 20 times (value of the variable "rows")

        #These indicate where the next line should be placed.
        #var = current value + 25
        x = x + sizeBtwn
        y = y + sizeBtwn

        #Draws a white line on the game window. #Edit: Changed to mint green.
        #This line extends from the 0th pixel to the window width.
        #pygame.draw.line(surface, (22,22,22), (x, 0), (x, w))
        #pygame.draw.line(surface, (22,22,22), (0, y), (w, y))

def redrawWindow(surface):
    global width, rows, s, snack

    #Sets the window background to black (0,0,0).
    #Edit: Changed to mint green.
    #surface.fill((153,217,140))
    surface.fill((20,20,20))

    #Draws the snake on the screen.
    s.draw(surface)

    #Draws the snack on the screen.
    snack.draw(surface)

    #Draws a grid on the game window with a specified size and # of rows.
    drawGrid(width, rows, surface)

    #Updates the window to the next frame.
    pygame.display.update()

def randomSnack(rows, items):
    global snackx, snacky
    positions = items.body

    while True:
        snackx = random.randrange(rows)
        snacky = random.randrange(rows)

        aiScript.snX = snackx
        aiScript.snY = snacky
        print(f"New Snack Pos: {aiScript.snX}, {aiScript.snY}")

        #Checks if the randomly chosen position is where the snake is.
        #Makes sure that the snack doesn't spawn on the snake.
        if len(list(filter(lambda z:z.pos == (snackx,snacky), positions))) > 0:
            continue
        else:
            break

    return (snackx,snacky)

def messageBox(subject, content):
    #Creates a new Tk object named root.
    root = tk.Tk()

    #Forces the message box to appear in front
    root.attributes("-topmost", True)

    root.withdraw() #I don't know what this does. -Rus

    #Displays the message as a separate window.
    messagebox.showinfo(subject, content)

    try:
        #Removes the root object
        root.destroy()
    except:
        # It will continually try to remove the root object until the user closes the message box.
        pass

def main():
    global width, rows, s, snack, aiCon, dirnx, dirny, longest, loseMsg

    flag = True

    #Creates a window object for displaying.
    win = pygame.display.set_mode((width, height))

    #Creates a snake object. First parameter is the color, second is the position.
    s = snake((132,169,140), (random.randrange(rows),random.randrange(rows)))

    #Creates a snack object.
    snack = cube(randomSnack(rows, s), color = (random.randrange(50,255),random.randrange(50,255),random.randrange(50,255)))#(158,42,43))

    #Creates a clock object.
    clock = pygame.time.Clock()

    while flag:
        #Delays the time by 50ms to avoid absurd playing speeds.
        #Lower number = faster updates
        #pygame.time.delay(0)

        #Forces the game to update 10 ticks per second.
        #Lower number = slower updates
        clock.tick(10)
        s.move()

        #Checks if the snack is in the same position as the snake's head.
        if s.body[0].pos == snack.pos:

            #Adds a new cube to the snake's body.
            s.addCube()

            #Creates a new snack object.
            snack = cube(randomSnack(rows, s), color = (random.randrange(50,255),random.randrange(50,255),random.randrange(50,255)))

        for x in range(len(s.body)):
            #Checks if the head collides with any other part of the body.
            cldx, cldy = True, True


            #If the head (pos) is headed towards a body part based on the current direction,
            #turn to the direction closest to the snack.
            isNotHeadX = s.body[x] != s.body[0]
            not0X = dirx != 0
            willCollideX = s.body[0].pos[0] + s.dirnx*0 == s.body[x].pos[0]

            isNotHeadY = s.body[x] != s.body[0]
            not0Y = diry != 0
            willCollideY = s.body[0].pos[1] + s.dirny*0 == s.body[x].pos[1]
            if isNotHeadX and not0X and willCollideX:
                print(f"Head {s.body[0].pos} will collide with X:{x}! S: {s.body[0].pos[0]}+{s.dirnx}, B: {s.body[x].pos}, NoGo: {aiScript.noGo}")
                #aiScript.noGo = (s.dirnx, s.dirny)
                #aiScript.check()
#                 s.dirnx = dirx
#                 s.dirny = diry
#                 s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]
#                 aiScript.hdX = s.head.pos[0]
#                 aiScript.hdY = s.head.pos[1]

            else: cldx = False

            if isNotHeadY and not0Y and willCollideY:
                print(f"Head {s.body[0].pos} will collide with Y:{x}! S: {s.body[0].pos[1]}+{s.dirny}, B: {s.body[x].pos}, NoGo: {aiScript.noGo}")
                #aiScript.noGo = (s.dirnx, s.dirny)
                #aiScript.check()
#                 s.dirnx = dirx
#                 s.dirny = diry
#                 s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]
#                 aiScript.hdX = s.head.pos[0]
#                 aiScript.hdY = s.head.pos[1]

            else: cldy = False

            """
            Known problems:
            - Can't detect when AI turns directly backwards.
            -
            """
            if x == 0:
                print(f"H: {s.body[0].pos[0]}, {s.body[0].pos[1]}")
            if cldx == False and cldy == False and x > 0:
                #print(f"B: ")
                print(f"B: {s.body[x].pos[0]}, {s.body[x].pos[1]}; Index: {x}")

            #print(f"x: {s.body[x].pos[1]} y: {s.body[x].pos[0]}")
#                 if s.body[0].pos == s.body[x].pos[0] + dirx:
#                     print(f"{s.body[0].pos} will collide with {s.body[x].pos}")

            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                if len(s.body) > longest:
                    longest = len(s.body)
                    loseMsg = f"\nGame Over! Highscore: {longest*10}"
                print(f"{loseMsg}")
                #pygame.time.wait(3600000)
                #quit()
                if False:
                    messageBox(f"You lost with {len(s.body)*10} points!", "Play again?")
                s.reset((random.randrange(20),random.randrange(20)))
                break

        #Updates the frame
        redrawWindow(win)


def init():
    global dirx, diry, snackx, snacky, headPosX, headPosY


dirx = 0
diry = 0
snackx = 0
snacky = 0
headPosX = 0
headPosY = 0
coords = []

def start(PC):
    global aiCon, loseMsg
    aiCon = PC
    try:
        main()
    except pygame.error as e:
        #Catches a false error when the game is closed.
        print(f"Game closed.\nFalse error: \"{str(e)}\"")
        print(loseMsg)
        quit()
#     except Exception as e:
#         #Catches every other error.
#         print(f"Exception caught: {str(e)}")
#         quit()

if __name__ == "__main__":
    sys.path.append("../")
    from aiModules import aiScript
    testmd = True
    print("---------------DEBUG MODE---------------")
    aiScript.run()
elif __name__ != "__main__" and testmd == True:
    sys.path.append("../")
    from aiModules import aiScript
    testmd = True
    aiScript.run()
else:
    print("---------------PLAY MODE---------------")
    testmd == False
