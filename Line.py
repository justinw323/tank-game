#################################################
# TP
#
# Your name: Justin Wang
# Your andrew id: jyw2
#################################################

# Line objects are used to calculate hitbox collisions for tanks, bullets, and
# obstacles, as well as for the AI's aiming system

class Line(object):
    def __init__(self, p1, p2):
        self.endpoint1 = p1
        self.endpoint2 = p2
        self.type = None
    def comparePointToLine(self, px, py):
        if(py > px*self.m + self.b):
            return ">"
        elif(py == px*self.m + self.b):
            return "="
        elif(py < px*self.m + self.b):
            return "<"

class LineD(Line):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        # Of the form y = mx+b
        self.m = (p1[1]-p2[1])/(p1[0]-p2[0])
        self.b = self.m*(-p1[0]) + p1[1]
        # of the form x = (1/m)*y - b/m
        self.m2 = 1/self.m
        self.b2 = -self.b/self.m
        self.type = "lineD"

class LineH(Line):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        self.y = p1[1]
        self.endpointx1 = p1[0]
        self.endpointx2 = p2[0]
        self.type = "lineH"

class LineV(Line):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        self.x = p1[0]
        self.endpointy1 = p1[1]
        self.endpointy2 = p2[1]
        self.type = "lineV"