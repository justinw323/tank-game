#################################################
# TP
#
# Your name: Justin Wang
# Your andrew id: jyw2
#################################################

# The main file
# Contains app information, canvas information, and controls the general
# gamestate

from cmu_112_graphics import *
import random, math, time
from Maze import Maze
from Wall import Wall
from Bullet import Bullet
from Tank import Tank, PlayerTank, AITank
from Line import Line, LineH, LineV, LineD
from Graph import Graph

def appStarted(app):
    app.player = None
    app.playerColor = "red"
    app.bot = None
    app.tanks = []
    app.bullets = []
    app.gameOver = False
    app.prevGameOver = False
    app.gameOverTime = math.inf
    app.mazeObj = None
    app.walls = []
    app.paused = False
    app.splashScreen = True
    app.controlScreen = False
    app.gameScreen = False
    app.chooseColorScreen = False
    app.slider1Pos = 372
    app.slider2Pos = 372
    app.slider3Pos = 372
    # newRound(app)

def newRound(app):
    time.sleep(1)
    newMaze = Maze(7,10, 80)
    newMaze.generateMaze()
    app.mazeObj = newMaze
    app.mazeGraph = app.mazeObj.generateGraph()
    app.walls = []
    generateWalls(app, app.mazeObj.maze)
    pRow = random.randint(0,app.mazeObj.rows-1)
    pCol = random.randint(0,app.mazeObj.cols-1)
    bRow = random.randint(0,app.mazeObj.rows-1)
    bCol = random.randint(0,app.mazeObj.cols-1)
    # print(f"pRow = {pRow}\tpCol = {pCol}")
    # print(f"bRow = {bRow}\tbCol = {bCol}")
    while(bRow == pRow and bCol == pCol):
        bRow = random.randint(0,app.mazeObj.rows-1)
    # print(f"pRow = {pRow}\tpCol = {pCol}")
    # print(f"bRow = {bRow}\tbCol = {bCol}")
    # bRow = pRow
    px, py = app.mazeObj.maze[pRow][pCol].getCenterCoordinates()
    bx, by = app.mazeObj.maze[bRow][bCol].getCenterCoordinates()
    app.gameOver = False
    app.prevGameOver = False
    app.gameOverTime = math.inf
    if(app.player == None):
        app.player = PlayerTank(px, py, "Player", app.playerColor)
    if(app.bot == None):
        app.bot = AITank(bx, by)
    else:
        playerScore = app.player.score
        botScore = app.bot.score
        app.player = PlayerTank(px, py, app.player.name, app.player.color, 
                playerScore)
        app.bot = AITank(bx, by, botScore)
    app.tanks = [app.player, app.bot]
    app.gameOver = False

