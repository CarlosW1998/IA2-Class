from random import choice, randint
from time import time
import os

class ImaginaryCity:
    def __init__(self):
        self.city = [[' ' for i in range(19)] for j in range(19)]
        self.logicCity = [[1 for i in range(19)] for j in range(19)]
        self.semafory = []
        for i in range(19):
            for j in range(19):
                if i == 0:
                    self.city[i][j] = 'L'
                    self.logicCity[i][j] = 0
                if i == 18:
                    self.city[i][j] = 'R'
                    self.logicCity[i][j] = 0
                if i == 6:
                    self.city[i][j] = 'R'
                    self.logicCity[i][j] = 0
                if i == 12:
                    self.city[i][j] = 'L'
                    self.logicCity[i][j] = 0
                if (i == 0 or i == 18) and (j == 0 or j == 18): continue
                if j%6 == 0 and j < 10:
                    if self.city[i][j] == ' ': self.city[i][j] = 'D'
                    else: self.city[i][j] += 'D'
                    self.logicCity[i][j] = 0
                if j%6 == 0 and j > 10:
                    if self.city[i][j] == ' ': self.city[i][j] = 'U'
                    else:self.city[i][j] += 'U'
                    self.logicCity[i][j] = 0
                    
        for i in range(19):
            for j in range(19):
                if len(self.city[i][j]) > 1:
                    self.semafory.append(TrafficLight((i, j), self.city[i][j][0], self.city[i][j][1], randint(1, 10)))


        self.city[0][0] = 'D'
        self.city[18][18] = 'U'
        self.city[12][0] = 'D'
        self.city[0][12] = 'L'
        self.city[6][18] = 'U'
        self.city[18][6] = 'R'
        

    def getState(self):
        #for i in self.city:
        #    for j in i:
        #        print('%3s' % (j), end = '')
        #    print()
        #print()
        for i in self.logicCity:
            for j in i:
                print('%3d' % (j), end = '')
            print()
        print()
        #for i in self.semoforyCity:
        #    for j in i:
        #        print('%3d' % (j), end = '')
        #    print()

    def getValidMoves(self, y, x):
        if x >= 19 or x < 0: return None
        if y >= 19 or y < 0: return None
        roads = []
        if "U" in self.city[y][x]: roads.append((y-1, x))
        if "D" in self.city[y][x]: roads.append((y+1, x))
        if "R" in self.city[y][x]: roads.append((y, x+1))
        if "L" in self.city[y][x]: roads.append((y, x-1))
        return roads

class Car:
    def __init__(self, start, end, time,timeToStart):
        self.start = start
        self.end = end
        self.time = time
        self.locate = start
        self.arrive = False
        self.timeStart = timeToStart
        
    def update(self, y, x):
        self.locate = (y, x)

    def nextStep(self, possibilites):
        return choice(possibilites)

    def getPosition(self, y, x):
        return self.locate

class TrafficLight:
    def __init__(self, position, d1, d2, steps):
        self.conf = {}
        self.conf[d1] = False
        self.conf[d2] = True
        self.d1 = d1
        self. d2 = d2
        self.position = position
        self.steps = steps
    
    def changeMode(self, step):
        if step%self.steps == 0:
            if self.conf[self.d1] == False:
                self.conf[self.d1] = True
                self.conf[self.d2] = False
            else:
                self.conf[self.d1] = False
                self.conf[self.d2] = True

    
    def __bool__(self): return True
    def __int__(self): return 1

class AmbienteCity:
    def __init__(self, stepTime=0.001, agents = 20, log=True):
        self.city = ImaginaryCity()
        self.stepTime = stepTime
        self.steps = 1
        self.agents = [getRandomCarState(self.city.logicCity) for i in range(agents)]
        self.colisions = 0
        self.log = log

    def executeStep(self):
        finished = True
        for i in self.agents:
            if not i.arrive:
                finished = False
                if i.locate == i.end:
                    self.city.logicCity[i.locate[0]][i.locate[1]] = 0
                    i.arrive = True
                    i.locate = (1000, 1000)
                    continue
                if self.steps%i.time == 0 and i.timeStart <= self.steps:
                    j = i.nextStep(self.city.getValidMoves(*i.locate))
                    if j in [a.locate for a in self.agents]:
                        if self.log: print("Colision on ", *i.locate, " to", *j, end = ' | ')
                        self.colisions += 1
                    else:
                        s = get(self.city.semafory, j)
                        if s:
                            if s.conf[self.city.city[i.locate[0]][i.locate[1]]]:
                                self.city.logicCity[i.locate[0]][i.locate[1]] = 0
                                i.locate = j
                                self.city.logicCity[i.locate[0]][i.locate[1]] = 5
                            else:
                                if self.log: print("Semafory Colision on ", *i.locate, end = ' ')                                
                        else:
                            self.city.logicCity[i.locate[0]][i.locate[1]] = 0
                            i.locate = j
                            self.city.logicCity[i.locate[0]][i.locate[1]] = 5
        for i in self.city.semafory:
            i.changeMode(self.steps)
                            
        return finished



    def execute(self):
        t = time()
        while True:
            if (time() - t) > self.stepTime:
                if self.log: print("Step ",self.steps, ": ", end = ' ')
                #self.city.getState()
                t = time()
                self.steps += 1
                if self.executeStep(): 
                    if self.log: print()
                    break
                if self.log: print()
        print("Colision: ", self.colisions)




def getRandomCarState(city):
    x, y = randint(0, 18), randint(0, 18)
    while city[y][x] != 0:x, y = randint(0, 18), randint(0, 18)
    city[y][x] = 5
    start = (y, x)
    x, y = randint(0, 18), randint(0, 18)
    while city[y][x] == 1:x, y = randint(0, 18), randint(0, 18)
    end = (y, x)
    step = 1
    return Car(start, end, step, randint(0, 5))

def get(sem, p):
    for i in sem:
        if i.position == p: return i

    return None