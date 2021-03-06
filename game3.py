import pygame
pygame.init()
import numpy as np
#the following was written by stefan with edits by philip
win = pygame.display.set_mode((840, 400))
pygame.display.set_caption("ball")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 70)

dc = 0.5

class player(object):
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.xvel = 0
        self.yvel = 0
        self.xacc = 0
        self.yacc = 0


    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), 15)

class ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xvel = 0
        self.yvel = 0
        self.xacc = 0
        self.yacc = 0

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), 10)

def redrawgamewindow():
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (123, 158, 108), (100, 70, 640, 260))
    pygame.draw.rect(win, (123, 158, 108), (70, 145, 30, 110))
    pygame.draw.rect(win, (123, 158, 108), (740, 145, 30, 110))
    pygame.draw.rect(win, (199, 230, 189), (98, 68, 4, 264))
    pygame.draw.rect(win, (199, 230, 189), (738, 68, 4, 264))
    pygame.draw.rect(win, (199, 230, 189), (98, 68, 644, 4))
    pygame.draw.rect(win, (199, 230, 189), (98, 328, 644, 4))
    you.draw(win)
    you2.draw(win)
    b.draw(win)
    string = str(red) + ":" + str(pink)
    text = font.render(string, True, (255, 255, 255))
    win.blit(text, (380, 25))
    pygame.display.update()


def goal(you, you2, b, red, pink):
    if b.x <= 100:
        pink += 1
        you.x = 200
        you.y = 200
        you2.x = 640
        you2.y = 200
        b.x = 420
        b.y = 200
        b.xvel = 0
        b.yvel = 0
        you.xvel = 0
        you.yvel = 0
        you2.xvel = 0
        you2.yvel = 0
    elif b.x >= 740:
        red += 1
        you.x = 200
        you.y = 200
        you2.x = 640
        you2.y = 200
        b.x = 420
        b.y = 200
        b.xvel = 0
        b.yvel = 0
        you.xvel = 0
        you.yvel = 0
        you2.xvel = 0
        you2.yvel = 0

    return [red, pink]


you = player(200, 200, (255,0,0))
you2 = player(640, 200, (0, 0, 255))
b = ball(200, 200)
accelarating = False
youspeed = 0
pink = 0
red = 0
balldamping = 0.99
playerdamping = 0.96

run = True
while run:
    clock.tick(60)


    keys = pygame.key.get_pressed()

    if you.x <= 15 or you.x >= 825:
        you.xvel = 0

    if you.y <= 15 or you.y >= 385:
        you.yvel = 0

    if you2.x <= 15 or you2.x >= 825:
        you2.xvel = 0

    if you2.y <= 15 or you2.y >= 385:
        you2.yvel = 0


    if b.x <= 110 or b.x >= 730:
        if b.y >= 145 and b.y <= 255:
            pass
        else:
            b.xvel = - b.xvel

    if b.y <= 80 or b.y >= 320:
        b.yvel = - b.yvel

    if keys[pygame.K_LEFT]:
        you.xvel -= 1
        accelarating = True

    if keys[pygame.K_RIGHT]:
        you.xvel += 1
        accelarating = True

    if keys[pygame.K_UP]:
        you.yvel -= 1
        accelarating = True

    if keys[pygame.K_DOWN]:
        you.yvel += 1
        accelarating = True

    if keys[pygame.K_a]:
        you2.xvel -= 1
        accelarating = True

    if keys[pygame.K_d]:
        you2.xvel += 1
        accelarating = True

    if keys[pygame.K_w]:
        you2.yvel -= 1
        accelarating = True

    if keys[pygame.K_s]:
        you2.yvel += 1
        accelarating = True



    youspeed = np.linalg.norm([you.xvel, you.yvel])

    toball = [b.x - you.x, b.y - you.y]
    distance = np.linalg.norm(toball)

    if toball[1] > 0:
        angle = np.arctan(toball[0]/toball[1])
    if toball[1] < 0:
        angle = np.arctan(toball[0]/toball[1]) + np.pi
    else:
        if toball[0] > 0:
            angle = np.pi/2
        else:
            angle = 3*np.pi/2

    youspeed2 = np.linalg.norm([you2.xvel, you2.yvel])

    toball2 = [b.x - you2.x, b.y - you2.y]
    distance2 = np.linalg.norm(toball2)

    if toball2[1] > 0:
        angle2 = np.arctan(toball2[0]/toball2[1])
    if toball2[1] < 0:
        angle2 = np.arctan(toball2[0]/toball2[1]) + np.pi
    else:
        if toball[0] > 0:
            angle2 = np.pi/2
        else:
            angle2 = 3*np.pi/2


    if distance <= 25:
        b.xvel = int(np.floor(toball[0] * youspeed/30))
        b.yvel = int(np.floor(toball[1] * youspeed/30))
        b.x += 1
        b.y += 1
    b.x += b.xvel
    b.y += b.yvel


    if distance2 <= 25:
        b.xvel = int(np.floor(toball2[0] * youspeed2/30))
        b.yvel = int(np.floor(toball2[1] * youspeed2/30))
        b.x += 1
        b.y += 1
    b.x += b.xvel
    b.y += b.yvel

    you.x += you.xvel
    you.y += you.yvel

    you2.x += you2.xvel
    you2.y += you2.yvel

    if you.x >= 825:
        you.x = 825

    if you.y >= 385:
        you.y = 385

    if you.x <= 15:
        you.x = 15

    if you.y <= 15:
        you.y = 15

    if you2.x >= 825:
        you2.x = 825

    if you2.y >= 385:
        you2.y = 385

    if you2.x <= 15:
        you2.x = 15

    if you2.y <= 15:
        you2.y = 15

    if b.x <= 110:
        if b.y >= 255 or b.y <= 145:
            b.x = 110

    if b.y <= 80:
        b.y = 80

    if b.x >= 730:
        if b.y >= 255 or b.y <= 145:
            b.x = 730

    if b.y >= 320:
        b.y = 320

    Q = goal(you, you2, b, red, pink)
    red = Q[0]
    pink = Q[1]
    redrawgamewindow()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
