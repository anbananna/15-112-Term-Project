## ** yeehaw HELLO FELLOW GAMERS ** ##
#  jk. but hello, how are you, welcome to my project. to start right off the bat,
#  yes.
#  all my code is in one file, but trust me, beauty in a thick bundle. i really do
#  hope you enjoy meticulously looking through my algorithmically algorithmic code
#  and just the project as a whole because i had a blast, surely almost an
#  explosion, making this.
#  sayonara and hope your summers are chill and stay healthy. weeezoomzoom
######################################
#  (the formatting of this file should roughly be from end to beginning)  #

import module_manager
module_manager.review()

from pygame.locals import *
from collections import deque
from imutils.video import VideoStream
import numpy as np
import pygame, cv2, sys, time, random, argparse, imutils, collections, os, math


# initializing application window
pygame.init()

displayWidth = 840
displayHeight = 720
frameWidth = 800

myDisplay = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()

scale = 1
white = (255, 255, 255)
black = (15,15,15)

fade = pygame.Surface((displayWidth, displayHeight))
fade.fill(black)


def graphColor(color):
    # retrieves the color of the object tracked to be shown when viewer is viewing their drawing
    if color == 'blue':
        return (0, 0, 255)
    elif color == 'green':
        return (0, 255, 0)
    elif color == 'red':
        return(255, 0, 0)


def end():
    # touch of the start screen to close off the applicaiton; allows the user to exit the app
    introImage = pygame.image.load('images/startmenu.png')
    quitb = pygame.image.load('images/quit.png')
    quitb1 = pygame.image.load('images/quit_1.png')

    scale = 1.75
    imageDimX, imageDimY = introImage.get_rect().size
    imageDimX, imageDimY = int(scale*imageDimX), int(scale*imageDimY)
    introImage = pygame.transform.scale(introImage, (imageDimX, imageDimY))
    imageX = displayWidth/2 - imageDimX/2 + 10
    imageY = displayHeight/2 - imageDimY*(7/8)

    qDimX, qDimY = quitb.get_rect().size
    scaleq = 0.5
    qDimX, qDimY = int(scaleq*qDimX), int(scaleq*qDimY)
    quitb = pygame.transform.scale(quitb, (qDimX, qDimY))
    quitb1 = pygame.transform.scale(quitb1, (qDimX, qDimY))
    buttonX, buttonY = (displayWidth/2 - qDimX/2), (displayHeight/2 + imageDimY*(1/3))

    if imageDimY != displayHeight:
        if imageDimY > displayHeight:
            scale = displayHeight/imageDimY
        else:
            scale = imageDimY/displayHeight

    myDisplay.fill(black)
    pygame.display.update()

    radian = 0
    cube = cubed((0, 0, 0.5))
    increase = True
    num = random.randint(1, 6)

    while True:
        t = clock.tick()/2000
        radian += 2*t

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if cube.scale > num:
            increase = False
        elif cube.scale < 0.00001:
            increase = True
        if increase:
            cube.scale += 0.0005
        else:
            cube.scale -= 0.001

        myDisplay.fill(black)
        
        for edge in edges:
            points = []
            for x, y, z in cubeVertices[edge[0]], cubeVertices[edge[1]]:
                x += cube.pos[0]
                y += cube.pos[1]
                z += cube.pos[2]
                x, z = rotateCube((x, z), radian)
                y, z = rotateCube((y, z), radian)
                z += 5
                if z != 0:
                    d = 250 / z
                x, y = x * d * cube.scale, y * d * cube.scale
                points += [(cubeX + int(x), cubeY + int(y))]

            pygame.draw.line(myDisplay, (100, 100, 100), points[0], points[1], 2)

        myDisplay.blit(introImage, (imageX, imageY))
        myDisplay.blit(quitb, (buttonX, buttonY))
        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()[0]

        buttonBX, buttonBY = buttonX + qDimX, buttonY + qDimY
        if (buttonX < mousePos[0] < buttonBX) and (buttonY < mousePos[1] < buttonBY):
            myDisplay.blit(quitb1, (buttonX, buttonY))
            if mouse:
                for n in range(0, 300, 10):
                    fade.set_alpha(n)
                    myDisplay.blit(introImage, (imageX, imageY))
                    myDisplay.blit(quitb1, (buttonX, buttonY))
                    myDisplay.blit(fade, (imageX, imageY))
                    pygame.display.update()
                pygame.quit()
                quit()

        pygame.display.update()


