import numpy as np
import random as rnd
from AI.Genome import Genome
from GAME.Player import Player
from GAME.Ball import Ball

MUTATION_CHANCE = 0.1
RANDOM_MUTATION_CHANCE = 0.4
WEIGHT_DISTRIBUTION = 0.25
WEIGHT_RANGE = 1.0
PARENT1_CHANCE = 0.5
PARENT2_CHANCE = 0.4

def abs(x):
    return -x if x < 0 else x

class Species:
    def __init__(self, gene: Genome = None):
        self.gene = gene if gene != None else Genome()

    def crossingOver(self, parent):
        if self.gene < parent.gene:
            return parent.crossingOver(self)

        childWeights = []
        for (i, weight) in enumerate(self.gene.weights):
            childW = self.crossMatrices(weight[0], parent.gene.weights[i][0])
            chance = rnd.random()
            childB = parent.gene.weights[i][1] if chance < 1.0 - PARENT1_CHANCE else weight[1]
            childWeights.append([childW, childB])

        return Species(Genome(childWeights))

    def crossMatrices(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        if parent1.shape != parent2.shape:
            pass

        child = np.zeros(parent1.shape)

        for i in range(parent1.shape[0]):
            for j in range(parent1.shape[1]):
                chance = rnd.random()
                value = parent1[i][j]
                if chance < 1.0 - (PARENT1_CHANCE + PARENT2_CHANCE):
                    value = (parent1[i][j] + parent2[i][j]) / 2.0
                elif chance < 1.0 - PARENT1_CHANCE:
                    value = parent2[i][j]

                child[i][j] = self.mutateValue(value)

        return child

    def mutateValue(self, value: float) -> float:
        chance = rnd.random()

        if chance > MUTATION_CHANCE:
            return value

        if chance <= RANDOM_MUTATION_CHANCE:
            return (value + (2.0 * WEIGHT_RANGE * rnd.random() - WEIGHT_RANGE)) / 2.0

        uniform = 2.0 * WEIGHT_DISTRIBUTION * rnd.random() - WEIGHT_DISTRIBUTION
        value += uniform

        '''
        if value > WEIGHT_RANGE:
            value = WEIGHT_RANGE

        if value < -WEIGHT_RANGE:
            value = WEIGHT_RANGE
        '''

        return value

    def calculateFitness(self, me: Player, enemy: Player, ball: Ball) -> int:
        initialPoint = 2 * me.point + 100 if ball.getWinner() == me.playerID and me.point > 0 else me.point

        diff1, diff2 = me.getDiferences(ball)
        ballDiff = ball.getDifferences()

        fitness = initialPoint - (enemy.point / 2)

        hWall = "wallDOWN" if me.playerID == 1 else "wallUP"
        vWall = "wallRIGHT" if me.playerID == 1 else "wallLEFT"

        if ball.getWinner() == enemy.playerID and me.point > 0:
            fitness -= abs(diff2) / 10 if ballDiff[hWall] < ballDiff[vWall] else abs(diff1) / 10
        elif ball.getWinner() == enemy.playerID:
            fitness -= abs(diff2) / 25 if ballDiff[hWall] < ballDiff[vWall] else abs(diff1) / 25

        self.gene.setFitness(fitness)

        return self.gene.fitness