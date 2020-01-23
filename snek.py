import pygame, sys, random, time
from pygame.locals import *

pygame.init()
# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 40  # number of columns in the board
BOARDHEIGHT = 40  # number of rows in the board
WINDOWWIDTH = 750
WINDOWHEIGHT = 750
TILESIZE = int(1000 / 40)
FPS = 60
BLANK = None

#                 R    G    B
BLACK =          (  0,   0,   0)
WHITE =          (255, 255, 255)
DARKGREY =       ( 64,  64,  64)
GREY =           (178, 178, 178)
BLUE =           ( 64,  64, 255)
LIGHTBLUE =      (178, 178, 255)
GREYTAN =        (178, 166, 153)
LIGHTGREEN =     (178, 255, 178)
GREEN =          ( 64, 255,  64)
ORANGE =         (255, 179,  25)

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
DRAWSURF = pygame.Surface((1000,1000))
DRAWSURF.fill(BLUE)
BASICFONTSIZE = 27
BIGFONTSIZE = 50
BIGFONT = pygame.font.Font('freesansbold.ttf', BIGFONTSIZE)
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
board = []
snake1 = []
snake2 = []
TWOPLAYER = False
MENU = True
SPEED_UP = False
GAMEOVER = False
TRON = False
STATICRECT = pygame.Rect(-1, -1, 100, 200)
SPEEDRECT = pygame.Rect(-1, -1, 100, 200)
MULTIPLAYERRECT = pygame.Rect(-1, -1, 100, 200)
TRONRECT = pygame.Rect(-1, -1, 100, 200)
STATICBUTTON = BASICFONT.render("NO SPEED UP", True, BLACK, LIGHTGREEN)
SPEEDBUTTON = BASICFONT.render("SPEED UP", True, BLACK, LIGHTGREEN)
MULTIPLAYERBUTTON = BASICFONT.render("2 Players", True, BLACK, LIGHTGREEN)
TRONBUTTON = BASICFONT.render("TRON", True, BLACK, LIGHTGREEN)
BOARD = []
SNEKS = []


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT, DRAWSURF, MENU, SPEED_UP, STATICRECT, SPEEDRECT, MULTIPLAYERRECT, TWOPLAYER, GAMEOVER, BOARD, TRON
    MENU = True

    clickpos = (-2, -2)

    while True:
        clickpos = (-2, -2)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and not MENU and not GAMEOVER:
                if not TWOPLAYER:
                    if event.key in (K_UP, K_w) and not SNEKS[0].direction == DOWN:
                        SNEKS[0].direction = UP
                    elif event.key in (K_LEFT, K_a) and not SNEKS[0].direction == RIGHT:
                        SNEKS[0].direction = LEFT
                    elif event.key in (K_RIGHT, K_d) and not SNEKS[0].direction == LEFT:
                        SNEKS[0].direction = RIGHT
                    elif event.key in (K_DOWN, K_s) and not SNEKS[0].direction == UP:
                        SNEKS[0].direction = DOWN
                else:
                    if event.key == K_UP and not SNEKS[0].direction == DOWN:
                        SNEKS[0].direction = UP
                    elif event.key == K_LEFT and not SNEKS[0].direction == RIGHT:
                        SNEKS[0].direction = LEFT
                    elif event.key == K_RIGHT and not SNEKS[0].direction == LEFT:
                        SNEKS[0].direction = RIGHT
                    elif event.key == K_DOWN and not SNEKS[0].direction == UP:
                        SNEKS[0].direction = DOWN
                    if event.key == K_w and not SNEKS[1].direction == DOWN:
                        SNEKS[1].direction = UP
                    elif event.key == K_a and not SNEKS[1].direction == RIGHT:
                        SNEKS[1].direction = LEFT
                    elif event.key == K_d and not SNEKS[1].direction == LEFT:
                        SNEKS[1].direction = RIGHT
                    elif event.key == K_s and not SNEKS[1].direction == UP:
                        SNEKS[1].direction = DOWN
            if event.type == KEYDOWN and GAMEOVER:
                if event.key == K_r:
                    TWOPLAYER = False
                    MENU = True
                    SPEED_UP = False
                    GAMEOVER = False
                    TRON = False
                    BOARD = []
                    STATICRECT = pygame.Rect(-1, -1, 100, 200)
                    SPEEDRECT = pygame.Rect(-1, -1, 100, 200)
                    MULTIPLAYERRECT = pygame.Rect(-1, -1, 100, 200)
                    DRAWSURF.fill(BLUE)
                    main()
            elif event.type == VIDEORESIZE:
                WINDOWWIDTH = event.w
                WINDOWHEIGHT = event.h
                DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
                DISPLAYSURF.fill(BLACK)
            elif event.type == MOUSEBUTTONUP:
                clickpos = pygame.mouse.get_pos()
        if MENU:
            buttonColision(clickpos)
            drawButtons()
        elif not GAMEOVER:
            moveSneks()
            drawBoard()
            if not TRON:
                dumpJuice()
            endGame()
        drawSurface()
        pygame.display.update()
        FPSCLOCK.tick()