def generateWalls(app, maze):
    walls = []
    #Generate the outer wall of the maze
    northWallv1 = maze[0][0].getNorthWallCoordinates()[0]
    northWallv4 = maze[0][0].getNorthWallCoordinates()[3]
    northWallv2 = maze[0][len(maze[0])-1].getNorthWallCoordinates()[1]
    northWallv3 = maze[0][len(maze[0])-1].getNorthWallCoordinates()[2]
    walls.append(Wall(northWallv1, northWallv2, northWallv3, northWallv4))
    southWallv1 = maze[len(maze)-1][0].getSouthWallCoordinates()[0]
    southWallv4 = maze[len(maze)-1][0].getSouthWallCoordinates()[3]
    southWallv2 = maze[len(maze)-1][len(maze[0])-1].getSouthWallCoordinates()[1]
    southWallv3 = maze[len(maze)-1][len(maze[0])-1].getSouthWallCoordinates()[2]
    walls.append(Wall(southWallv1, southWallv2, southWallv3, southWallv4))
    westWallv1 = maze[0][0].getWestWallCoordinates()[0]
    westWallv2 = maze[0][0].getWestWallCoordinates()[1]
    westWallv3 = maze[len(maze)-1][0].getWestWallCoordinates()[2]
    westWallv4 = maze[len(maze)-1][0].getWestWallCoordinates()[3]
    walls.append(Wall(westWallv1, westWallv2, westWallv3, westWallv4))
    eastWallv1 = maze[0][len(maze[0])-1].getEastWallCoordinates()[0]
    eastWallv2 = maze[0][len(maze[0])-1].getEastWallCoordinates()[1]
    eastWallv3 = maze[len(maze)-1][len(maze[0])-1].getEastWallCoordinates()[2]
    eastWallv4 = maze[len(maze)-1][len(maze[0])-1].getEastWallCoordinates()[3]
    walls.append(Wall(eastWallv1, eastWallv2, eastWallv3, eastWallv4))
    for r in range(len(maze)-1):
        # print()
        # print(f"row {r}")
        southWalls = []
        c = 0
        while(c < (len(maze[0]))):
            if(maze[r][c].s):
                # print(f"cell[{r}][{c}] has a south wall")
                newWall = [c]
                while((c < (len(maze[0])-1)) and maze[r][c+1].s):
                    c += 1
                    # print(f"cell[{r}][{c}] has a south wall")
                newWall.append(c)
                southWalls.append(newWall)
            c += 1
        # print(f"southWalls row {r} = {southWalls}")
        for wall in southWalls:
            v1 = maze[r][wall[0]].getSouthWallCoordinates()[0]
            v4 = maze[r][wall[0]].getSouthWallCoordinates()[3]
            v2 = maze[r][wall[1]].getSouthWallCoordinates()[1]
            v3 = maze[r][wall[1]].getSouthWallCoordinates()[2]
            walls.append(Wall(v1, v2, v3, v4))
    for c in range(len(maze[0])-1):
        eastWalls = []
        r = 0
        while(r < (len(maze))):
            if(maze[r][c].e):
                # print(f"cell[{r}][{c}] has an east wall")
                newWall = [r]
                while((r < (len(maze)-1)) and maze[r+1][c].e):
                    r += 1
                    # print("bruh")
                newWall.append(r)
                eastWalls.append(newWall)
            r += 1
        # print(f"eastWalls col {c} = {eastWalls}")
        for wall in eastWalls:
            v1 = maze[wall[0]][c].getEastWallCoordinates()[0]
            v2 = maze[wall[0]][c].getEastWallCoordinates()[1]
            v3 = maze[wall[1]][c].getEastWallCoordinates()[2]
            v4 = maze[wall[1]][c].getEastWallCoordinates()[3]
            walls.append(Wall(v1, v2, v3, v4))
    # for wall in walls:
    #     print(f"v1 {v1}\tv2 {v2}\tv3 {v3}\tv4 {v4}")
    app.walls.extend(walls)

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def angle(x1, y1, x2, y2):
    # Returns the angle from point 1 to 2
    if(x2-x1 == 0):
        if(y1 > y2):
            return -math.pi/2
        if(y1 < y2):
            return math.pi/2
    return math.atan2((y2-y1),(x2-x1))

def lineToPointDistance(line, px, py):
    minX = min(line.endpoint1[0], line.endpoint2[0])
    maxX = max(line.endpoint1[0], line.endpoint2[0])
    minY = min(line.endpoint1[1], line.endpoint2[1])
    maxY= max(line.endpoint1[1], line.endpoint2[1])
    if(type(line) == LineH):
        if(minX < px < maxX):
            return abs(py - maxY)
        else:
            return min(distance(line.endpoint1[0], line.endpoint1[1], px, py), 
            distance(line.endpoint2[0], line.endpoint2[1], px, py))
    if(type(line) == LineV):
        if(minY < py < maxY):
            return abs(px - maxX)
        else:
            return min(distance(line.endpoint1[0], line.endpoint1[1], px, py), 
            distance(line.endpoint2[0], line.endpoint2[1], px, py))

