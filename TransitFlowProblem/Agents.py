class ImaginaryCity:
    def __init__(self):
        self.city = [[' ' for i in range(19)] for j in range(19)]
        for i in range(19):
            for j in range(19):
                if i == 0:
                    self.city[i][j] = 'L'
                if i == 18:
                    self.city[i][j] = 'R'
                if i == 6:
                    self.city[i][j] = 'R'
                if i == 12:
                    self.city[i][j] = 'L'
                if (i == 0 or i == 18) and (j == 0 or j == 18): continue
                if j%6 == 0 and j < 10:
                    if self.city[i][j] == ' ': self.city[i][j] = 'D'
                    else : self.city[i][j] += 'D'
                if j%6 == 0 and j > 10:
                    if self.city[i][j] == ' ': self.city[i][j] = 'U'
                    else:self.city[i][j] += 'U'
        self.city[0][0] = 'D'
        self.city[18][18] = 'U'

    def getState(self):
        for i in self.city:
            for j in i:
                print('%3s' % (j), end = '')
            print()

    def getValidMoves(self, x, y):
        if x >= 19 or x < 0: return None
        if y >= 19 or y < 0: return None
        roads = []
        if "U" in self.city[y][x]: roads.append((x, y-1))
        if "D" in self.city[y][x]: roads.append((x, y+1))
        if "R" in self.city[y][x]: roads.append((x+1, y))
        if "L" in self.city[y][x]: roads.append((x-1, y))
        return roads

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self, x, y):
        self.x = x
        self.y = y
    def getPosition(self, x, y):
        return (self.x, self.y)