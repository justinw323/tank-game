#################################################
# TP
#
# Your name: Justin Wang
# Your andrew id: jyw2
#################################################

# Tank objects, with parameters and functions to control the player tank
# and move the AI Tank

from Line import Line, LineH, LineV, LineD
from Bullet import Bullet
import math, time, copy, random

class Tank(object):
    def __init__(self, x, y, score = 0):
        self.name = ""
        self.x = x
        self.y = y
        self.dir = random.random()*2*math.pi
        # self.dir = 0
        self.turretDir = self.dir
        self.color = ""
        self.alive = True
        self.bullets = []
        self.score = score
        self.maxBullets = 8
        self.actions = set()
        self.lastBulletTime = time.time()
    def shoot(self):
        if(self.alive and len(self.bullets) < self.maxBullets and 
        time.time()-self.lastBulletTime > 0.15):
            self.bullets.append(Bullet(self.x + 20*math.cos(self.turretDir), 
                self.y + 20*math.sin(self.turretDir), self.turretDir, self))
            self.lastBulletTime = time.time()
    def fakeShoot(self):
        self.bullets.append(Bullet(self.x + 20*math.cos(self.turretDir), 
            self.y + 20*math.sin(self.turretDir), self.turretDir, self))
    def calcVertices(self):
        # Tanks are 45 by 30
        l = 22.5
        w = 15
        # r = distance from center of tank to vertices
        r = (l**2 + w**2)**0.5
        v1 = (self.x + r*math.cos(self.dir + math.atan(w/l)), 
            self.y + r*math.sin(self.dir + math.atan(w/l)))
        v2 = (self.x + r*math.cos(self.dir - math.atan(w/l)), 
            self.y + r*math.sin(self.dir - math.atan(w/l)))
        v3 = (self.x + r*math.cos(self.dir + math.pi + math.atan(w/l)), 
            self.y + r*math.sin(self.dir + math.pi + math.atan(w/l)))
        v4 = (self.x + r*math.cos(self.dir + math.pi - math.atan(w/l)), 
            self.y + r*math.sin(self.dir + math.pi - math.atan(w/l)))
        return (v1, v2, v3, v4)
    def calcTurretVertices(self):
        # Turret bases are 23 by 18
        l = 11.5
        w = 9
        # r = distance from center of turrent base to vertices
        r = (l**2 + w**2)**0.5
        v1 = (self.x + r*math.cos(self.turretDir + math.atan(w/l)), 
            self.y + r*math.sin(self.turretDir + math.atan(w/l)))
        v2 = (self.x + r*math.cos(self.turretDir - math.atan(w/l)), 
            self.y + r*math.sin(self.turretDir - math.atan(w/l)))
        v3 = (self.x + r*math.cos(self.turretDir + math.pi + math.atan(w/l)), 
            self.y + r*math.sin(self.turretDir + math.pi + math.atan(w/l)))
        v4 = (self.x + r*math.cos(self.turretDir + math.pi - math.atan(w/l)), 
            self.y + r*math.sin(self.turretDir + math.pi - math.atan(w/l)))
        return (v1, v2, v3, v4)
    def calcBarrelVertices(self):
        # Barrels are 13 by 4
        l = 7.5
        w = 3
        # r = distance from center of barrel to vertices
        r = (l**2 + w**2)**0.5
        v1 = (self.x + r*math.cos(self.turretDir + math.atan(w/l)) + 
            19*math.cos(self.turretDir), self.y + r*math.sin(self.turretDir + 
            math.atan(w/l)) + 19*math.sin(self.turretDir))
        v2 = (self.x + r*math.cos(self.turretDir - math.atan(w/l)) + 
            19*math.cos(self.turretDir), self.y + r*math.sin(self.turretDir - 
            math.atan(w/l)) + 19*math.sin(self.turretDir))
        v3 = (self.x + r*math.cos(self.turretDir + math.pi + math.atan(w/l)) + 
            19*math.cos(self.turretDir), self.y + r*math.sin(self.turretDir + 
            math.pi + math.atan(w/l)) + 19*math.sin(self.turretDir))
        v4 = (self.x + r*math.cos(self.turretDir + math.pi - math.atan(w/l)) + 
            19*math.cos(self.turretDir), self.y + r*math.sin(self.turretDir + 
            math.pi - math.atan(w/l)) + 19*math.sin(self.turretDir))
        return (v1, v2, v3, v4)
    def calcLines(self):
        v1, v2, v3, v4 = self.calcVertices()
        if(self.dir == 0 or self.dir == math.pi):
            l1 = LineH(v1, v2)
            l2 = LineV(v2, v3)
            l3 = LineH(v3, v4)
            l4 = LineV(v4, v1)
        elif(self.dir == math.pi/2 or self.dir == 3*math.pi/2):
            l1 = LineV(v1, v2)
            l2 = LineH(v2, v3)
            l3 = LineV(v3, v4)
            l4 = LineH(v4, v1)
        else:
            l1 = LineD(v1, v2)
            l2 = LineD(v2, v3)
            l3 = LineD(v3, v4)
            l4 = LineD(v4, v1)
        return l1, l2, l3, l4
    def rotateTank(self, dir):
        if(dir == "Left"):
            self.dir -= math.pi/45
            self.turretDir -= math.pi/45
        if(dir == "Right"):
            self.dir += math.pi/45
            self.turretDir += math.pi/45
    def moveTank(self, dir):
        if(dir == "Forward"):
            self.x += 2.5*math.cos(self.dir)
            self.y += 2.5*math.sin(self.dir)
        if(dir == "Backward"):
            self.x -= 2.5*math.cos(self.dir)
            self.y -= 2.5*math.sin(self.dir)
    def rotateTurret(self, dir):
        if(dir == "Left"):
            self.turretDir -= math.pi/30
        if(dir == "Right"):
            self.turretDir += math.pi/30
    def calcProposedMove(self, dir):
        # Returns a tank object that has carried out the proposed move
        fakeTank = copy.deepcopy(self)
        fakeTank.moveTank(dir)
        return fakeTank
    def calcProposedRotation(self, dir):
        # Returns a tank object that has carried out the proposed rotation
        fakeTank = copy.deepcopy(self)
        fakeTank.rotateTank(dir)
        return fakeTank

