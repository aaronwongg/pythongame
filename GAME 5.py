import pygame
import numpy as np

windowwidth = 840
windowheight = 400
pitchwidth = 640
pitchheight = 260
goalsize = 110

pygame.init()
win = pygame.display.set_mode((windowwidth, windowheight))
pygame.display.set_caption("ball")

clock = pygame.time.Clock()


font = pygame.font.Font(None, 50)

# defines player numbers
# the first players are controlled manually
# this was added because it will end up being added anyways
# it also allows us to test the robustness of player-player collisions when there are large numbers of players
redteamsize = 5
pinkteamsize = 5

# game parameters for the player
playerradius = 15
playerbouncing = 0.5
playerinvmass = 0.5
playerdamping = 0.96
accel = 0.1
kickaccel = 0.07
kickstrength = 5

# game parameters for the ball
ballradius = 10
balldamping = 0.99
ballinvmass = 1
ballbouncing = 0.5

# parameters for the pitch drawing
redstart = (200, 200)
pinkstart = (640, 200)
ballstart = (420, 200)
goalpostradius = 8
goalpostbouncingquotient = 0.5
goallinethickness = 3
kickingcircleradius = 15
kickingcirclethickness = 2

# defines colors used in drawing the map
redcolour = (255, 0, 0)
pinkcolour = (255, 0, 255)
ballcolour = (0, 0, 0)
goallinecolour = (199, 230, 189)
goalpostcolour = (150, 150, 150)
pitchcolour = (127, 162, 112)
bordercolour = (113, 140, 90)
kickingcirclecolour = (255, 255, 255)

# defines centre line properties
centrecircleradius = 70
centrecirclecolour = (199, 230, 189)
centrecirclethickness = 3
centrelinethickness = 3

# defines text properties
textcolour = (0, 0, 0)
textposition = (215, 25)

# defines relevant pitch coordinates for calculation
pitchcornerx = int(np.floor((windowwidth - pitchwidth)/2))
pitchcornery = int(np.floor((windowheight - pitchheight)/2))

goalcornery = int(np.floor((windowheight - goalsize)/2))
y1 = pitchcornerx - 30

z1 = pitchcornerx + pitchwidth
z2 = goalcornery

a1 = y1 + 2*ballradius
a2 = int(np.floor(goalcornery-goallinethickness/2))

b1 = z1
b2 = int(np.floor(goalcornery-goallinethickness/2))

# defines the movespace of a player
movespacex = [playerradius, windowwidth - playerradius]
movespacey = [playerradius, windowheight - playerradius]

# defines the movespace of a ball
ballspacex = [pitchcornerx + ballradius, pitchcornerx + pitchwidth - ballradius]
ballspacey = [pitchcornery + ballradius, pitchcornery + pitchheight - ballradius]

# defines goal width
goaly = [goalcornery, goalcornery + goalsize]

# handles player indexing
curr_idx = -1


def get_idx():
    global curr_idx
    curr_idx += 1
    return curr_idx

class player(object):

    def __init__(self, x, y, colour):

        # sets default positions
        self.defaultx = x
        self.defaulty = y
        self.idx = get_idx()

        # position vectors
        self.pos = np.array([x,y]).astype(float)

        # velocity and speed
        self.velocity = np.array([0, 0])
        self.speed = 0

        # acceleration
        self.acc = np.array([0, 0])
        self.acceleration = accel

        # player properties
        self.colour = colour
        self.kicking = False
        self.bouncingquotient = playerbouncing
        self.radius = playerradius

    def draw(self, win):

        pygame.draw.circle(win, self.colour, tuple(self.pos.astype(int)), playerradius)
        if self.kicking == True:
            pygame.draw.ellipse(win, kickingcirclecolour, (
            self.pos[0] - kickingcircleradius, self.pos[1] - kickingcircleradius, 2 * kickingcircleradius,
            2 * kickingcircleradius), kickingcirclethickness)
        else:
            pygame.draw.ellipse(win, (0, 0, 0), (
            self.pos[0] - kickingcircleradius, self.pos[1] - kickingcircleradius, 2 * kickingcircleradius,
            2 * kickingcircleradius), kickingcirclethickness)

    def reset(self):

        # position vectors
        self.pos = np.array([self.defaultx,self.defaulty]).astype(float)

        # velocity and speed
        self.velocity = np.array([0, 0])
        self.speed = 0

        # acceleration
        self.acc = np.array([0, 0])
        self.acceleration = accel

        # player properties
        self.kicking = False

    def dist(self, obj):
        return np.linalg.norm(obj.pos - self.pos)

    def kickdirection(self, ball):
        return (ball.pos - self.pos) / self.dist(ball)