def viewChooser(pts, color):
    # displays a menu that allows the user to choose which view they want to see their object in
    views = pygame.image.load('images/views.png')
    vDimX, vDimY = views.get_rect().size
    scale = 2
    vDimX, vDimY = int(scale*vDimX), int(scale*vDimY)
    views = pygame.transform.scale(views, (vDimX, vDimY))
    vX, vY = displayWidth/2 - vDimX/2, 70

    keyrot = pygame.image.load('images/key rotate.png')
    keyrot1 = pygame.image.load('images/key rotate_1.png')
    keyrot2 = pygame.image.load('images/key rotate_2.png')
    krotDimX, krotDimY = keyrot.get_rect().size
    scale = 0.5
    krotDimX, krotDimY = int(scale*krotDimX), int(scale*krotDimY)
    keyrot = pygame.transform.scale(keyrot, (krotDimX, krotDimY))
    keyrot1 = pygame.transform.scale(keyrot1, (krotDimX, krotDimY))
    krotX, krotY = (displayWidth - 2*krotDimX) / 3, displayHeight/2 - krotDimX/2 + 125
    scale = 0.55
    krot2DimX, krot2DimY = keyrot2.get_rect().size
    krot2DimX, krot2DimY = int(scale*krot2DimX), int(scale*krot2DimY)
    keyrot2 = pygame.transform.scale(keyrot2, (krot2DimX, krot2DimY))
    krot2X, krot2Y = (krotX*2 + krotDimX)/2 - krot2DimX/2, krotY + krotDimY + 30
    
    freerot = pygame.image.load('images/free rotate.png')
    freerot1 = pygame.image.load('images/free rotate_1.png')
    freerot2 = pygame.image.load('images/free rotate_2.png')
    freerot = pygame.transform.scale(freerot, (krotDimX, krotDimY))
    freerot1 = pygame.transform.scale(freerot1, (krotDimX, krotDimY))
    frotX, frotY = krotX*2 + krotDimX, krotY
    freerot2 = pygame.transform.scale(freerot2, (krot2DimX, krot2DimY))
    frot2X, frot2Y = (frotX*2 + krotDimX)/2 - krot2DimX/2, krot2Y

    finish = pygame.image.load('images/finish.png')
    finish1 = pygame.image.load('images/finish_1.png')
    scale = 0.45
    finDimX, finDimY = finish.get_rect().size
    finDimX, finDimY = int(scale*finDimX), int(scale*finDimY)
    finish = pygame.transform.scale(finish, (finDimX, finDimY))
    finish1 = pygame.transform.scale(finish1, (finDimX, finDimY))
    finX, finY = displayWidth - finDimX - 10, displayHeight - finDimY - 10

    key = []
    for n in range(1, 102, 3):
        key.append('images/k_' + str(n) + '.png')
    i = 0

    free = []
    for n in range(1, 85, 2):
        free.append('images/f_' + str(n) + '.png')
    j = 0
    
    for n in range(300, 0, -15):
        fade.set_alpha(n)
        myDisplay.blit(views, (vX, vY))
        myDisplay.blit(keyrot, (krotX, krotY))
        myDisplay.blit(freerot, (frotX, frotY))
        myDisplay.blit(finish, (finX, finY))
        myDisplay.blit(fade, (0, 0))
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        myDisplay.fill(black)
        myDisplay.blit(views, (vX, vY))
        myDisplay.blit(keyrot, (krotX, krotY))
        myDisplay.blit(freerot, (frotX, frotY))
        myDisplay.blit(finish, (finX, finY))

        image = pygame.image.load(key[i])
        iDimX, iDimY = image.get_rect().size
        scale = 0.40
        iDimX, iDimY = int(scale*iDimX), int(scale*iDimY)
        image = pygame.transform.scale(image, (iDimX, iDimY))
        crop = pygame.Surface((iDimX - 45, iDimY - 150))
        crop.blit(image, (0, 0), (20, 23, iDimX, iDimY - 150))
        myDisplay.blit(crop, ((krotX*2 + krotDimX)/2 - (iDimX - 45)/2, krotY - 175))
        i += 1
        if i > 31:
            i = 0

        imagef = pygame.image.load(free[j])
        iDimX, iDimY = imagef.get_rect().size
        scale = 0.25
        iDimX, iDimY = int(scale*iDimX), int(scale*iDimY)
        imagef = pygame.transform.scale(imagef, (iDimX, iDimY))
        crop = pygame.Surface((iDimX - 50, iDimY - 110))
        crop.blit(imagef, (0, 0), (40, 30, iDimX - 50, iDimY - 110))
        myDisplay.blit(crop, ((frotX*2 + krotDimX)/2 - (iDimX - 45)/2, krotY - 175))
        pygame.display.update()
        j += 2
        if j == 40:
            j = 0

        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()[0]

        if (krotX < mousePos[0] < krotX + krotDimX) and (krotY < mousePos[1] < krotY + krotDimY):
            myDisplay.blit(keyrot1, (krotX, krotY))
            myDisplay.blit(keyrot2, (krot2X, krot2Y))
            myDisplay.blit(finish, (finX, finY))
            if mouse:
                for n in range(0, 300, 7):
                    fade.set_alpha(n)
                    myDisplay.blit(views, (vX, vY))
                    myDisplay.blit(keyrot1, (krotX, krotY))
                    myDisplay.blit(keyrot2, (krot2X, krot2Y))
                    myDisplay.blit(finish, (finX, finY))
                    myDisplay.blit(crop, ((krotX*2 + krotDimX)/2 - (iDimX - 45)/2, krotY - 210))
                    myDisplay.blit(crop, ((frotX*2 + krotDimX)/2 - (iDimX - 45)/2, krotY - 210))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                keyCube(pts, color)

        elif (frotX < mousePos[0] < frotX + krotDimX) and (frotY < mousePos[1] < frotY + krotDimY):
            myDisplay.blit(freerot1, (frotX, frotY))
            myDisplay.blit(freerot2, (frot2X, frot2Y))
            if mouse:
                for n in range(0, 300, 7):
                    fade.set_alpha(n)
                    myDisplay.blit(views, (vX, vY))
                    myDisplay.blit(freerot1, (frotX, frotY))
                    myDisplay.blit(freerot2, (frot2X, frot2Y))
                    myDisplay.blit(finish, (finX, finY))
                    myDisplay.blit(crop, ((krotX*2 + krotDimX)/2 - (iDimX - 45)/2, krotY - 210))
                    myDisplay.blit(crop, ((frotX*2 + krotDimX)/2 - (iDimX - 45)/2, krotY - 210))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                moveCube(pts, color)
                
        elif (finX < mousePos[0] < finX + finDimX) and (finY < mousePos[1] < finY + finDimY):
            myDisplay.blit(finish1, (finX, finY))
            if mouse:
                for n in range(0, 300, 7):
                    fade.set_alpha(n)
                    myDisplay.blit(views, (vX, vY))
                    myDisplay.blit(keyrot, (krotX, krotY))
                    myDisplay.blit(freerot, (frotX, frotY))
                    myDisplay.blit(finish, (finX, finY))
                    myDisplay.blit(crop, ((krotX*2 + krotDimX)/2 - (iDimX - 45)/2, krotY - 210))
                    myDisplay.blit(crop, ((frotX*2 + krotDimX)/2 - (iDimX - 45)/2, krotY - 210))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                end()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()


def pointFormat(radList, coordinates):
    # formatting the points retrieved from the color tracing function to set the points up onto the
    # correct axis when the viewer is looking at their drawings
    maxRad = max(radList)
    xPoints = [] # radlist
    yPoints = [] # x points
    zPoints = [] # y points
    length = len(radList)

    for n in range(length):
        y = radList[n]
        foo = coordinates[n]
        x, z = foo[0], foo[1]
        xPoints.append(x)
        yPoints.append(y)
        zPoints.append(z)

    zMax = max(zPoints)
    yMax = max(yPoints)
    xMax = max(xPoints)

    for n in range(length):
        zN = zPoints[n]
        yN = yPoints[n]
        xN = xPoints[n]
        zPoints[n] = zMax - zN
        yPoints[n] = yMax - yN
        xPoints[n] = xMax - xN

    pL = []
    for n in range(length):
        x = xPoints[n]
        y = yPoints[n]
        z = zPoints[n]
        pL.append([x,y,z])
    return pL


def drawToView():
    # short message for the users to know what is coming up next
    myDisplay.fill(black)
    dtv = pygame.image.load('images/drawtoview.png')
    dDimX, dDimY = dtv.get_rect().size
    scale = 0.9
    dDimX, dDimY = int(scale*dDimX), int(scale*dDimY) - 10
    dtv = pygame.transform.scale(dtv, (dDimX, dDimY))
    dtvX, dtvY = displayWidth/2 - dDimX/2, displayHeight/2 - dDimY/2
    myDisplay.blit(dtv, (dtvX, dtvY))
    
    time.sleep(0.2)
    
    for n in range(300, 0, -10):
        fade.set_alpha(n)
        myDisplay.blit(dtv, (dtvX, dtvY))
        myDisplay.blit(fade, (0, 0))
        pygame.display.update()

    time.sleep(4)
    
    for n in range(0, 300, 4):
        fade.set_alpha(n)
        myDisplay.blit(dtv, (dtvX, dtvY))
        myDisplay.blit(fade, (0, 0))
        pygame.display.update()

    pygame.display.update()


