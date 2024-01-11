#################################################
# TP
#
# Your name: Justin Wang
# Your andrew id: jyw2
#################################################

# Graph object is primarily used to implement Dijkstra's algorithm in the AI for
# a pathfinding algorithm

import math

class Graph(object):
    def __init__(self):
        self.table = {}
    def addEdge(self, node1, node2):
        if(node1 not in self.table):
            self.table[node1] = set(node2)
        else:
            self.table[node1].add(node2)
        if(node2 not in self.table):
            self.table[node2] = set(node1)
        else:
            self.table[node2].add(node1)
    def getNeighbors(self, node):
        return self.table[node]
    def getNodes(self):
        # print(self.table)
        nodes = []
        for node in self.table:
            # print(f"node: {node}")
            nodes.append(node)
        # print(f"nodes: {nodes}")
        return nodes
    def getPath(self, startNode, endNode):
        # print(f"startNode = {startNode}")
        # print(f"endNode = {endNode}")
        distances = {}
        visitedNodes = set()
        prevNodes = {}
        # print(f"nodes: {self.getNodes()}")
        for node in self.getNodes():
            if(node == startNode):
                distances[node] = 0
                visitedNodes.add(node)
            else:
                distances[node] = math.inf
        # print(distances)
        queue = [startNode]
        while len(queue) > 0:
            # print("getting path")
            # print(f"node = {node}")
            # print(f"queue = {queue}")
            node = queue.pop(0)
            # print(node)
            # print(self.getNeighbors(node))
            if(node == endNode):
                # print(f"node({node}) == startNode({startNode})")
                # print(f"getPath0 prevNodes = {prevNodes}")
                return prevNodes
            # print(f"node({node}) == startNode({startNode})")
            for neighbor in self.getNeighbors(node):
                # print(f"neighbor = {neighbor}")
                if(neighbor not in visitedNodes):
                    # print("here")
                    visitedNodes.add(neighbor)
                    # distances[neighbor] = distances[node] + 1
                    prevNodes[neighbor] = node
                    # print(f"prevNodes[{node}] = {neighbor}")
                    queue.append(neighbor)
                    if(neighbor == startNode):
                        # print(f"getPath1 prevNodes = {prevNodes}")
                        return prevNodes
    def tracePath(self, startNode, endNode, prevNodes):
        path = [endNode]
        # print(path)
        currentNode = endNode
        while (currentNode != startNode):
            # print(prevNodes[currentNode])
            path.insert(0, prevNodes[currentNode])
            currentNode = prevNodes[currentNode]
        # print(path)
        return path