def checkPointInTank(point, tank):
    x = point[0]
    y = point[1]
    l1, l2, l3, l4 = tank.calcLines()
    v1, v2, v3, v4 = tank.calcVertices()
    xMax = max(v1[0], v2[0], v3[0], v4[0])
    yMax = max(v1[1], v2[1], v3[1], v4[1])
    xMin = min(v1[0], v2[0], v3[0], v4[0])
    yMin = min(v1[1], v2[1], v3[1], v4[1])
    if (point[1] < yMin or point[1] > yMax):
        return False
    elif (point[0] < xMin or point[0] > xMax):
        return False
    elif(type(l1) == LineH or type(l2) == LineH):
        return True
    else:
        # the point is within the bounds of the vertices, but not necessarily
        # in the actual box (diagonal lines)
        d = distance(x, y, tank.x, tank.y)
        dir = angle(tank.x, tank.y, x, y)
        if(d < 15):
            return True
        if(-math.atan(15/22.5) <= dir <= math.atan(15/22.5)):
            if(d < 22.5/(math.cos(dir))):
                return True
        else:
            if(d < 15/(math.sin(dir))):
                return True
    return False

def checkBulletTankCollision(app):
    for tank in app.tanks:
        for b in range(len(app.bullets)):
            bullet = app.bullets[b]
            if(checkPointInTank((bullet.x, bullet.y), tank)):
                if(bullet.distance > 10 or bullet.shooter != tank):
                    app.bullets.pop(b)
                    tank.alive = False
                    if tank == app.player:
                        app.bot.score += 1
                    else:
                        app.player.score += 1
                    app.gameOver = True
                    break

def checkTankWallCollision(app, tank):
    collision = False
    for wall in app.walls:
        for point in tank.calcVertices():
            if wall.checkPointWallCollision(point):
                collision = True
                # print("point")
                # print(wall.row, wall.col, wall.dir)
                return collision
    for wall in app.walls:
        for line in tank.calcLines():
            if wall.checkLineWallCollision(line):
                # print("line")
                collision = True
                return collision
    # print(collision)
    return collision

def checkTankTankCollision(app, newPos, otherTank):
    # newPos represents the theoretical position of a tank after performing a
    # move, while tank represents the other tank that is not moving
    vertices1 = newPos.calcVertices()
    vertices2 = otherTank.calcVertices()
    for vertex in vertices1:
        if checkPointInTank(vertex, otherTank):
            return True
    for vertex in vertices2:
        if checkPointInTank(vertex, newPos):
            return True
    return False

def checkBulletWallCollision(app, bullet):
    nearestLine = app.walls[0].l1
    nearestLineDistance = (lineToPointDistance(app.walls[0].l1, bullet.x,
    bullet.y))
    for wall in app.walls:
        lines = [wall.l1, wall.l2, wall.l3, wall.l4]
        for line in lines:
            if(lineToPointDistance(line, bullet.x, bullet.y) < 
            nearestLineDistance):
                nearestLineDistance = lineToPointDistance(line, bullet.x, 
                bullet.y)
                nearestLine = line
    if(nearestLineDistance < 3):
        if(type(nearestLine) == LineH):
            bullet.dir = -bullet.dir
        elif(type(nearestLine) == LineV):
            bullet.dir = math.pi-bullet.dir

# Unsticking function is based on that from Tank Trouble described here:
# https://www.subterraneansoftware.com/tanktrouble-single-player-ai/
def unstick(app):
    # print("unsticking")
    app.bot.goToCell(app.mazeObj.whichCell(app.bot.x, app.bot.y))
    if(app.bot.dest[0]-5 < app.bot.x < app.bot.dest[0]+5
    and app.bot.dest[1]-5 < app.bot.y < app.bot.dest[1]+5):
        # print("not stuck anymore")
        app.bot.unstick = False

