#################################################
# TP
#
# Your name: Justin Wang
# Your andrew id: jyw2
#################################################

# Bullet object contains parameters and functions to move the bullets around
# the map

import math

class Bullet(object):
    def __init__(self, x, y, dir, shooter):
        self.x = x
        self.y = y
        self.r = 3
        self.color = "black"
        self.dir = dir
        self.distance = 0
        self.maxDistance = 1200
        self.shooter = shooter
    def reachedMaxDistance(self):
        return self.distance > self.maxDistance
    def moveBullet(self):
        self.x += 4*math.cos(self.dir)
        self.y += 4*math.sin(self.dir)
        self.distance += 4