class ball(object):

    def __init__(self, x, y):
        # sets default positions
        self.defaultx = x
        self.defaulty = y

        # position vectors
        self.pos = np.array([x,y]).astype(float)

        # velocity and speed
        self.velocity = np.array([0.0, 0.0])
        self.speed = 0

        # acceleration
        self.acc = np.array([0.0, 0.0])
        self.acceleration = accel

        # ball properties
        self.bouncingquotient = ballbouncing
        self.radius = ballradius

    def draw(self, win):

        pygame.draw.circle(win, (255, 255, 255), tuple(self.pos.astype(int)), ballradius)
        pygame.draw.ellipse(win, (0, 0, 0,),
                            (self.pos[0] - ballradius, self.pos[1] - ballradius, 2 * ballradius, 2 * ballradius), 2)

    def reset(self):
        # position vectors
        self.pos = np.array([self.defaultx, self.defaulty]).astype(float)

        # velocity and speed
        self.velocity = np.array([0, 0])
        self.speed = 0

        # acceleration
        self.acc = np.array([0, 0])
        self.acceleration = accel


class goalpost(object):

    def __init__(self, x, y):
        self.pos = np.array([x, y])
        self.bouncingquotient = goalpostbouncingquotient
        self.velocity = np.array([0.0,0.0])
        self.radius = goalpostradius

    def draw(self, win):
        pygame.draw.circle(win, goalpostcolour, tuple(self.pos.astype(int)), goalpostradius)


