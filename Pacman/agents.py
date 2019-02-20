import math
import random
import arcade
from states import AgentState

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, direction):
        if not direction:
            return False
        if direction == 1:
            self.x+=1
            return True
        if direction == 2:
            self.x -= 1
            return True
        if direction == 3:
            self.y += 1
            return True
        if direction == 4:
            self.y -= 1
            return True
        return False
    def drawn(self): pass


class Gosth:
    def __init__(self, x, y, size, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.size = size
        self.time = 0
        self.path = None
        self.state = AgentState.SEARCH

    def move(self, coordinates):
        direction = self.getMoviment()
        if not direction:
            return False
        if direction == 1:
            if coordinates[self.y][self.x+1] == 1: return False
            self.x+=1
            return True
        if direction == 2:
            if coordinates[self.y][self.x-1] == 1: return False
            self.x -= 1
            return True
        if direction == 3:
            if coordinates[self.y+1][self.x] == 1: return False
            self.y += 1
            return True
        if direction == 4:
            if coordinates[self.y-1][self.x] == 1: return False
            self.y -= 1
            return True
        return False
        
    def getMoviment(self):
        if self.state == AgentState.SEARCH:
            return random.randint(0, 5)
        
    def drawn(self):
        arcade.draw_circle_filled(self.x*self.scale, self.y*self.scale, self.size, arcade.color.GREEN)