class PlayerTank(Tank):
    def __init__(self, x, y, name, color, score = 0):
        super().__init__(x, y, score)
        self.name = name
        self.color = color

class AITank(Tank):
    def __init__(self, x, y, score = 0):
        super().__init__(x, y, score)
        self.name = "X Æ A-12"
        self.color = "gray"
        self.path = [(self.x, self.y)]
        self.dest = (self.x, self.y)
        self.unstick = False
    def findPath(self, graph, startCell, endCell):
        startNode = (startCell.row, startCell.col)
        endNode = (endCell.row, endCell.col)
        prevNodes = graph.getPath(startNode, endNode)
        # print(f"findPath prevNodes = {prevNodes}")
        return prevNodes
    def followPath(self):
        self.dest = self.path[1]
        # print(f"selfCoords = ({self.x}, {self.y})")
        # print(f"self.dest = {self.dest}")
        self.goToDest()
    def goToDest(self):
        # print(f"({self.x}, {self.y})")
        # print(self.dest)
        angleToDest = angle(self.x , self.y, self.dest[0], self.dest[1])
        while (self.dir-angleToDest >= 2*math.pi):
            self.dir -= 2*math.pi
        while (self.dir-angleToDest < 0):
            self.dir += 2*math.pi
        # print(f"self.dir = {self.dir}\tangleToDest = {angleToDest}")
        if(abs(self.dir-angleToDest) < 0.1 or abs(self.dir-angleToDest) > 2*math.pi-0.1):
            # print("move forward")
            # print(f"{abs(self.dir-angleToDest)} < 0.2")
            self.actions.add("Forward")
        if(abs(self.dir-angleToDest) > math.pi/120):
            if(self.dir > angleToDest and 
            (self.dir-angleToDest < math.pi)):
                # print("rotate turret left")
                self.actions.add("Left")
                if("Right" in self.actions):
                    self.actions.remove("Right")
            # if(self.turretDir < angleToPlayer):
            else:
                # print("rotate turret right")
                self.actions.add("Right")
                if("Left" in self.actions):
                    self.actions.remove("Left")
        # print(self.dest)
        # print(self.path)
        if(self.dest[0]-25 < self.x < self.dest[0]+25 and 
        self.dest[1]-25 < self.y < self.dest[1]+25):
            self.path.pop(0)
    def goToCell(self, cell):
        (cellX, cellY) = cell.getCenterCoordinates()
        print(f"going to {(cellX, cellY)}")
        angleToDest = angle(self.x , self.y, cellX, cellY)
        # while(self.dir-angleToDest >= 2*math.pi):
        #     self.dir -= 2*math.pi
        # while(self.dir-angleToDest < 0):
        #     self.dir += 2*math.pi
        self.dir = self.dir%(2*math.pi)
        angleToDest = angleToDest%(2*math.pi)
        # print(f"self.dir = {self.dir}")
        if(abs(self.dir-angleToDest) < 0.3):
            # print("move forward")
            # print(f"{abs(self.dir-angleToDest)} < 0.3")
            self.actions.add("Forward")
        else:
            if("Forward" in self.actions):
                self.actions.remove("Forward")
        if(math.pi-0.3 < abs(self.dir-angleToDest) < math.pi+0.3):
            self.actions.add("Backward")
        else:
            if("Backward" in self.actions):
                self.actions.remove("Backward")
        if(self.dir < angleToDest and abs(self.dir-angleToDest) < (2*math.pi)-0.2):
            # print(f"{self.dir} < {angleToDest}")
            # print("rotate right")
            self.actions.add("Right")
        else:
            if("Right" in self.actions):
                self.actions.remove("Right")
        # if(self.dir > angleToDest and 
        # (self.dir-angleToDest < math.pi)):
        if(self.dir > angleToDest and abs(self.dir-angleToDest) < (2*math.pi)-0.2):
            # print(f"{self.dir} > {angleToDest}")
            # print("rotate left")
            self.actions.add("Left")
        else:
            if("Left" in self.actions):
                self.actions.remove("Left")
    def aim(self, dir):
        if dir-0.01 < self.turretDir < dir+0.01:
            # print("shoot0")
            self.actions.add("Shoot")
        else:
            if(abs(self.turretDir-dir) > math.pi/15):
                if(self.turretDir > dir and 
                (self.turretDir-dir < math.pi)):
                    # print("rotate turret left")
                    self.rotateTurret("Left")
                # if(self.turretDir < angleToPlayer):
                else:
                    # print("rotate turret right")
                    self.rotateTurret("Right")
    def getLineToTarget(self, px, py):
        if self.y == py:
            # print(f"{self.y} == {py}")
            lineToTarget = LineH((self.x, self.y),(px, py))
        elif self.x == px:
            lineToTarget = LineV((self.x, self.y),(px, py))
        else:
            # print(f"diagonal line")
            lineToTarget = LineD((self.x, self.y),(px, py))
        return lineToTarget
    def aimAtPlayer(self, px, py):
        angleToPlayer = angle(self.x , self.y, px, py)
        while (self.turretDir-angleToPlayer >= 2*math.pi):
            self.turretDir -= 2*math.pi
        while (self.turretDir-angleToPlayer < 0):
            self.turretDir += 2*math.pi
        # print(f"self.turretDir = {self.turretDir}")
        # print(f"angleToPlayer = {angleToPlayer}")
        if(abs(self.turretDir-angleToPlayer) > math.pi/15):
            if(self.turretDir > angleToPlayer and 
            (self.turretDir-angleToPlayer < math.pi)):
                # print("rotate turret left")
                self.rotateTurret("Left")
            # if(self.turretDir < angleToPlayer):
            else:
                # print("rotate turret right")
                self.rotateTurret("Right")
        if(abs(self.turretDir-angleToPlayer) < 0.1):
            self.actions.add("Shoot")

def angle(x1, y1, x2, y2):
    # Returns the angle from point 1 to 2
    if(x2-x1 == 0):
        if(y1 > y2):
            return -math.pi/2
        if(y1 < y2):
            return math.pi/2
    return math.atan2((y2-y1),(x2-x1))