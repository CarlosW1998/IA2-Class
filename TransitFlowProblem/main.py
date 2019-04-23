from Agents import AmbienteCity, ImaginaryCity
from random import randint, choice


GlobalAmbient = AmbienteCity()
Gloalconfiguration = GlobalAmbient.agents

populationSize = 50
generations = 10
cromossomeSize = 12

class Individual:
    def __init__(self, cromossome):
        self.cromossome = cromossome
        self.value = getValue(self.cromossome)
    def __int__(self): return self.value
    def __float__(self): return self.value


def key(i):
    return i.value

def getValue(individual):
    GlobalAmbient.reset(preAgents=[i.copy()for i in Gloalconfiguration])
    for i, j in zip(individual, GlobalAmbient.city.semafory):
        j.steps = i
    return GlobalAmbient.execute()

def getPopulation():
    pop = [Individual([randint(1, 10) for i in range(cromossomeSize)]) for i in range(populationSize)]
    pop.sort(key=key)
    return pop


def cross(c1, c2):
    newc = []
    for elit, noElit in zip(c1, c2):
        if randint(0, 100) > 70:
            newc.append(noElit)
        else:
            newc.append(elit)
    return newc

def Mutation(cromossome):
    if randint(1, 100) > 95:
        cromossome[randint(0, cromossomeSize-1)] = randint(1, 10)

def nextPopulation(population):
    nPop = []
    cutPoint = int(len(population)*0.2)
    for i in population[:cutPoint]:
        nPop.append(i)
    for i in population[cutPoint:]:
        newi = cross(choice(population[:cutPoint]).cromossome,\
             choice(population[cutPoint:]).cromossome)
        Mutation(newi)
        nPop.append(Individual(newi))
    nPop.sort(key=key)
    return nPop

pop = getPopulation()

for i in range(generations):
    print(pop[0].value)
    pop = nextPopulation(pop)

def __main__():
    print("BUIA")