def mousePressed(app, event):
    if(app.splashScreen):
        if(400 <= event.x <= 600 and 400 <= event.y <= 450):
            app.splashScreen = False
            app.controlScreen = True
            newRound(app)
        if(400 <= event.x <= 600 and 500 <= event.y <= 550):
            app.splashScreen = False
            app.chooseColorScreen = True
    elif(app.controlScreen):
        if(600 <= event.x <= 700 and 500 <= event.y <= 550):
            app.controlScreen = False
            app.gameScreen = True
            newRound(app)
        if(300 <= event.x <= 400 and 500 <= event.y <= 550):
            app.controlScreen = False
            app.splashScreen = True
    elif(app.chooseColorScreen):
        if(250 < event.y < 300):
            if(287.5 < event.x < 337.5):
                app.playerColor = "red"
            if(362.5 < event.x < 412.5):
                app.playerColor = "blue"
            if(437.5 < event.x < 487.5):
                app.playerColor = "green"
            if(512.5 < event.x < 562.5):
                app.playerColor = "yellow"
            if(587.5 < event.x < 637.5):
                app.playerColor = "purple"
            if(662.5 < event.x < 712.5):
                app.playerColor = "orange"
        if(372 < event.x < 628):
            if(330 < event.y < 370):
                app.slider1Pos = event.x
                app.playerColor = calcHexColor(app)
            if(390 < event.y < 430):
                app.slider2Pos = event.x
                app.playerColor = calcHexColor(app)
            if(450 < event.y < 490):
                app.slider3Pos = event.x
                app.playerColor = calcHexColor(app)
        if(450 <= event.x <= 550 and 500 <= event.y <= 550):
            app.splashScreen = True
            app.chooseColorScreen = False

def keyPressed(app, event):
    if(event.key == "q"):
        app.splashScreen = True
        app.controlScreen = False
        app.gameScreen = False
        app.paused = False
        app.player.score = 0
        app.bot.score = 0
    if(event.key == "p"):
        app.paused = not app.paused
    if(event.key == "r"):
        if app.paused:
            app.player.score = 0
            app.bot.score = 0
    if(event.key == "Left" or event.key == "a"):
        if app.gameScreen:
            app.player.actions.add("Left")
    if(event.key == "Right" or event.key == "d"):
        if app.gameScreen:
            app.player.actions.add("Right")
    if(event.key == "Up" or event.key == "w"):
        if app.gameScreen:
            app.player.actions.add("Forward")
    if(event.key == "Down" or event.key == "s"):
        if app.gameScreen:
            app.player.actions.add("Backward")
    if(event.key == "Space"):
        if app.gameScreen:
            app.player.actions.add("Shoot")
    if(event.key == "z" or event.key == ","):
        if app.gameScreen:
            app.player.actions.add("TurretLeft")
    if(event.key == "x" or event.key == "."):
        if app.gameScreen:
            app.player.actions.add("TurretRight")
    if(event.key == "c"):
        newRound(app)
    # if(event.key == "v"):
    #     print(len(app.player.bullets))
    #     print(len(app.bot.bullets))
        # print(f"self.turretDir = {app.bot.turretDir}")
        # print(f"angleToPlayer = {angleToPlayer}")
        # for tank in app.tanks:
        #     print(tank.alive)

def keyReleased(app, event):
    if(event.key == "Left" or event.key == "a"):
        if("Left" in app.player.actions):
            app.player.actions.remove("Left")
    if(event.key == "Right" or event.key == "d"):
        if("Right" in app.player.actions):
            app.player.actions.remove("Right")
    if(event.key == "Up" or event.key == "w"):
        if("Forward" in app.player.actions):
            app.player.actions.remove("Forward")
    if(event.key == "Down" or event.key == "s"):
        if("Backward" in app.player.actions):
            app.player.actions.remove("Backward")
    if(event.key == "Space" or event.key == "m"):
        if("Shoot" in app.player.actions):
            app.player.actions.remove("Shoot")
    if(event.key == "z" or event.key == ","):
        if("TurretLeft" in app.player.actions):
            app.player.actions.remove("TurretLeft")
    if(event.key == "x" or event.key == "."):
        if("TurretRight" in app.player.actions):
            app.player.actions.remove("TurretRight")

