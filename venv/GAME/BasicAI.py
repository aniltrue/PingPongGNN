import numpy as np
import math
import random as rnd
from GAME.Player import Player
from GAME.Ball import Ball

class BasicAIPlayer(Player):
    def getAction(self, enemy: Player, ball: Ball) -> np.ndarray:
        self.beta = 0
        action = self.getActionBasicAI(ball, "wallUP", "wallLEFT") if self.playerID == 0 else self.getActionBasicAI(ball, "wallDOWN", "wallRIGHT")
        return np.array([action])

    def getActionBasicAI(self, ball: Ball, firstWall: str, secondWall: str) -> list:
        alpha = self.windowSize[0] * self.beta if self.windowSize[0] < self.windowSize[1] else self.windowSize[1] * self.beta
        action = []

        diff1, diff2 = self.getDiferences(ball)
        collisionPoints = ball.getCollisionPoints()

        if collisionPoints[firstWall] != -1.0:
            c1 = collisionPoints[firstWall] + 2.0 * alpha * rnd.random() - alpha

            if c1 - ball.size < self.x:
                action.extend([0, 0, 1]) # LEFT
            elif c1 + ball.size > self.x + self.size:
                action.extend([1, 0, 0]) # RIGHT
            else:
                action.extend([0, 1, 0]) # STOP

        else:
            diff1 += 2.0 * alpha * rnd.random() - alpha
            if diff1 < 0:
                action.extend([1, 0, 0])  # RIGHT
            elif diff1 > 0:
                action.extend([0, 0, 1])  # LEFT
            else:
                action.extend([0, 1, 0])  # STOP

        if collisionPoints[secondWall] != -1.0:
            c2 = collisionPoints[secondWall]  + 2.0 * alpha * rnd.random() - alpha

            if c2 - ball.size < self.y:
                action.extend([1, 0, 0])  # UP
            elif c2 + ball.size > self.y + self.size:
                action.extend([0, 0, 1])  # DOWN
            else:
                action.extend([0, 1, 0])  # STOP

        else:
            diff2 += 2.0 * alpha * rnd.random() - alpha
            if diff2 < 0:
                action.extend([0, 0, 1])  # DOWN
            elif diff2 > 0:
                action.extend([1, 0, 0])  # UP
            else:
                action.extend([0, 1, 0])  # STOP

        return [self.old2New(action)]