vertices = (0,-2,0),(2,-2,0),(2,0,0),(0,0,0),(0,-2,-2),(2,-2,-2),(2,0,-2),(0,0,-2)
edges = (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)
cx, cy = (displayWidth//2, displayHeight//2)

"""
vv complex to think through and geometrically manipulate to look right
"""

class View:
    # class for free rotating function/feature/view
    def __init__(self, position = (0,0,0), rotation = (0.436332, -0.698132), scale = 2.5):
        self.pos = list(position)
        self.rot = list(rotation)
        self.scale = scale

    def rotate(self, event):
        # tracked mouse movement and changes the points and axis' position, amount rotated, and scale
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= 200
            y /= 200
            self.rot[0] += y
            self.rot[1] += x
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if (self.scale + 0.1) <= 2.75:
                    self.scale += 0.05
            if event.button == 5:
                if (self.scale - 0.1) > 1.75:
                    self.scale -= 0.05


def moveCube(pts, color):
    # free rotating function that allows the users to zoom in/out and rotate their drawing
    view = View((0,0,-0,5))
    pygame.event.set_allowed(pygame.MOUSEMOTION)
    pygame.event.get()
    pygame.mouse.get_rel()
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    fdir = pygame.image.load('images/freedirections.png')
    scale = 0.55
    fDimX, fDimY = fdir.get_rect().size
    fDimX, fDimY = int(scale*fDimX), int(scale*fDimY)
    fdir = pygame.transform.scale(fdir, (fDimX, fDimY))
    fX, fY = 10, 10

    while True:
        t = clock.tick()/2000
        myDisplay.fill(black)

        key = pygame.key.get_pressed()

        if key[pygame.K_b]:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            myDisplay.fill(black)
            myDisplay.blit(fdir, (fX, fY))
            pygame.display.update()
            for n in range(0, 300, 15):
                fade.set_alpha(n)
                myDisplay.blit(fdir, (fX, fY))
                myDisplay.blit(fade, (0, 0))
                pygame.display.update()
            viewChooser(pts, color)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    quit()
            view.rotate(event)

        myDisplay.blit(fdir, (fX, fY))
        
        for edge in edges:
            points = []
            for x, y, z in vertices[edge[0]], vertices[edge[1]]:
                x, z = rotateCube((x, z), view.rot[1])
                y, z = rotateCube((y, z), view.rot[0])
                z += 10
                d = 250/z
                x, y = x*d*view.scale, y*d*view.scale
                points += [(cx+int(x), cy+int(y))]
            if not(edge == (0,1) or edge == (1,2) or edge == (2,6) or edge == (0,4) or edge == (4,5) or
                   edge == (1,5) or edge == (6,7) or edge == (7,4) or edge == (5,6)):
                pygame.draw.line(myDisplay, white, points[0], points[1], 1)

        for x, y, z in pts:
            y *= -1
            z += 5
            f = 200/z
            x, y = x * (view.scale - 0.5), y * (view.scale - 0.5)
            z *= -1
            z *= (view.scale - 1.25)
            y, z = z, y
            x, z = rotateCube((x,z), view.rot[1])
            y, z = rotateCube((y,z), view.rot[0])
            pygame.draw.circle(myDisplay, color, (cx+int(x), cy+int(y)), 6)

        pygame.display.flip()


svertices = (-2,-2,2),(-2,2,2),(2,2,2),(2,-2,2),(-2,-2,-2),(-2,2,-2),(2,2,-2),(2,-2,-2)
sedges = (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)


class spinView:
    # class for controlled rotating with keys
    def __init__(self, position = (0,0,0), rotation = (0,0), scale = 1):
        self.pos = list(position)
        self.rot = list(rotation)
        self.scale = scale

    def movement(self, t, key):
        # tracks user's keyboard and scrolling motions to control the points and axis' position, rotation, and scale
        dm = t * 10
        if key[pygame.K_UP]:
            self.rot[0] -= t*2
        if key[pygame.K_DOWN]:
            self.rot[0] += t*2
        if key[pygame.K_LEFT]:
            self.rot[1] -= t*2
        if key[pygame.K_RIGHT]:
            self.rot[1] += t*2
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if (self.scale + 0.1) <= 1.75:
                        self.scale += 0.03
                if event.button == 5:
                    if (self.scale - 0.1) > 0.3:
                        self.scale -= 0.03
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


def keyCube(pts, color):
    # allows users to vie their obejct through keyboard motions and mouse scrolling, more controlled than the free rotating feature
    radian = 0
    view = spinView((0, 0, 0.5))

    kdir = pygame.image.load('images/keydirections.png')
    scale = 0.55
    kDimX, kDimY = kdir.get_rect().size
    kDimX, kDimY = int(scale*kDimX), int(scale*kDimY)
    kdir = pygame.transform.scale(kdir, (kDimX, kDimY))
    kX, kY = 10, 10

    back = pygame.image.load('images/back_draw.png')
    back1 = pygame.image.load('images/back_draw_1.png')
    scale = 0.4
    backDimX, backDimY = back.get_rect().size
    backDimX, backDimY = int(scale*backDimX), int(scale*backDimY)
    back = pygame.transform.scale(back, (backDimX, backDimY))
    back1 = pygame.transform.scale(back1, (backDimX, backDimY))
    backX, backY = 10, displayHeight - backDimY - 10

    while True:
        t = clock.tick()/2000
        myDisplay.fill(black)
        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        myDisplay.blit(kdir, (kX, kY))
        myDisplay.blit(back, (backX, backY))
    
        for x, y, z in pts:
            v0, v1, v2 = view.pos[0] * 100, view.pos[1] * 100, view.pos[2] * 100
            x += v0
            y += v1
            z += v2
            z += v2
            y *= -1
            z += 5
            if z != 0:
                f = 200/z
            x, y = x * (view.scale - 0.05), y * (view.scale - 0.05)
            z *= -(view.scale - 0.05)
            y, z = z, y
            x, z = rotateCube((x,z), view.rot[1])
            y, z = rotateCube((y,z), view.rot[0])
            pygame.draw.circle(myDisplay, color, (cx+int(x), cy+int(y)), 6)

        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()[0]

        if (backX < mousePos[0] < backX + backDimX) and (backY < mousePos[1] < backY + backDimY):
            myDisplay.blit(kdir, (kX, kY))
            myDisplay.blit(back1, (backX, backY))
            if mouse:
                for n in range(0, 300, 15):
                    fade.set_alpha(n)
                    myDisplay.blit(kdir, (kX, kY))
                    myDisplay.blit(back1, (backX, backY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                viewChooser(pts, color)

        pygame.display.flip()
        view.movement(t, key)


# referenced from https://gist.github.com/radames/1e7c794842755683162b
# heavily influenced by https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
def liveDraw(color):
    # tracks what the user is drawing (how large an object is to remember depth and position of object on the screen)
    (color, bgrHex), lower, upper = colorGetter(color)

    argp = argparse.ArgumentParser() # easy to write user-friendly command-line interfaces --> defines what arguments it requires
    argp.add_argument("-b", "--buffer", type = int, default = 5000, help = "max buffer size") # tells argumentparser how to take strings on command line --> objects
    args = vars(argp.parse_args()) # returns object with two attributes (integers, accumulate); list of one or more ints, accumulate max()
    points = deque(maxlen = args["buffer"])
    vs = VideoStream(src = 0).start()
    radList = []

    screen = pygame.display.set_mode([displayWidth, displayHeight])
    fWidth = frameWidth - 80

    direc = pygame.image.load('images/livedirections.png')
    scale = 0.5
    dirDimX, dirDimY = direc.get_rect().size
    dirDimX, dirDimY = int(scale*dirDimX), int(scale*dirDimY)
    direc = pygame.transform.scale(direc, (dirDimX, dirDimY))
    dX, dY = 15, 250

    notdrawn = pygame.image.load('images/notdrawn.png')
    scale = 1
    ndDimX, ndDimY = notdrawn.get_rect().size
    ndDimX, ndDimY = int(scale*ndDimX), int(scale*ndDimY)
    notdrawn = pygame.transform.scale(notdrawn, (ndDimX, ndDimY))
    notdrawnX, notdrawnY = displayWidth/2 - ndDimX/2, displayHeight/2 - ndDimY/2 + 200

    reset = pygame.image.load('images/livereset.png')
    scale = 0.5
    rDimX, rDimY = reset.get_rect().size
    rDimX, rDimY = int(scale*rDimX), int(scale*rDimY)
    reset = pygame.transform.scale(reset, (rDimX, rDimY))
    rX, rY = dX + 50, dY + dirDimY - 5

    yT, zT = False, 0

    if color == 'blue':
        hx = (0, 0, 255)
    elif color == 'green':
        hx = (0, 255, 0)
    elif color == 'red':
        hx = (255, 0, 0)
    view = View((0,0,-0.5))

    pygame.event.set_allowed(pygame.MOUSEMOTION)
    pygame.event.get()
    pygame.mouse.get_rel()
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    pts = []
    screen.fill(black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                vs.stream.release()
                quit()

        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN] and len(pts) != 0:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            vs.stream.release()
            return pts
        elif key[pygame.K_RETURN] and len(pts) == 0:
            if len(radList) == 0:
                myDisplay.blit(notdrawn, (notdrawnX, notdrawnY))
                yT = True
                zT = 0

        elif key[pygame.K_SPACE]:
            pts = liveDraw(color)
            return pts

        if yT and zT < 81:
            myDisplay.blit(notdrawn, (notdrawnX, notdrawnY))
            zT += 1
            print(zT)
            if zT == 80:
                zT == 0
                yT = False
        else:
            screen.fill(black)

        frame = vs.read()

        frame = imutils.resize(frame, width = 300)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) # resize the frame, blur it, and convert it to the HSV color space
        maskColor = cv2.inRange(hsv, lower, upper) # mask for color
        kernel = np.ones((5, 5), np.uint8)
        noiseRemove = cv2.morphologyEx(maskColor, cv2.MORPH_OPEN, kernel) # removing noise
        mask = cv2.dilate(noiseRemove, None, iterations = 2) # increasing white masked region

        contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = imutils.grab_contours(contour) # find contours in the mask and initialize the current (x, y) center of the ball

        center = None

        if len(contour) > 0:
            outline = list(bgrHex)
            for i in range(3):
                if outline[i] == 255:
                    pass
                elif i >= 1:
                    outline[i] += 150
                else:
                    outline[i] += 100
            
            circle = max(contour, key = cv2.contourArea) # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
            ((x, y), radius) = cv2.minEnclosingCircle(circle) # finds minimal enclosing circle of 2D point set
            M = cv2.moments(circle) # finds "center of mass"; parameters include 
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) # finds center of most intense points
            
            if radius > 5:
                radList.insert(0, radius)
                points.appendleft(center)
                cv2.circle(frame, (int(x), int(y)), int(radius), tuple(outline), 2) # draw the circle and centroid on the frame, then update the list of tracked points
                cv2.circle(frame, center, 5, tuple(outline), -1)
    
        for i in range(1, len(points)):
            if points[i - 1] is None or points[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 0.75) # compute the thickness of the line and draw the connecting lines
            cv2.line(frame, points[i - 1], points[i], bgrHex, thickness)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frameX, frameY = (displayWidth/2 - fWidth/2), 10
        screen.blit(frame, (10, frameY))
        myDisplay.blit(direc, (dX, dY))
        myDisplay.blit(reset, (rX, rY))

        if len(radList) > 0:
            pts = pointFormat(radList, points)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        quit()
                view.rotate(event)

            for edge in edges:
                drawpoints = []
                for x, y, z in vertices[edge[0]], vertices[edge[1]]:
                    x, z = rotateCube((x, z), view.rot[1])
                    y, z = rotateCube((y, z), view.rot[0])
                    z += 10
                    d = 250/z
                    x, y = x*d*view.scale, y*d*view.scale 
                    drawpoints += [(cx+int(x), cy+int(y))]
                if not(edge == (0,1) or edge == (1,2) or edge == (2,6) or edge == (0,4) or edge == (4,5) or
                    edge == (1,5) or edge == (6,7) or edge == (7,4) or edge == (5,6)):
                    pygame.draw.line(myDisplay, white, drawpoints[0], drawpoints[1], 1)

            for x, y, z in pts:
                y *= -1
                z += 5
                f = 200/z
                x, y = x * (view.scale - 1.1), y * (view.scale - 1.1)
                z *= -1
                z *= (view.scale - 1.25)
                y, z = z, y
                x, z = rotateCube((x,z), view.rot[1])
                y, z = rotateCube((y,z), view.rot[0])
                pygame.draw.circle(myDisplay, hx, (cx+int(x), cy+int(y)), 6)
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        quit()
                view.rotate(event)
            if not (yT and zT < 81):
                for edge in edges:
                    drawpoints = []
                    for x, y, z in vertices[edge[0]], vertices[edge[1]]:
                        x, z = rotateCube((x, z), view.rot[1])
                        y, z = rotateCube((y, z), view.rot[0])
                        z += 10
                        d = 250/z
                        x, y = x*d*view.scale, y*d*view.scale
                        drawpoints += [(cx+int(x), cy+int(y))]
                    if not(edge == (0,1) or edge == (1,2) or edge == (2,6) or edge == (0,4) or edge == (4,5) or
                        edge == (1,5) or edge == (6,7) or edge == (7,4) or edge == (5,6)):
                        pygame.draw.line(myDisplay, white, drawpoints[0], drawpoints[1], 1)

            pygame.display.flip()

        pygame.display.update()


def colorGetter(color):
    # allows user to choose the color they want to track; BLUE, GREEN, RED
    if color == 'red':
        lower, upper = (150, 150, 70), (180, 255, 255)
        bgrHex = (0, 0, 255)
    elif color == 'green':
        lower, upper = (29, 86, 6), (64, 255, 255)
        bgrHex = (0, 255, 0)
    elif color == 'blue':
        lower, upper = (100, 50, 50), (130, 255, 255)
        bgrHex = (255, 0, 0)
    return (color, bgrHex), lower, upper


# referenced from https://gist.github.com/radames/1e7c794842755683162b
# heavily influenced by https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
def colorTracer(color):
    # tracks what the user is drawing (how large an object is to remember depth and position of object on the screen)
    clr = color
    (color, bgrHex), lower, upper = colorGetter(color)

    argp = argparse.ArgumentParser() # easy to write user-friendly command-line interfaces --> defines what arguments it requires
    argp.add_argument("-b", "--buffer", type = int, default = 5000, help = "max buffer size") # tells argumentparser how to take strings on command line --> objects
    args = vars(argp.parse_args()) # returns object with two attributes (integers, accumulate); list of one or more ints, accumulate max()
    points = deque(maxlen = args["buffer"])
    vs = VideoStream(src = 0).start()
    radList = []

    screen = pygame.display.set_mode([displayWidth, displayHeight])
    fWidth = frameWidth - 80

    back = pygame.image.load('images/back_draw.png')
    back1 = pygame.image.load('images/back_draw_1.png')
    scale = 0.75
    backDimX, backDimY = back.get_rect().size
    backDimX, backDimY = int(scale*backDimX), int(scale*backDimY)
    back = pygame.transform.scale(back, (backDimX, backDimY))
    back1 = pygame.transform.scale(back1, (backDimX, backDimY))
    backX, backY = (displayWidth - 3*backDimX) / 4, displayHeight - backDimY - 50

    reset = pygame.image.load('images/reset.png')
    reset1 = pygame.image.load('images/reset_1.png')
    reset = pygame.transform.scale(reset, (backDimX, backDimY))
    reset1 = pygame.transform.scale(reset1, (backDimX, backDimY))
    resetX, resetY = displayWidth/2 - backDimX/2, displayHeight - backDimY - 50

    finish = pygame.image.load('images/finish.png')
    finish1 = pygame.image.load('images/finish_1.png')
    finish = pygame.transform.scale(finish, (backDimX, backDimY))
    finish1 = pygame.transform.scale(finish1, (backDimX, backDimY))
    finishX, finishY = resetX + backDimX + backX, displayHeight - backDimY - 50

    notdrawn = pygame.image.load('images/notdrawn.png')
    scale = 1.25
    ndDimX, ndDimY = notdrawn.get_rect().size
    ndDimX, ndDimY = int(scale*ndDimX), int(scale*ndDimY)
    notdrawn = pygame.transform.scale(notdrawn, (ndDimX, ndDimY))
    notdrawnX, notdrawnY = displayWidth/2 - ndDimX/2, 175

    yT, zT = False, 0

    while True:
        frame = vs.read()
        screen.fill(black)

        frame = imutils.resize(frame, width = fWidth)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        maskColor = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        noiseRemove = cv2.morphologyEx(maskColor, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(noiseRemove, None, iterations = 2)

        contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = imutils.grab_contours(contour)

        center = None

        if len(contour) > 0:
            outline = list(bgrHex)
            for i in range(3):
                if outline[i] == 255:
                    pass
                elif i >= 1:
                    outline[i] += 150
                else:
                    outline[i] += 100
            
            circle = max(contour, key = cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(circle)
            M = cv2.moments(circle)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            if radius > 5:
                radList.insert(0, radius)
                points.appendleft(center)
                cv2.circle(frame, (int(x), int(y)), int(radius), tuple(outline), 2)
                cv2.circle(frame, center, 5, tuple(outline), -1)
    
        for i in range(1, len(points)):
            if points[i - 1] is None or points[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 0.75)
            cv2.line(frame, points[i - 1], points[i], bgrHex, thickness)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frameX, frameY = (displayWidth/2 - fWidth/2), 10
        screen.blit(frame, (frameX, frameY))

        myDisplay.blit(back, (backX, backY))
        myDisplay.blit(reset, (resetX, resetY))
        myDisplay.blit(finish, (finishX, finishY))
        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()[0]

        if (backX < mousePos[0] < backX + backDimX) and (backY < mousePos[1] < backY + backDimY):
            myDisplay.blit(frame, (frameX, frameY))
            myDisplay.blit(back1, (backX, backY))
            if mouse:
                for n in range(0, 300, 15):
                    fade.set_alpha(n)
                    myDisplay.blit(frame, (frameX, frameY))
                    myDisplay.blit(back1, (backX, backY))
                    myDisplay.blit(reset, (resetX, resetY))
                    myDisplay.blit(finish, (finishX, finishY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                vs.stream.release()
                color = tips(clr)
                return colorTracer(color)

        elif (resetX < mousePos[0] < resetX + backDimX) and (resetY < mousePos[1] < resetY + backDimY):
            myDisplay.blit(frame, (frameX, frameY))
            myDisplay.blit(reset1, (resetX, resetY))
            if mouse:
                for n in range(0, 300, 20):
                    fade.set_alpha(n)
                    myDisplay.blit(frame, (frameX, frameY))
                    myDisplay.blit(back, (backX, backY))
                    myDisplay.blit(reset1, (resetX, resetY))
                    myDisplay.blit(finish, (finishX, finishY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                vs.stream.release()
                radList, points, color = colorTracer(color)
                return radList, points, color

        elif (finishX < mousePos[0] < finishX + backDimX) and (finishY < mousePos[1] < finishY + backDimY):
            myDisplay.blit(frame, (frameX, frameY))
            myDisplay.blit(finish1, (finishX, finishY))
            if mouse:
                if len(radList) == 0:
                    myDisplay.blit(notdrawn, (notdrawnX, notdrawnY))
                    yT = True
                    zT = 0
                else:
                    for n in range(0, 300, 15):
                        fade.set_alpha(n)
                        myDisplay.blit(frame, (frameX, frameY))
                        myDisplay.blit(back, (backX, backY))
                        myDisplay.blit(reset, (resetX, resetY))
                        myDisplay.blit(finish1, (finishX, finishY))
                        myDisplay.blit(fade, (0, 0))
                        pygame.display.update()
                    myDisplay.fill(black)
                    pygame.display.update()
                    vs.stream.release()
                    return radList, points, color
        
        if yT and zT < 81:
            myDisplay.blit(notdrawn, (notdrawnX, notdrawnY))
            zT += 1
            print(zT)
            if zT == 80:
                zT == 0
                yT = False

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                vs.stream.release()
                quit()


def tipsManual():
    # screen that shows some tips to generate a nice graph of what the user draws
    tipsL = pygame.image.load('images/tips_2.png')
    tipsL1 = pygame.image.load('images/tips_3.png')

    scale = 1.5
    tipsDimX, tipsDimY = tipsL.get_rect().size
    tipsDimX, tipsDimY = int(scale*tipsDimX), int(scale*tipsDimY)
    tipsL = pygame.transform.scale(tipsL, (tipsDimX, tipsDimY))

    scale = 0.9
    tipsLDimX, tipsLDimY = tipsL1.get_rect().size
    tipsLDimX, tipsLDimY = int(scale*tipsLDimX), int(scale*tipsLDimY)
    tipsL1 = pygame.transform.scale(tipsL1, (tipsLDimX, tipsLDimY))
    tipsTX, tipsTY = displayWidth/2 - tipsDimX/2, 50
    tipsLX, tipsLY = displayWidth/2 - tipsLDimX/2, 110

    backb = pygame.image.load('images/back.png')
    back1 = pygame.image.load('images/back_1.png')
    scale = 0.15
    backDimX, backDimY = backb.get_rect().size
    backDimX, backDimY = int(scale*backDimX), int(scale*backDimY)
    backb = pygame.transform.scale(backb, (backDimX, backDimY))
    back1 = pygame.transform.scale(back1, (backDimX, backDimY))
    backX, backY = 10, displayHeight - backDimY - 10

    myDisplay.fill(black)
    myDisplay.blit(tipsL, (tipsTX, tipsTY))
    myDisplay.blit(tipsL1, (tipsLX, tipsLY))
    myDisplay.blit(backb, (backX, backY))
    pygame.display.update()

    for n in range(300, 0, -20):
        fade.set_alpha(n)
        myDisplay.blit(tipsL, (tipsTX, tipsTY))
        myDisplay.blit(tipsL1, (tipsLX, tipsLY))
        myDisplay.blit(backb, (backX, backY))
        myDisplay.blit(fade, (0, 0))
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        myDisplay.blit(tipsL, (tipsTX, tipsTY))
        myDisplay.blit(tipsL1, (tipsLX, tipsLY))
        myDisplay.blit(backb, (backX, backY))
        
        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()[0]

        if (backX < mousePos[0] < backX + backDimX) and (backY < mousePos[1] < backY + backDimY):
            myDisplay.blit(back1, (backX, backY))
            if mouse:
                for n in range(0, 300, 20):
                    fade.set_alpha(n)
                    myDisplay.blit(tipsL, (tipsTX, tipsTY))
                    myDisplay.blit(tipsL1, (tipsLX, tipsLY))
                    myDisplay.blit(back1, (backX, backY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                return
        pygame.display.update()


def tips(color):
    # displays whether to go back to color choosing screen, retrieve some tips, or continue to draw
    myDisplay.fill(black)
    backb = pygame.image.load('images/back.png')
    back1 = pygame.image.load('images/back_2.png')
    scale = 0.25
    backDimX, backDimY = backb.get_rect().size
    backDimX, backDimY = int(scale*backDimX), int(scale*backDimY)
    backb = pygame.transform.scale(backb, (backDimX, backDimY))
    back1 = pygame.transform.scale(back1, (backDimX, backDimY))
    backX, backY = (displayWidth - 3*backDimX) / 4, displayHeight/2 - backDimY/2

    drawb = pygame.image.load('images/draw.png')
    draw1 = pygame.image.load('images/draw_1.png')
    drawb = pygame.transform.scale(drawb, (backDimX, backDimY))
    draw1 = pygame.transform.scale(draw1, (backDimX, backDimY))
    drawX, drawY = displayWidth/2 - backDimX/2, displayHeight/2 - backDimY/2

    tips = pygame.image.load('images/tips.png')
    tips1 = pygame.image.load('images/tips_1.png')
    tips = pygame.transform.scale(tips, (backDimX, backDimY))
    tips1 = pygame.transform.scale(tips1, (backDimX, backDimY))
    tipsX, tipsY = drawX + backDimX + backX, displayHeight/2 - backDimY/2
    
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        myDisplay.fill(black)
        myDisplay.blit(backb, (backX, backY))
        myDisplay.blit(drawb, (drawX, drawY))
        myDisplay.blit(tips, (tipsX, tipsY))
        
        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()[0]

        if (backX < mousePos[0] < backX + backDimX) and (backY < mousePos[1] < backY + backDimY):
            myDisplay.fill(black)
            myDisplay.blit(back1, (backX, backY))
            myDisplay.blit(drawb, (drawX, drawY))
            myDisplay.blit(tips, (tipsX, tipsY))
            if mouse:
                for n in range(0, 300, 15):
                    fade.set_alpha(n)
                    myDisplay.blit(back1, (backX, backY))
                    myDisplay.blit(drawb, (drawX, drawY))
                    myDisplay.blit(tips, (tipsX, tipsY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                color = colorChooser()
                for n in range(300, 0, -2):
                    fade.set_alpha(n)
                    myDisplay.blit(backb, (backX, backY))
                    myDisplay.blit(drawb, (drawX, drawY))
                    myDisplay.blit(tips, (tipsX, tipsY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()

        elif (drawX < mousePos[0] < drawX + backDimX) and (drawY < mousePos[1] < drawY + backDimY):
            myDisplay.blit(draw1, (drawX, drawY))
            if mouse:
                for n in range(0, 300, 15):
                    fade.set_alpha(n)
                    myDisplay.blit(backb, (backX, backY))
                    myDisplay.blit(draw1, (drawX, drawY))
                    myDisplay.blit(tips, (tipsX, tipsY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                return color

        elif (tipsX < mousePos[0] < tipsX + backDimX) and (tipsY < mousePos[1] < tipsY + backDimY):
            myDisplay.blit(tips1, (tipsX, tipsY))
            if mouse:
                for n in range(0, 300, 15):
                    fade.set_alpha(n)
                    myDisplay.blit(backb, (backX, backY))
                    myDisplay.blit(drawb, (drawX, drawY))
                    myDisplay.blit(tips1, (tipsX, tipsY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                tipsManual()

        pygame.display.update()


def chooseToDraw():
    # screen hyping user up to draw; this will go ito the "tips page"
    myDisplay.fill(black)
    chooseToDraw = pygame.image.load('images/choosetodraw.png')
    chooseToDraw1 = pygame.image.load('images/choosetodraw_1.png')
    scale = 0.6
    cTDDimX, cTDDimY = chooseToDraw.get_rect().size
    cTDDimX, cTDDimY = int(scale*cTDDimX), int(scale*cTDDimY)
    chooseToDraw = pygame.transform.scale(chooseToDraw, (cTDDimX - 10, cTDDimY))
    chooseToDraw1 = pygame.transform.scale(chooseToDraw1, (cTDDimX - 10, cTDDimY))
    cTDX, cTDY = displayWidth/2 - cTDDimX/2, displayHeight/2 - cTDDimY/2

    time.sleep(0.5)
    
    for n in range(300, 0, -2):
        fade.set_alpha(n)
        myDisplay.blit(chooseToDraw, (cTDX, cTDY))
        myDisplay.blit(fade, (cTDX, cTDY))
        pygame.display.update()

    time.sleep(0.75)

    for n in range(300, 0, -2):
        fade.set_alpha(n)
        myDisplay.blit(chooseToDraw1, (cTDX + 10, cTDY))
        myDisplay.blit(fade, (cTDX, cTDY + 50))
        pygame.display.update()
    
    time.sleep(1.25)
    
    for n in range(0, 300, 2):
        fade.set_alpha(n)
        myDisplay.blit(chooseToDraw, (cTDX, cTDY))
        myDisplay.blit(chooseToDraw1, (cTDX + 10, cTDY))
        myDisplay.blit(fade, (cTDX, cTDY))
        pygame.display.update()
    
    time.sleep(0.5)


def choosechoose(color):
    # menu that allows the user to choose whether they want to draw with a live grapher or not
    draw = pygame.image.load('images/drawq.png')
    scale = 1
    dDimX, dDimY = draw.get_rect().size
    dDimX, dDimY = int(scale*dDimX), int(scale*dDimY)
    draw = pygame.transform.scale(draw, (dDimX, dDimY))
    qX, qY = displayWidth/2 - dDimX/2, displayHeight/2 - 100

    yes = pygame.image.load('images/yes.png')
    yes1 = pygame.image.load('images/yes_1.png')

    no = pygame.image.load('images/no.png')
    no1 = pygame.image.load('images/no_1.png')

    scale = 1
    bDimX, bDimY = yes.get_rect().size
    bDimX, bDimY = int(scale*bDimX), int(scale*bDimY)
    yes = pygame.transform.scale(yes, (bDimX, bDimY))
    yes1 = pygame.transform.scale(yes1, (bDimX, bDimY))
    no = pygame.transform.scale(no, (bDimX, bDimY))
    no1 = pygame.transform.scale(no1, (bDimX, bDimY))
    yX, yY = displayWidth/3 - bDimX/2, displayHeight/2 + 50
    nX, nY = displayWidth*(2/3) - bDimX/2, yY

    for n in range(300, 0, -3):
        fade.set_alpha(n)
        myDisplay.blit(draw, (qX, qY))
        myDisplay.blit(yes, (yX, yY))
        myDisplay.blit(no, (nX, nY))
        myDisplay.blit(fade, (0, 0))
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        myDisplay.blit(draw, (qX, qY))
        myDisplay.blit(draw, (qX, qY))
        myDisplay.blit(yes, (yX, yY))
        myDisplay.blit(no, (nX, nY))
        
        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()[0]

        if (yX < mousePos[0] < yX + bDimX) and (yY < mousePos[1] < yY + bDimY):
            myDisplay.blit(yes1, (yX, yY))
            if mouse:
                for n in range(0, 300, 8):
                    fade.set_alpha(n)
                    myDisplay.blit(draw, (qX, qY))
                    myDisplay.blit(yes1, (yX, yY))
                    myDisplay.blit(no, (nX, nY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                chooseToDraw()
                pts = liveDraw(color)
                drawToView()
                colorHex = graphColor(color)
                viewChooser(pts, colorHex)
                end()
        elif (nX < mousePos[0] < nX + bDimX) and (nY < mousePos[1] < nY + bDimY):
            myDisplay.blit(no1, (nX, nY))
            if mouse:
                for n in range(0, 300, 8):
                    fade.set_alpha(n)
                    myDisplay.blit(draw, (qX, qY))
                    myDisplay.blit(yes, (yX, yY))
                    myDisplay.blit(no1, (nX, nY))
                    myDisplay.blit(fade, (0, 0))
                    pygame.display.update()
                return

        pygame.display.update()


def colorRange(color):
    # returns the color range of red, green, and blue for the choosing screen
    if color == 'r':
        lRed, uRed = (150, 150, 70), (180, 255, 255)
        return lRed, uRed
    elif color == 'g':
        lGreen, uGreen = (29, 86, 6), (64, 255, 255)
        return lGreen, uGreen
    elif color == 'b':
        lBlue, uBlue = (100, 50, 50), (130, 255, 255)
        return lBlue, uBlue


"""
vv complex to fit openCV with pygame
"""

# referenced from https://gist.github.com/radames/1e7c794842755683162b
# tips and code inspriation from https://github.com/CJoseFlores/python-OpenCV-Zoom/blob/master/VidStream.py
def colorChooser():
    # screen that allows users to choose what color their drawing utensil is;
    argp = argparse.ArgumentParser()
    argp.add_argument("-b", "--buffer", type = int, default = 5000, help = "max buffer size")
    args = vars(argp.parse_args())
    points = deque(maxlen = args["buffer"])

    vs = VideoStream(src = 0).start()
    screen = pygame.display.set_mode([displayWidth, displayHeight])

    cWidth, cHeight = 320, 260

    directions = pygame.image.load('images/directions_2.png')
    dirDimX, dirDimY = directions.get_rect().size
    scale = 0.80
    dirDimX, dirDimY = int(scale*dirDimX), int(scale*dirDimY)
    directions = pygame.transform.scale(directions, (dirDimX, dirDimY))
    dirX, dirY = displayWidth/2 - dirDimX/2, displayHeight/10 - dirDimY/2 + 10

    rectangle = pygame.image.load('images/rectchoose.png').convert()
    rectangle.set_alpha(200)
    rectDimX, rectDimY = rectangle.get_rect().size
    scale = 1.03
    rectDimX, rectDimY = int(scale*rectDimX), int((scale - 0.25)*rectDimX)
    rectangle = pygame.transform.scale(rectangle, (rectDimX, rectDimY))

    while True:
        cam1X, cam1Y = (displayWidth - (cWidth*2))/3, (displayHeight*(4/5) - 2*cHeight)/3 + displayHeight/5
        cam2X, cam2Y = (cam1X*2) + cWidth, cam1Y
        cam3X, cam3Y = displayWidth/2 - cWidth/2, cam1Y + cHeight + ((displayHeight*(4/5) - 2*cHeight)/3)
        # cam4X, cam4Y = cam2X, cam3Y

        frame = vs.read()
        screen.fill(black)
        myDisplay.blit(directions, (dirX, dirY + 10))

        ######## RED ########
        rLower, rUpper = colorRange('r')
        rframe = imutils.resize(frame, width = cWidth)
        blurred = cv2.GaussianBlur(rframe, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        maskColor = cv2.inRange(hsv, rLower, rUpper)
        kernel = np.ones((5, 5), np.uint8)
        noiseRemove = cv2.morphologyEx(maskColor, cv2.MORPH_OPEN, kernel)
        rmask = cv2.dilate(noiseRemove, None, iterations = 2)
        res = cv2.bitwise_and(rframe, rframe, mask = rmask)
        rframe = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        rframe = np.rot90(rframe)
        rframe = pygame.surfarray.make_surface(rframe)
        myDisplay.blit(rectangle, (cam1X - 20, cam1Y))
        screen.blit(rframe, (cam1X - 10, cam1Y + 10))

        ######## GREEN ########
        gLower, gUpper = colorRange('g')
        gframe = imutils.resize(frame, width = cWidth)
        gblurred = cv2.GaussianBlur(frame, (11, 11), 0)
        ghsv = cv2.cvtColor(gblurred, cv2.COLOR_BGR2HSV)
        gmaskColor = cv2.inRange(hsv, gLower, gUpper)
        gnoiseRemove = cv2.morphologyEx(gmaskColor, cv2.MORPH_OPEN, kernel)
        gmask = cv2.dilate(gnoiseRemove, None, iterations = 2)
        gres = cv2.bitwise_and(gframe, gframe, mask = gmask)
        gframe = cv2.cvtColor(gres, cv2.COLOR_BGR2RGB)
        gframe = np.rot90(gframe)
        gframe = pygame.surfarray.make_surface(gframe)
        myDisplay.blit(rectangle, (cam2X - 10, cam2Y))
        screen.blit(gframe, (cam2X, cam2Y + 10))

        ######## BLUE ########
        bLower, bUpper = colorRange('b')
        bframe = imutils.resize(frame, width = cWidth)
        bblurred = cv2.GaussianBlur(frame, (11, 11), 0)
        bhsv = cv2.cvtColor(bblurred, cv2.COLOR_BGR2HSV)
        bmaskColor = cv2.inRange(hsv, bLower, bUpper)
        bnoiseRemove = cv2.morphologyEx(bmaskColor, cv2.MORPH_OPEN, kernel)
        bmask = cv2.dilate(bnoiseRemove, None, iterations = 2)
        bres = cv2.bitwise_and(bframe, bframe, mask = bmask)
        bframe = cv2.cvtColor(bres, cv2.COLOR_BGR2RGB)
        bframe = np.rot90(bframe)
        bframe = pygame.surfarray.make_surface(bframe)
        myDisplay.blit(rectangle, (cam3X - 20, cam3Y))
        screen.blit(bframe, (cam3X - 10, cam3Y + 10))

        pygame.display.update()

        mouse = pygame.mouse.get_pressed()[0]
        mousePos = pygame.mouse.get_pos()
        
        if (cam1X < mousePos[0] < cam1X+cWidth) and (cam1Y < mousePos[1] < cam1Y+cHeight) and mouse:
            vs.stream.release()
            return 'red'
        elif (cam2X < mousePos[0] < cam2X+cWidth) and (cam2Y < mousePos[1] < cam2Y+cHeight) and mouse:
            vs.stream.release()
            return 'green'
        elif (cam3X < mousePos[0] < cam3X+cWidth) and (cam3Y < mousePos[1] < cam3Y+cHeight) and mouse:
            vs.stream.release()
            return 'blue'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                vs.stream.release()
                quit()


def startToChoose():
    # displays a line of directions to get user ready for next screen
    directions = pygame.image.load('images/directions_1.png')
    dirDimX, dirDimY = directions.get_rect().size
    scale = 0.5
    dirDimX, dirDimY = int(scale*dirDimX), int(scale*dirDimY) - 10
    directions = pygame.transform.scale(directions, (dirDimX, dirDimY))
    dirX, dirY = displayWidth/2 - dirDimX/2, displayHeight/2 - dirDimY/2
    myDisplay.blit(directions, (dirX, dirY))
    
    for n in range(300, 0, -15):
        fade.set_alpha(n)
        myDisplay.blit(directions, (dirX, dirY))
        myDisplay.blit(fade, (dirX, dirY))
        pygame.display.update()

    time.sleep(3)
    
    for n in range(0, 300, 2):
        fade.set_alpha(n)
        myDisplay.blit(directions, (dirX, dirY))
        myDisplay.blit(fade, (dirX, dirY))
        pygame.display.update()

    pygame.display.update()


cubeVertices = (-1,-1,1),(-1,1,1),(1,1,1),(1,-1,1),(-1,-1,-1),(-1,1,-1),(1,1,-1),(1,-1,-1)
cubeX, cubeY = displayWidth/2, displayHeight/2

class cubed:
    # class for rotating cube on start menu
    def __init__(self, position = (0,0,0), rotation = (0,0), scale = 0.00001):
        self.pos = list(position)
        self.rot = list(rotation)
        self.scale = scale


def rotateCube(pos, rad):
    x, y = pos
    s, c = math.sin(rad), math.cos(rad)
    return x*c - y*s, y*c + x*s


# inspired by https://github.com/demaisj/Pygame-Transitions/blob/master/transitions.py
def startMenu(width, height):
    # start menu with minimalistic graphics; user can choose when to start ('start')
    introImage = pygame.image.load('images/startmenu.png')
    startButton = pygame.image.load('images/start_1.png')
    startPButton = pygame.image.load('images/start_2.png')

    scale = 1.75
    imageDimX, imageDimY = introImage.get_rect().size
    imageDimX, imageDimY = int(scale*imageDimX), int(scale*imageDimY)
    introImage = pygame.transform.scale(introImage, (imageDimX, imageDimY))
    imageX = displayWidth/2 - imageDimX/2 + 10
    imageY = height/2 - imageDimY*(7/8)

    scale_b = 2
    buttonDimX, buttonDimY = startButton.get_rect().size
    startButton = pygame.transform.scale(startButton, (buttonDimX, buttonDimY))
    buttonX, buttonY = (displayWidth/2 - buttonDimX/2), (height/2 + imageDimY*(1/3))

    if imageDimY != height:
        if imageDimY > height:
            scale = height/imageDimY
        else:
            scale = imageDimY/height

    myDisplay.fill(black)
    pygame.display.update()

    radian = 0
    cube = cubed((0, 0, 0.5))
    increase = True
    num = random.randint(1, 6)

    while True:
        t = clock.tick()/2000
        radian += 2*t

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if cube.scale > num:
            increase = False
        elif cube.scale < 0.00001:
            increase = True
        if increase:
            cube.scale += 0.0005
        else:
            cube.scale -= 0.001

        myDisplay.fill(black)
        
        for edge in edges:
            points = []
            for x, y, z in cubeVertices[edge[0]], cubeVertices[edge[1]]:
                x += cube.pos[0]
                y += cube.pos[1]
                z += cube.pos[2]
                x, z = rotateCube((x, z), radian)
                y, z = rotateCube((y, z), radian)
                z += 5
                if z != 0:
                    d = 250 / z
                x, y = x * d * cube.scale, y * d * cube.scale
                points += [(cubeX + int(x), cubeY + int(y))]

            pygame.draw.line(myDisplay, (100, 100, 100), points[0], points[1], 2)

        myDisplay.blit(introImage, (imageX, imageY))
        myDisplay.blit(startButton, (buttonX, buttonY))
        mousePos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()[0]

        buttonBX, buttonBY = buttonX + buttonDimX, buttonY + buttonDimY
        if (buttonX < mousePos[0] < buttonBX) and (buttonY < mousePos[1] < buttonBY):
            myDisplay.blit(startPButton, (buttonX, buttonY))
            if mouse:
                for n in range(0, 300, 10):
                    fade.set_alpha(n)
                    myDisplay.blit(introImage, (imageX, imageY))
                    myDisplay.blit(startButton, (buttonX, buttonY))
                    myDisplay.blit(fade, (imageX, imageY))
                    pygame.display.update()
                return
        pygame.display.update()


def splashScreen(width, height):
    # first screen users see, displays app's title
    myDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('images/dimensional drawer')
    introImage = pygame.image.load('images/startmenu.png')
    scale = 1
    imageDimX, imageDimY = introImage.get_rect().size
    if imageDimY != height:
        if imageDimY < height:
            scale = height/imageDimY
            scale -= 1
        else:
            scale = imageDimY/height
    imageDimX, imageDimY = int(scale*imageDimX), int(scale*imageDimY)
    introImage = pygame.transform.scale(introImage, (imageDimX, imageDimY))
    imageX = -(imageDimX - displayWidth)/2 + 10
    imageY = height/2 - imageDimY/2

    myDisplay.fill(black)
    myDisplay.blit(introImage, (imageX, imageY))
    pygame.display.update()
    time.sleep(1)
    
    for n in range(0, 300, 5):
        fade.set_alpha(n)
        myDisplay.blit(introImage, (imageX, imageY))
        myDisplay.blit(fade, (imageX, imageY))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


'''
starting app:
1.   splash screen
2.   start menu
3.   between start menu and choose screen
4.   screen to choose which color to track
5.   between choose menu to draw screen with added tips
6.   transition screen
7.   transition screen with "back," "draw," "tips"
8.   tracing and tracking the user's motion
9.   transition screen
10.  formats the points retrieved from the tracing function
11.  gathers the color of what will be graphed
12.  screen to choose what view the graph will be seen in
13.  the end!
'''

splashScreen(displayWidth, displayHeight)   # 1
color = startMenu(displayWidth, displayHeight)   # 2
startToChoose()   # 3
color = colorChooser()   # 4
choosechoose(color)   # 5
chooseToDraw()  # 6
color = tips(color)   # 7
radList, points, color = colorTracer(color)   # 8
drawToView()   # 9
pts = pointFormat(radList, points)   # 10
colorHex = graphColor(color)   # 11
viewChooser(pts, colorHex)   # 12
end()   # 13

pygame.quit()
quit()

