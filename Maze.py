#################################################
# TP
#
# Your name: Justin Wang
# Your andrew id: jyw2
#################################################

# Maze class, with functions to generate new mazes through recursive
# backtracking, get certain parameters, and generate a graph object for the AI

from Cell import Cell
from Graph import Graph
import copy, random

class Maze(object):
    def __init__(self, rows, cols, cellSize):
        self.cols = cols
        self.rows = rows
        self.cellSize = cellSize
        self.maze = [ ([0] * self.cols) for row in range(self.rows) ]
        for x in range(self.rows):
            for y in range(self.cols):
                self.maze[x][y] = Cell(x, y, cellSize)
    def __repr__(self):
        for r in self.rows:
            for c in self.cols:
                print(self.maze[r][c].n)
    def generateMaze(self):
        mazeGrid = copy.deepcopy(self.maze)
        row = random.randint(0,self.rows-1)
        col = random.randint(0,self.cols-1)
        self.maze = self.generateMazeBacktrack(mazeGrid, row, col, row, col)
    def generateMazeBacktrack(self, grid, row, col, startRow, startCol):
        # print(row, col)
        grid[row][col].visited = True
        moves = [(1,0,"south"), (0,1,"east"), (-1,0,"north"), (0,-1,"west")]
        random.shuffle(moves)
        for move in moves:
            newRow = row+move[0]
            newCol = col+move[1]
            if self.checkLegalMove(grid, newRow, newCol):
                if(move[2] == "east"):
                    # print("east")
                    # print(f"going to: {newRow, newCol}")
                    grid[row][col].e = False
                    grid[newRow][newCol].w = False
                elif(move[2] == "north"):
                    # print("north")
                    # print(f"going to: {newRow, newCol}")
                    grid[row][col].n = False
                    grid[newRow][newCol].s = False
                elif(move[2] == "west"):
                    # print("west")
                    # print(f"going to: {newRow, newCol}")
                    grid[row][col].w = False
                    grid[newRow][newCol].e = False
                elif(move[2] == "south"):
                    # print("south")
                    # print(f"going to: {newRow, newCol}")
                    grid[row][col].s = False
                    grid[newRow][newCol].n = False
                solution = self.generateMazeBacktrack(grid, newRow, newCol, 
                    startRow, startCol)
                if(solution != None):
                    return solution
        if(row == startRow and col == startCol):
            # print(row, col)
            # print("ended")
            return grid
        return None
    def checkLegalMove(self, grid, row, col):
        if(row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0])):
            return False
        if grid[row][col].visited == True:
            return False
        return True
    def getCell(self, row, col):
        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):
                cell = self.maze[r][c]
                # print(f"cell.row {cell.row}")
                # print(f"cell.col {cell.col}")
                # print(f"cell = {cell}")
                if (cell.row == row and cell.col == col):
                    return cell
    def whichCell(self, px, py):
        # Returns which cell a point is in
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                cell = self.maze[row][col]
                if(cell.v1[0] <= px < cell.v2[0] and 
                cell.v1[1] <= py <= cell.v3[1]):
                    return cell
    def generateGraph(self):
        newGraph = Graph()
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                cell = self.maze[row][col]
                rowCol = (cell.row, cell.col)
                newGraph.table[rowCol] = set()
                # print(rowCol)
                if(cell.row > 0 and not cell.n):
                    rowColNorth = (cell.row-1, cell.col)
                    newGraph.addEdge(rowCol, rowColNorth)
                if(cell.row < len(self.maze)-1 and not cell.s):
                    rowColSouth = (cell.row+1, cell.col)
                    newGraph.addEdge(rowCol, rowColSouth)
                if(cell.col > 0 and not cell.w):
                    rowColWest = (cell.row, cell.col-1)
                    newGraph.addEdge(rowCol, rowColWest)
                if(cell.col < len(self.maze[0])-1 and not cell.e):
                    rowColEast = (cell.row, cell.col+1)
                    newGraph.addEdge(rowCol, rowColEast)
        return newGraph