def drawSplashScreen(app, canvas):
    tank1 = Tank(250,200)
    tank2 = Tank(750,200)
    tank3 = Tank(250,500)
    tank4 = Tank(750,500)
    tank1.dir = 0.5
    tank2.dir = -0.5-math.pi
    tank3.dir = -0.5
    tank4.dir = 0.5+math.pi
    tank1.color = "red"
    tank2.color = "green"
    tank3.color = "blue"
    tank4.color = "gray"
    canvas.create_text(app.width/2, 300, text = "Tank Battle 112", 
    font = "Helvetica 48 bold")
    for tank in [tank1, tank2, tank3, tank4]:
            v1, v2, v3, v4 = tank.calcVertices()
            canvas.create_polygon(v1, v2, v3, v4, fill = tank.color, 
            outline = "black")
            t1, t2, t3, t4 = tank.calcTurretVertices()
            canvas.create_polygon(t1, t2, t3, t4, fill = tank.color, 
            outline = "black", width = 1.2)
            b1, b2, b3, b4 = tank.calcBarrelVertices()
            canvas.create_polygon(b1, b2, b3, b4, fill = tank.color, 
            outline = "black", width = 1.2)
    canvas.create_rectangle(400, 400, 600, 450)
    canvas.create_text(app.width/2, 425, text = "Play", 
    font = "Helvetica 12 bold")
    canvas.create_rectangle(400, 500, 600, 550)
    canvas.create_text(app.width/2, 525, text = "Choose Colors", 
    font = "Helvetica 12 bold")

def drawControlScreen(app, canvas):
    canvas.create_text(app.width/2, 100, text = "Controls:", 
    font = "Helvetica 30 bold")
    # Do not add tabs. It messes with the spacing on the canvas
    canvas.create_text(app.width/2, 300, text = "Move forward:\tUp or w\n\
Move backward:\tDown or s\nTurn left:\t\tLeft or a\nTurn right:\t\t\
Right or d\nRotate turret left:\tz or ,\nRotate turret right:\tx or .\n\
Shoot gun:\tSpace\nPause:\t\tp\nQuit:\t\tq", font = "Helvetica 14")
    canvas.create_rectangle(600, 500, 700, 550)
    canvas.create_text(650, 525, text = "Play", font = "Helvetica 12 bold")
    canvas.create_rectangle(300, 500, 400, 550)
    canvas.create_text(350, 525, text = "Back", font = "Helvetica 12 bold")

def calcHexColor(app):
    hex1 = hex(app.slider1Pos-372)
    hex2 = hex(app.slider2Pos-372)
    hex3 = hex(app.slider3Pos-372)
    # print(1)
    # print(hex1, hex2, hex3)
    hex1 = str(hex1[2:])
    hex2 = str(hex2[2:])
    hex3 = str(hex3[2:])
    # print(2)
    # print(hex1, hex2, hex3)
    hexColor = "#"
    if(len(hex1) == 1):
        hexColor += "0"
        hexColor += hex1
    else:
        hexColor += hex1
    if(len(hex2) == 1):
        hexColor += "0"
        hexColor += hex2
    else:
        hexColor += hex2
    if(len(hex3) == 1):
        hexColor += "0"
        hexColor += hex3
    else:
        hexColor += hex3
    return hexColor