def drawSurface():

    global DRAWSURF, STATICRECT,SPEEDRECT, MULTIPLAYERRECT, TRONRECT
    if WINDOWWIDTH > WINDOWHEIGHT:
        blitsurf = pygame.transform.scale(DRAWSURF, (WINDOWHEIGHT, WINDOWHEIGHT))
        DISPLAYSURF.blit(blitsurf, (WINDOWWIDTH/2 - WINDOWHEIGHT/2, 0))
        if MENU:
            STATICRECT = pygame.Rect((WINDOWWIDTH/2 - WINDOWHEIGHT/2) + 250 *(WINDOWHEIGHT/1000), 350 *(WINDOWHEIGHT/1000), 200 *(WINDOWHEIGHT/1000), 100*(WINDOWHEIGHT/1000))
            SPEEDRECT = pygame.Rect((WINDOWWIDTH/2 - WINDOWHEIGHT/2) + 550 *(WINDOWHEIGHT/1000), 350 *(WINDOWHEIGHT/1000), 200 *(WINDOWHEIGHT/1000), 100*(WINDOWHEIGHT/1000))
            MULTIPLAYERRECT = pygame.Rect((WINDOWWIDTH/2 - WINDOWHEIGHT/2) + 550 *(WINDOWHEIGHT/1000), 550 *(WINDOWHEIGHT/1000), 200 *(WINDOWHEIGHT/1000), 100*(WINDOWHEIGHT/1000))
            TRONRECT = pygame.Rect((WINDOWWIDTH/2 - WINDOWHEIGHT/2) + 250 *(WINDOWHEIGHT/1000), 550 *(WINDOWHEIGHT/1000), 200 *(WINDOWHEIGHT/1000), 100*(WINDOWHEIGHT/1000))


    else:
        blitsurf = pygame.transform.scale(DRAWSURF, (WINDOWWIDTH, WINDOWWIDTH))
        DISPLAYSURF.blit(blitsurf, (0, WINDOWHEIGHT / 2 - WINDOWWIDTH / 2))
        if MENU:
            STATICRECT = pygame.Rect(250 *(WINDOWWIDTH/1000), (WINDOWHEIGHT/2 - WINDOWWIDTH/2) + 350 *(WINDOWWIDTH/1000), 200 *(WINDOWWIDTH/1000), 100*(WINDOWWIDTH/1000))
            SPEEDRECT = pygame.Rect(550 *(WINDOWWIDTH/1000), (WINDOWHEIGHT/2 - WINDOWWIDTH/2) + 350 *(WINDOWWIDTH/1000), 200 *(WINDOWWIDTH/1000), 100*(WINDOWWIDTH/1000))
            MULTIPLAYERRECT = pygame.Rect(550 * (WINDOWWIDTH/1000), (WINDOWHEIGHT/2 - WINDOWWIDTH/2) + 550 *(WINDOWWIDTH/1000), 200 *(WINDOWWIDTH/1000), 100*(WINDOWWIDTH/1000))
            TRONRECT = pygame.Rect(250 * (WINDOWWIDTH/1000), (WINDOWHEIGHT/2 - WINDOWWIDTH/2) + 550 *(WINDOWWIDTH/1000), 200 *(WINDOWWIDTH/1000), 100*(WINDOWWIDTH/1000))
    pygame.transform.scale(DRAWSURF, (1000, 1000))


def drawButtons():

    global STATICBUTTON, SPEEDBUTTON, MULTIPLAYERBUTTON, DRAWSURF, TRONBUTTON
    pygame.draw.rect(DRAWSURF, LIGHTGREEN, (250, 350, 200, 100))
    pygame.draw.rect(DRAWSURF, LIGHTGREEN, (550, 350, 200, 100))
    pygame.draw.rect(DRAWSURF, LIGHTGREEN, (250, 550, 200, 100))
    pygame.draw.rect(DRAWSURF, LIGHTGREEN, (550, 550, 200, 100))
    DRAWSURF.blit(STATICBUTTON, (255, 385))
    DRAWSURF.blit(SPEEDBUTTON, (580, 385))
    DRAWSURF.blit(MULTIPLAYERBUTTON, (585, 585))
    DRAWSURF.blit(TRONBUTTON, (290, 585))

def moveSneks():

    for snek in SNEKS:
        if time.time() - snek.lastMove >= snek.moveTime:
            snek.moveSnek()



def buttonColision(point):

    global MENU, SPEED_UP, TWOPLAYER, TRON
    if STATICRECT.collidepoint(point):
        MENU = False
        makeBoard()
    elif SPEEDRECT.collidepoint(point):
        MENU = False
        SPEED_UP = True
        makeBoard()
    elif MULTIPLAYERRECT.collidepoint(point):
        MENU = False
        SPEED_UP = True
        TWOPLAYER = True
        makeBoard()
    elif TRONRECT.collidepoint(point):
        MENU = False
        SPEED_UP = True
        TWOPLAYER = True
        TRON = True
        makeBoard()


