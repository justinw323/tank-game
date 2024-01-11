#################################################
# TP
#
# Your name: Justin Wang
# Your andrew id: jyw2
#################################################

# Maze is made up of cells. Cell object is useful for getting locations within
# the maze, as well as generating walls

from Wall import Wall

class Cell(object):
    def __init__(self, row, col, side):
        self.side = side
        self.row = row
        self.col = col
        self.visited = False
        self.n = True
        self.e = True
        self.s = True
        self.w = True
        self.v1 = (80*self.col + 80, 80*self.row + 80)
        self.v2 = (80*(self.col+1) + 80, 80*(self.row) + 80)
        self.v3 = (80*(self.col+1) + 80, 80*(self.row+1) + 80)
        self.v4 = (80*(self.col) + 80, 80*(self.row+1) + 80)
    def getCenterCoordinates(self):
        return (80*self.col + 120, 80*self.row + 120)
    def getNorthWallCoordinates(self):
        w1 = (self.v1[0], self.v1[1]-2)
        w2 = (self.v2[0], self.v2[1]-2)
        w3 = (self.v2[0], self.v2[1]+2)
        w4 = (self.v1[0], self.v1[1]+2)
        return w1, w2, w3, w4
    def getEastWallCoordinates(self):
        w1 = (self.v2[0]-2, self.v2[1])
        w2 = (self.v2[0]+2, self.v2[1])
        w3 = (self.v3[0]+2, self.v3[1])
        w4 = (self.v3[0]-2, self.v3[1])
        return w1, w2, w3, w4
    def getSouthWallCoordinates(self):
        w1 = (self.v4[0], self.v4[1]-2)
        w2 = (self.v3[0], self.v3[1]-2)
        w3 = (self.v3[0], self.v3[1]+2)
        w4 = (self.v4[0], self.v4[1]+2)
        return w1, w2, w3, w4
    def getWestWallCoordinates(self):
        w1 = (self.v1[0]-2, self.v1[1])
        w2 = (self.v1[0]+2, self.v1[1])
        w3 = (self.v4[0]+2, self.v4[1])
        w4 = (self.v4[0]-2, self.v4[1])
        return w1, w2, w3, w4
    def buildWalls(self):
        walls = []
        if self.n:
            v1, v2, v3, v4 = self.getNorthWallCoordinates()
            walls.append(Wall(v1, v2, v3, v4))
        if self.e:
            v1, v2, v3, v4 = self.getEastWallCoordinates()
            walls.append(Wall(v1, v2, v3, v4))
        if self.s:
            v1, v2, v3, v4 = self.getSouthWallCoordinates()
            walls.append(Wall(v1, v2, v3, v4))
        if self.w:
            v1, v2, v3, v4 = self.getWestWallCoordinates()
            walls.append(Wall(v1, v2, v3, v4))
        return walls