def drawColorScreen(app, canvas):
    canvas.create_rectangle(287.5,250,337.5,300, fill = "red")
    canvas.create_rectangle(362.5,250,412.5,300, fill = "blue")
    canvas.create_rectangle(437.5,250,487.5,300, fill = "green")
    canvas.create_rectangle(512.5,250,562.5,300, fill = "yellow")
    canvas.create_rectangle(587.5,250,637.5,300, fill = "purple")
    canvas.create_rectangle(662.5,250,712.5,300, fill = "orange")
    canvas.create_rectangle(450, 500, 550, 550)
    canvas.create_text(500, 525, text = "Back", font = "Helvetica 12 bold")
    canvas.create_rectangle(372,345,628,355, fill = "gray")
    canvas.create_rectangle(372,405,628,415, fill = "gray")
    canvas.create_rectangle(372,465,628,475, fill = "gray")
    canvas.create_rectangle(app.slider1Pos-5,330,app.slider1Pos+5,370, 
    fill = "white")
    canvas.create_rectangle(app.slider2Pos-5,390,app.slider2Pos+5,430, 
    fill = "white")
    canvas.create_rectangle(app.slider3Pos-5,450,app.slider3Pos+5,490, 
    fill = "white")
    tank = Tank(500,200)
    tank.dir = 1.5*math.pi
    tank.turretDir = 1.5*math.pi
    v1, v2, v3, v4 = tank.calcVertices()
    canvas.create_polygon(v1, v2, v3, v4, fill = app.playerColor, 
    outline = "black")
    t1, t2, t3, t4 = tank.calcTurretVertices()
    canvas.create_polygon(t1, t2, t3, t4, fill = app.playerColor, 
    outline = "black", width = 1.2)
    b1, b2, b3, b4 = tank.calcBarrelVertices()
    canvas.create_polygon(b1, b2, b3, b4, fill = app.playerColor, 
    outline = "black", width = 1.2)

def drawPauseScreen(app, canvas):
    canvas.create_rectangle(350, 200, 650, 420, fill = "white")
    canvas.create_text(500,250, text = "Paused", 
    justify = CENTER, font = "Helvetica 18 bold")
    canvas.create_text(500,280, text = "Press p to unpause", 
    justify = CENTER, font = "Helvetica 18 bold")
    canvas.create_text(500,310, text = "Press r to reset scores", 
    justify = CENTER, font = "Helvetica 18 bold")
    canvas.create_text(500,340, text = "Press q to quit to menu", 
    justify = CENTER, font = "Helvetica 18 bold")

def drawTanks(app, canvas):
    for tank in app.tanks:
        if tank.alive:
            v1, v2, v3, v4 = tank.calcVertices()
            canvas.create_polygon(v1, v2, v3, v4, fill = tank.color, 
            outline = "black")
            t1, t2, t3, t4 = tank.calcTurretVertices()
            canvas.create_polygon(t1, t2, t3, t4, fill = tank.color, 
            outline = "black", width = 1.2)
            b1, b2, b3, b4 = tank.calcBarrelVertices()
            canvas.create_polygon(b1, b2, b3, b4, fill = tank.color, 
            outline = "black", width = 1.2)

def drawBullets(app, canvas):
    for bullet in app.bullets:
        canvas.create_oval(bullet.x-bullet.r, bullet.y-bullet.r, 
            bullet.x+bullet.r, bullet.y+bullet.r, fill = "black")

def drawScores(app, canvas):
    canvas.create_text(app.width/4, app.height-20, text = f"{app.player.name}: \
    {app.player.score}", font = "Helvetica 18 bold")
    canvas.create_text(app.width*3/4, app.height-20, text = f"{app.bot.name} \
    {app.bot.score}", font = "Helvetica 18 bold")

def drawMaze(app, canvas):
    for wall in app.walls:
        if((wall.v2[0] - wall.v1[0]) > (wall.v4[1] - wall.v1[1])):
            canvas.create_line(wall.v1[0], wall.v1[1]+2, wall.v2[0], 
            wall.v2[1]+2, fill = "black", width = 4)
        else:
            canvas.create_line(wall.v1[0]+2, wall.v1[1], wall.v4[0]+2,  
            wall.v4[1], fill = "black", width = 4)