class Tile:

    def __init__(self):
        self.tileSurf = pygame.Surface((TILESIZE, TILESIZE))
        self.tileSurf.fill(GREY)
        self.hassnek = False
        self.hasjuice = False

    def giveSnek(self, _sneknum):
        self.hassnek = True
        if _sneknum == 1:
            self.tileSurf.fill(GREEN)
        elif _sneknum == 2:
            self.tileSurf.fill(BLUE)

    def takeSnekTheTakening(self):
        self.hassnek = False
        self.tileSurf.fill(GREY)

    def giveJuice(self):
        self.hasjuice = True
        self.tileSurf.fill(ORANGE)

    def depriveOfJuice(self):
        self.hasjuice = False


class Snek:

    def __init__(self, _playerNum):
        self.playerNum = _playerNum
        self.length = 3
        self.position = []
        self.direction = ''
        self.moveTime = 0.1
        self.lastMove = time.time()
        self.isAlive = True
        if _playerNum == 1:
            self.position = [[30, 20], [31, 20], [32, 20]]
            self.direction = LEFT
        else:
            self.position = [[10, 20], [9, 20], [8, 20]]
            self.direction = RIGHT
        if TRON:
            self.moveTime = 0.075

    def moveSnek(self):
        global BOARD
        temparray = [-1,-1]
        if self.direction == LEFT:
            if not self.position[0][0] - 1 == -1 and not BOARD[self.position[0][0] - 1][self.position[0][1]].hassnek:
                temparray = [self.position[0][0] - 1, self.position[0][1]]
            else:
                self.isAlive = False
        elif self.direction == RIGHT:
            if not self.position[0][0] + 1 == len(BOARD) and not BOARD[self.position[0][0] + 1][self.position[0][1]].hassnek:
                temparray = [self.position[0][0] + 1, self.position[0][1]]
            else:
                self.isAlive = False
        elif self.direction == UP:
            if not self.position[0][1] - 1 == -1 and not BOARD[self.position[0][0]][self.position[0][1] - 1].hassnek:
                temparray = [self.position[0][0], self.position[0][1] - 1]
            else:
                self.isAlive = False
        elif self.direction == DOWN:
            if not self.position[0][1]+1 == len(BOARD[0]) and not BOARD[self.position[0][0]][self.position[0][1] + 1].hassnek:
                temparray = [self.position[0][0], self.position[0][1] + 1]
            else:
                self.isAlive = False
        if self.isAlive:
            self.position.insert(0, temparray)
            BOARD[self.position[0][0]][self.position[0][1]].giveSnek(self.playerNum)
            self.drinkJuice(self.position[0][0], self.position[0][1])

            if not TRON:
                if self.length < len(self.position):
                    BOARD[self.position[len(self.position)-1][0]][self.position[len(self.position)-1][1]].takeSnekTheTakening()
                    self.position.pop()
            self.lastMove = time.time()

    def drinkJuice(self, _xmove, _ymove):
        global BOARD
        if BOARD[_xmove][_ymove].hasjuice:
            self.length += 1
            if SPEED_UP:
                self.moveTime = 0.95 * self.moveTime
            BOARD[_xmove][_ymove].depriveOfJuice()

def dumpJuice():
    global BOARD
    boardJuice = False
    for column in BOARD:
        for square in column:
            if square.hasjuice:
                boardJuice = True

    if not boardJuice:
        juiceLeft = True
        while juiceLeft:
            rand1 = random.randint(0, 39)
            rand2 = random.randint(0, 39)
            if not BOARD[rand1][rand2].hassnek:
                juiceLeft = False
                BOARD[rand1][rand2].giveJuice()


def endGame():

    global DRAWSURF, BOARD, GAMEOVER, SNEKS
    lost_num = -1

    for snek in SNEKS:
        if not snek.isAlive:
            lost_num = snek.playerNum
            GAMEOVER = True

    if GAMEOVER:
        lostSurf = BIGFONT.render("Player " + str(lost_num) + " Lost!", True, BLACK)
        restartSurf = BIGFONT.render("Press R to restart", True, BLACK)
        DRAWSURF.blit(lostSurf, (350, 500))
        DRAWSURF.blit(restartSurf, (350, 600))



def makeBoard():
    global BOARD, SNEKS
    for x in range(BOARDWIDTH):
        tempArray = []
        for y in range(BOARDHEIGHT):
            tempArray.append(Tile())
        BOARD.append(tempArray)

    if TWOPLAYER:
        SNEKS = [Snek(1), Snek(2)]

    else:
        SNEKS = [Snek(1)]

    for snek in SNEKS:
        for position in snek.position:
            BOARD[position[0]][position[1]].giveSnek(snek.playerNum)


def drawBoard():
    global DRAWSURF, BOARD
    for x in range(0, len(BOARD)):
        for y in range(0, len(BOARD[0])):
            DRAWSURF.blit(BOARD[x][y].tileSurf, (x * TILESIZE, y * TILESIZE))









































main()