def redrawgamewindow():
    win.fill((0, 0, 0))

    # draws border
    pygame.draw.rect(win, bordercolour, (0, 0, windowwidth, windowheight))

    # draws pitch
    pygame.draw.rect(win, pitchcolour, (pitchcornerx, pitchcornery, pitchwidth, pitchheight))
    pygame.draw.rect(win, pitchcolour, (pitchcornerx - 30, goalcornery, 30, goalsize))
    pygame.draw.rect(win, pitchcolour, (windowwidth - pitchcornerx, goalcornery, 30, goalsize))

    #draws goal lines
    pygame.draw.rect(win, goallinecolour, (pitchcornerx - goallinethickness // 2, pitchcornery - goallinethickness // 2, goallinethickness, pitchheight + goallinethickness))
    pygame.draw.rect(win, goallinecolour, (windowwidth- pitchcornerx - goallinethickness // 2, pitchcornery - goallinethickness // 2, goallinethickness, pitchheight + goallinethickness))
    pygame.draw.rect(win, goallinecolour, (pitchcornerx - goallinethickness // 2, pitchcornery - goallinethickness // 2, pitchwidth + goallinethickness, goallinethickness))
    pygame.draw.rect(win, goallinecolour, (pitchcornerx - goallinethickness // 2, windowheight - pitchcornery - goallinethickness // 2, pitchwidth + goallinethickness, goallinethickness))

    # draws center circle
    pygame.draw.ellipse(win, centrecirclecolour, (ballstart[0] - centrecircleradius, ballstart[1] - centrecircleradius, 2*centrecircleradius, 2*centrecircleradius), centrecirclethickness)
    pygame.draw.rect(win, centrecirclecolour, (windowwidth // 2 - centrelinethickness // 2, pitchcornery, centrelinethickness, pitchheight))

    # draws environment objects
    for obj in movingobjects:
        obj.draw(win)

    for goal in goalposts:
        goal.draw(win)

    b.draw(win)

    string = str(redscore) + ":" + str(pinkscore)
    text = font.render(string, True, (255, 255, 255))
    win.blit(text, (215, 25))
    pygame.display.update()


# defines object-object collision
def collision(obj1, obj2):
    direction = (obj1.pos - obj2.pos)
    bouncingq = obj1.bouncingquotient * obj2.bouncingquotient

    # calculates normal and tangent vectors
    collisionnormal = direction / (np.linalg.norm(direction))
    collisiontangent = np.array([direction[1], - direction[0]]) / (np.linalg.norm(direction))

    # updates object components
    obj1component = np.dot(np.array(obj1.velocity), collisionnormal)
    obj2component = np.dot(np.array(obj2.velocity), collisionnormal)

    velocityafter = (obj1component + obj2component)*bouncingq*2
    obj1tangentvelocity = np.dot(np.array(obj1.velocity), collisiontangent)
    obj2tangentvelocity = np.dot(np.array(obj2.velocity), collisiontangent)

    obj1.velocity = velocityafter * np.array(collisionnormal) + obj1tangentvelocity * np.array(collisiontangent)
    obj2.velocity = velocityafter * np.array(collisionnormal) + obj2tangentvelocity * np.array(collisiontangent)

    obj2.pos = obj1.pos - collisionnormal*(obj1.radius + obj2.radius + 1)


# defines object-goalpost collision
def collisiongoalpost(obj1, obj2):
    direction = (obj1.pos - obj2.pos)
    bouncingq = obj1.bouncingquotient * obj2.bouncingquotient

    # calculates normal and tangent vectors
    collisionnormal = direction / (np.linalg.norm(direction))
    collisiontangent = np.array([direction[1], - direction[0]]) / (np.linalg.norm(direction))

    # updates components
    obj1component = np.dot(np.array(obj1.velocity), collisionnormal)
    obj2component = np.dot(np.array(obj2.velocity), collisionnormal)
    velocityafter = (obj1component + obj2component)*bouncingq*2

    obj1tangentvelocity = np.dot(np.array(obj1.velocity), collisiontangent)
    obj2tangentvelocity = np.dot(np.array(obj2.velocity), collisiontangent)

    obj1.velocity = - velocityafter * np.array(collisionnormal) + obj1tangentvelocity * np.array(collisiontangent)
    obj2.velocity = velocityafter * np.array(collisionnormal) + obj2tangentvelocity * np.array(collisiontangent)

    obj2.pos = obj1.pos - collisionnormal*(obj1.radius + obj2.radius + 1)

# handles kick interaction
def kick(obj1, ball):
    ball.velocity = np.array(ball.velocity) + kickstrength * ballinvmass * obj1.kickdirection(ball)

# handles goal event
def goal(ball, redscore, pinkscore):
    if ball.pos[0] <= a1:
        pinkscore += 1
        resetgame()
    elif ball.pos[0] >= b1 + 5:
        redscore += 1
        resetgame()

    return [redscore, pinkscore]

# resets the game
def resetgame():
    for obj in movingobjects:
        obj.reset()


# handles players and movespace
def keep_player_in_movespace(player):

    # should keep things on board
    if player.pos[0] <= movespacex[0] or player.pos[0] >= movespacex[1]:
        player.velocity[0] = 0
        if player.pos[0] <= movespacex[0]:
            player.pos[0] = movespacex[0]
        if player.pos[0] >= movespacex[1]:
            player.pos[0] = movespacex[1]
    if player.pos[1] <= movespacey[0] or player.pos[1] >= movespacey[1]:
        player.velocity[1] = 0
        if player.pos[1] <= movespacey[0]:
            player.pos[1] = movespacey[0]
        if player.pos[1] >= movespacey[1]:
            player.pos[1] = movespacey[1]


# handles balls and movespace
def keep_ball_in_movespace(ball):
    if ball.pos[0] <= ballspacex[0] or ball.pos[0] >= ballspacex[1]:
        if ball.pos[1] >= goaly[0] and ball.pos[1] <= goaly[1]:
            pass
        else:
            ball.velocity[0] = - 0.5 * ball.velocity[0]
            if ball.pos[0] <= ballspacex[0]:
                ball.pos[0] = ballspacex[0]

            if ball.pos[0] >= ballspacex[1]:
                ball.pos[0] = ballspacex[1]
    if ball.pos[1] <= ballspacey[0] or b.pos[1] >= ballspacey[1]:
        ball.velocity[1] = - 0.5 * b.velocity[1]
        if ball.pos[1] <= ballspacey[0]:
            ball.pos[1] = ballspacey[0]
        if ball.pos[1] >= ballspacey[1]:
            ball.pos[1] = ballspacey[1]


# initialises players
reds = []
pinks = []

# for now, now players are distributed evenly along the starting point as a proof of concept
for i in range(redteamsize):
    reds.append(player(redstart[0]+50*np.random.uniform(-1,1), redstart[1]+50*np.random.uniform(-1,1), redcolour))

for i in range(pinkteamsize):
    pinks.append(player(pinkstart[0]+50*np.random.uniform(-1, 1), pinkstart[1]+50*np.random.uniform(-1, 1), pinkcolour))

b = ball(ballstart[0], ballstart[1])

# initialises goalposts
redgoalpost1 = goalpost(pitchcornerx, goalcornery)
redgoalpost2 = goalpost(pitchcornerx, goalcornery + goalsize)
pinkgoalpost1 = goalpost(windowwidth - pitchcornerx, goalcornery)
pinkgoalpost2 = goalpost(windowwidth - pitchcornerx, goalcornery + goalsize)

# collects objects into useful groups
players = reds + pinks
movingobjects = players + [b]
goalposts = [redgoalpost1, redgoalpost2, pinkgoalpost1, pinkgoalpost2]

# initialises scores
pinkscore = 0
redscore = 0

run = True
while run:
    clock.tick(60)

    # should keep things on board
    for player in players:
        keep_player_in_movespace(player)

    keep_ball_in_movespace(b)

    # handles the key events
    keys = pygame.key.get_pressed()

    # red movement controls
    if keys[pygame.K_LEFT]:
        if keys[pygame.K_UP]:
            reds[0].acc = np.array([-1.0,-1.0])/(2)**(1/2)
        elif keys[pygame.K_DOWN]:
            reds[0].acc = np.array([-1.0,1.0])/(2)**(1/2)
        else:
            reds[0].acc = np.array([-1.0, 0.0])

    elif keys[pygame.K_RIGHT]:
        if keys[pygame.K_UP]:
            reds[0].acc = np.array([1.0,-1.0])/(2)**(1/2)
        elif keys[pygame.K_DOWN]:
            reds[0].acc = np.array([1.0,1.0])/(2)**(1/2)
        else:
            reds[0].acc = np.array([1.0,0.0])

    elif keys[pygame.K_UP]:
        reds[0].acc = np.array([0.0,-1.0])

    elif keys[pygame.K_DOWN]:
        reds[0].acc = np.array([0.0,1.0])

    else:
        reds[0].acc = np.array([0.0,0.0])

    if keys[pygame.K_SPACE]:
        reds[0].kicking = True
    else:
        reds[0].kicking = False

    # pink movement controls
    if keys[pygame.K_a]:
        if keys[pygame.K_w]:
            pinks[0].acc = np.array([- 1.0,- 1.0])/(2)**(1/2)
        elif keys[pygame.K_s]:
            pinks[0].acc = np.array([- 1.0,1.0])/(2)**(1/2)
        else:
            pinks[0].acc = np.array([- 1.0, 0.0])

    elif keys[pygame.K_d]:
        if keys[pygame.K_w]:
            pinks[0].acc = np.array([1.0,- 1.0])/(2)**(1/2)
        elif keys[pygame.K_s]:
            pinks[0].acc = np.array([1.0,1.0])/(2)**(1/2)
        else:
            pinks[0].acc = np.array([1.0, 0.0])

    elif keys[pygame.K_w]:
        pinks[0].acc = np.array([0.0, -1.0])

    elif keys[pygame.K_s]:
        pinks[0].acc = np.array([0.0, 1.0])

    else:
        pinks[0].acc = np.array([0.0,0.0])

    if keys[pygame.K_g]:
        pinks[0].kicking = True
    else:
        pinks[0].kicking = False

    # moves the players
    for player in players:
        if player.kicking == False:
            player.velocity = np.array(player.velocity) + player.acc*player.acceleration
        else:
            player.velocity = np.array(player.velocity) + player.acc*kickaccel

        player.velocity = player.velocity * playerdamping
        player.pos += player.velocity

    # moves the ball
    b.velocity = np.array(b.velocity) * balldamping
    b.pos += b.velocity

    # handles kicks
    for player in players:
        if player.dist(b) <= playerradius + ballradius + 4:

            if player.kicking == False:
                if player.dist(b) <= playerradius + ballradius:
                    collision(b, player)
            else:
                kick(player, b)

    # checks for movingobject-goal collisions
    for thing in movingobjects:
        for goalpost in goalposts:
            vector =  goalpost.pos - thing.pos
            distance = np.linalg.norm(vector)
            if distance <= goalpostradius + thing.radius:
                thing.pos = goalpost.pos - vector/np.linalg.norm(vector)
                collisiongoalpost(goalpost, thing)

    # checks for player-player collision
    for i in range(len(players)):
        for j in range(i+1, len(players)):
            distance = players[i].dist(players[j])
            if players[i].idx != players[j].idx and distance <= 2*playerradius:
                collision(players[i], players[j])

    # updates score
    G = goal(b, redscore, pinkscore)
    redscore = G[0]
    pinkscore = G[1]
    redrawgamewindow()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