def executePlayerActions(app):
    if(app.player.alive):
        for action in app.player.actions:
            if(action == "Left"):
                newPos = app.player.calcProposedRotation("Left")
                if(not checkTankWallCollision(app, newPos) and not
                checkTankTankCollision(app, newPos, app.bot)):
                    app.player.rotateTank("Left")
            elif(action == "Right"):
                newPos = app.player.calcProposedRotation("Right")
                if(not checkTankWallCollision(app, newPos) and
                not checkTankTankCollision(app, newPos, app.bot)):
                    app.player.rotateTank("Right")
            elif(action == "Forward"):
                newPos = app.player.calcProposedMove("Forward")
                if(not checkTankWallCollision(app, newPos) and not
                checkTankTankCollision(app, newPos, app.bot)):
                    app.player.moveTank("Forward")
            elif(action == "Backward"):
                newPos = app.player.calcProposedMove("Backward")
                if(not checkTankWallCollision(app, newPos) and not
                checkTankTankCollision(app, newPos, app.bot)):
                    app.player.moveTank("Backward")
            elif(action == "Shoot"):
                app.player.shoot()
            elif(action == "TurretLeft"):
                app.player.rotateTurret("Left")
            elif(action == "TurretRight"):
                app.player.rotateTurret("Right")

def executeBotActions(app):
    moved = False
    if("Left" in app.bot.actions):
        newPos = app.bot.calcProposedRotation("Left")
        if(not checkTankWallCollision(app, newPos) and not
        checkTankTankCollision(app, newPos, app.player)):
            # print("rotating left")
            app.bot.rotateTank("Left")
            moved = True
    if("Right" in app.bot.actions):
        newPos = app.bot.calcProposedRotation("Right")
        if(not checkTankWallCollision(app, newPos) and not
        checkTankTankCollision(app, newPos, app.player)):
            # print("rotating right")
            app.bot.rotateTank("Right")
            moved = True
    if("Forward" in app.bot.actions):
        newPos = app.bot.calcProposedMove("Forward")
        if(not checkTankWallCollision(app, newPos) and not
        checkTankTankCollision(app, newPos, app.player)):
            # print("moving forward")
            app.bot.moveTank("Forward")
            moved = True
    if("Backward" in app.bot.actions):
        newPos = app.bot.calcProposedMove("Backward")
        if(not checkTankWallCollision(app, newPos) and not
        checkTankTankCollision(app, newPos, app.player)):
            # print("moving backward")
            app.bot.moveTank("Backward")
            moved = True
    if("Shoot" in app.bot.actions):
        app.bot.shoot()
        app.bot.actions.remove("Shoot")
    if("TurretLeft" in app.bot.actions):
        app.bot.rotateTurret("Left")
    if("TurretRight" in app.bot.actions):
        app.bot.rotateTurret("Right")
    if(not moved and len(app.bot.actions) > 0):
        app.bot.unstick = True

def getOppositeAction(action):
    if action == "Left":
        return "Right"
    if action == "Right":
        return "Left"
    if action == "Forward":
        return "Backward"
    if action == "Backward":
        return "Forward"

def calcShots(app):
    hitAngles = []
    for x in range(-10, 11):
        rads = x/2.0*math.pi/180
        fireDir = app.bot.turretDir + rads
        calcBullet = Bullet(app.bot.x, app.bot.y, app.bot.turretDir + rads, 
        app.bot)
        while(calcBullet.distance <= 60):
            # print(f"calcBullet pos: ({calcBullet.x}, {calcBullet.y})")
            # print(f"calcBullet distance: {calcBullet.distance}")
            if(checkPointInTank((calcBullet.x, calcBullet.y), app.bot) and 
            calcBullet.distance > 30):
                # print(f"hits self after {calcBullet.distance}")
                break
            elif(checkPointInTank((calcBullet.x, calcBullet.y), app.player)):
                # print(f"coords: {calcBullet.x")
                # print(f"distance = {distance(calcBullet.x, calcBullet.y, 
                # app.player.x, app.player.y)}")
                hitAngles.append(fireDir)
                break
            checkBulletWallCollision(app, calcBullet)
            calcBullet.x += 20*math.cos(calcBullet.dir)
            calcBullet.y += 20*math.sin(calcBullet.dir)
            calcBullet.distance += 20
            # print(calcBullet.distance)
        # print(f"angle {x} not hit")
    return hitAngles

