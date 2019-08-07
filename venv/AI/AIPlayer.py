import numpy as np
import keras
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import Nadam
from AI.Genome import INPUT_SIZE, LAYER_SIZE, OUTPUT_SIZE
from AI.Species import Species
from GAME.Player import Player
from GAME.Player import SPACE
from GAME.Player import WIDTH
from GAME.Ball import Ball

def getModel(drop_out: bool = True, alpha: float = 0.1, lr: float = 0.001) -> Sequential:
    model = Sequential()
    model.add(Dense(LAYER_SIZE, input_dim=INPUT_SIZE, activation="sigmoid"))
    if drop_out:
        model.add(Dropout(alpha))
    model.add(Dense(LAYER_SIZE, activation="sigmoid"))
    if drop_out:
        model.add(Dropout(alpha))
    model.add(Dense(LAYER_SIZE, activation="sigmoid"))
    if drop_out:
        model.add(Dropout(alpha))
    model.add(Dense(OUTPUT_SIZE, activation="softmax"))

    model.compile(optimizer=Nadam(lr=lr), loss="categorical_crossentropy")

    return model

AI_Model = getModel()

class AIPlayer(Player):
    def __init__(self, playerID: int, windowSize: (int, int), species: Species, store_history: bool = True, isTarget: bool = False):
        super().__init__(playerID, windowSize)
        self.species = species
        self.species.gene.model = AI_Model
        self.species.gene.updateModel()
        self.history = []
        self.store_history = store_history
        self.isTarget = isTarget

    def getAction(self, enemy, ball: Ball) -> np.ndarray:
        input = self.getInput(enemy, ball)
        action = self.species.gene.getOutput(np.asarray([input]))
        if self.store_history:
            self.history.append([input, action])

        return action

    def getInput(self, enemy: Player, ball: Ball) -> list:
        if not self.isTarget:
            return self._getInput2(enemy, ball)

        input = []
        space = SPACE() + WIDTH()
        collisionPoints = self.getCollisionPoint(ball)

        input.append(
            np.max([collisionPoints[1] - self.y, 0]) if self.windowSize[1] - space == collisionPoints[0] else 0)
        input.append(
            np.max([self.y - collisionPoints[1], 0]) if self.windowSize[1] - space == collisionPoints[0] else 0)
        input.append(
            np.max([collisionPoints[0] - self.x, 0]) if self.windowSize[0] - space == collisionPoints[1] else 0)
        input.append(
            np.max([self.x - collisionPoints[0], 0]) if self.windowSize[0] - space == collisionPoints[1] else 0)

        input.append(np.max([collisionPoints[1] - enemy.y, 0]) if space == collisionPoints[0] else 0)
        input.append(np.max([enemy.y - collisionPoints[1], 0]) if space == collisionPoints[0] else 0)
        input.append(np.max([collisionPoints[0] - enemy.x, 0]) if space == collisionPoints[1] else 0)
        input.append(np.max([enemy.x - collisionPoints[0], 0]) if space == collisionPoints[1] else 0)

        input.append(self.x / self.windowSize[0])
        input.append(self.y / self.windowSize[1])
        input.append(enemy.x / self.windowSize[0])
        input.append(enemy.x / self.windowSize[1])

        input.append(ball.x / self.windowSize[0])
        input.append(ball.y / self.windowSize[1])
        input.append((self.windowSize[0] - ball.x) / self.windowSize[0])
        input.append((self.windowSize[1] - ball.y) / self.windowSize[1])

        input.append(ball.x < self.windowSize[0] / 2.0)
        input.append(ball.x > self.windowSize[0] / 2.0)
        input.append(ball.y < self.windowSize[1] / 2.0)
        input.append(ball.y > self.windowSize[1] / 2.0)

        ballAngle = np.arctan2(ball.vY, ball.vX)

        input.append(np.cos(ballAngle))
        input.append(np.sin(ballAngle))

        input.extend(self.lastAction)
        # input.extend(enemy.lastAction)

        return input

    def _getInput2(self, enemy: Player, ball: Ball) -> list:
        input = []
        space = SPACE() + WIDTH()
        collisionPoints = self.getCollisionPoint(ball)

        input.append(np.max([collisionPoints[1] - self.y, 0]) if space == collisionPoints[0] else 0)
        input.append(np.max([self.y - collisionPoints[1], 0]) if space == collisionPoints[0] else 0)
        input.append(np.max([collisionPoints[0] - self.x, 0]) if space == collisionPoints[1] else 0)
        input.append(np.max([self.x - collisionPoints[0], 0]) if space == collisionPoints[1] else 0)

        input.append(
            np.max([collisionPoints[1] - enemy.y, 0]) if self.windowSize[1] - space == collisionPoints[0] else 0)
        input.append(
            np.max([enemy.y - collisionPoints[1], 0]) if self.windowSize[1] - space == collisionPoints[0] else 0)
        input.append(
            np.max([collisionPoints[0] - enemy.x, 0]) if self.windowSize[0] - space == collisionPoints[1] else 0)
        input.append(
            np.max([enemy.x - collisionPoints[0], 0]) if self.windowSize[0] - space == collisionPoints[1] else 0)

        input.append(self.x / self.windowSize[0])
        input.append(self.y / self.windowSize[1])
        input.append(enemy.x / self.windowSize[0])
        input.append(enemy.x / self.windowSize[1])

        input.append((self.windowSize[0] - ball.x) / self.windowSize[0])
        input.append((self.windowSize[1] - ball.y) / self.windowSize[1])
        input.append(ball.x / self.windowSize[0])
        input.append(ball.y / self.windowSize[1])

        input.append(ball.x > self.windowSize[0] / 2.0)
        input.append(ball.x < self.windowSize[0] / 2.0)
        input.append(ball.y > self.windowSize[1] / 2.0)
        input.append(ball.y < self.windowSize[1] / 2.0)

        ballAngle = np.arctan2(-ball.vY, -ball.vX)

        input.append(np.cos(ballAngle))
        input.append(np.sin(ballAngle))

        input.extend(self.lastAction)
        # input.extend(enemy.lastAction)

        return input

    def getCollisionPoint(self, ball: Ball) -> list:
        points = []
        ballCollisionPoints = ball.getCollisionPoints()

        if ballCollisionPoints["wallUP"] != -1:
            return [ballCollisionPoints["wallUP"], SPACE() + WIDTH()]

        if ballCollisionPoints["wallRIGHT"] != -1:
            return [self.windowSize[0] - SPACE() - WIDTH(), ballCollisionPoints["wallRIGHT"]]

        if ballCollisionPoints["wallDOWN"] != -1:
            return [ballCollisionPoints["wallDOWN"], self.windowSize[1] - SPACE() - WIDTH()]

        if ballCollisionPoints["wallLEFT"] != -1:
            return [SPACE() + WIDTH(), ballCollisionPoints["wallLEFT"]]

        return [0, 0] # Error