def timerFired(app):
    if app.gameScreen and not app.paused:
        app.bullets = app.player.bullets + app.bot.bullets
        if(app.gameOver):
            if(not app.prevGameOver):
                app.gameOverTime = time.time()
                app.prevGameOver = True
            elif(time.time() - app.gameOverTime > 3):
                newRound(app)
        checkBulletTankCollision(app)
        executePlayerActions(app)
        executeBotActions(app)
        shots = calcShots(app)
        # print(f"{len(shots)} shots")
        if(len(shots) > 0):
            app.bot.aim(shots[random.randint(0,len(shots)-1)])
        else:
            lineToTarget = app.bot.getLineToTarget(app.player.x, app.player.y)
            lineOfSightBlocked = False
            for wall in app.walls:
                if wall.checkLineWallCollision(lineToTarget):
                    lineOfSightBlocked = True
            if(app.player.alive and not lineOfSightBlocked):
                # print("shoot1")
                app.bot.aimAtPlayer(app.player.x, app.player.y)
        i = 0
        while i < len(app.player.bullets):
            if(not app.player.bullets[i].reachedMaxDistance()):
                checkBulletWallCollision(app, app.player.bullets[i])
                app.player.bullets[i].moveBullet()
                i += 1
            else:
                app.player.bullets.pop(i)
        j = 0
        while j < len(app.bot.bullets):
            if(not app.bot.bullets[j].reachedMaxDistance()):
                checkBulletWallCollision(app, app.bot.bullets[j])
                app.bot.bullets[j].moveBullet()
                j += 1
            else:
                app.bot.bullets.pop(j)
        n = 0
        while n < len(app.tanks):
            if not app.tanks[n].alive:
                app.tanks.pop(n)
            else:
                n += 1
        aiCell = app.mazeObj.whichCell(app.bot.x, app.bot.y)
        playerCell = app.mazeObj.whichCell(app.player.x, app.player.y)
        # playerCell = app.mazeObj.whichCell(40, 40)
        if(aiCell != playerCell):
            prevNodes = app.bot.findPath(app.mazeGraph, aiCell, playerCell)
            # print(f"timerFired prevNodes = {prevNodes}")
            aiPos = (aiCell.row, aiCell.col)
            playerPos = (playerCell.row, playerCell.col)
            path = app.mazeGraph.tracePath(aiPos, playerPos, prevNodes)
            # print(f"path = {path}")
            coordPath = []
            for cellPos in path:
                cell = app.mazeObj.getCell(cellPos[0], cellPos[1])
                coordPath.append(cell.getCenterCoordinates())
            # print(f"coordPath = {coordPath}")
            # app.bot.followPath(app.mazeObj, path)
            if(app.bot.path[-1] != coordPath[-1]):
                app.bot.path = coordPath
            if not app.bot.unstick:
                app.bot.followPath()
            else:
                unstick(app)

def redrawAll(app, canvas):
    if app.splashScreen:
        drawSplashScreen(app, canvas)
    if app.chooseColorScreen:
        drawColorScreen(app, canvas)
    if app.controlScreen:
        drawControlScreen(app, canvas)
    if app.gameScreen:
        drawMaze(app, canvas)
        drawScores(app, canvas)
        drawBullets(app, canvas)
        drawTanks(app, canvas)
        if app.paused:
            drawPauseScreen(app, canvas)

def playGame():
    runApp(width=1000, height=700)

playGame()