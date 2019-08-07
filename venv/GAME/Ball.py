import random as rnd
import math
import pygame
from GAME import Player

class Ball:
    def __init__(self, windowSize: (int, int)):
        self.windowSize = windowSize
        self.size = windowSize[0] / 100.0 if windowSize[0] < windowSize[1] else windowSize[1] / 100.0

        angle = 165.0 * rnd.random() - 30.0
        while (angle >= 40 and angle <= 50) or (angle >= 85 and angle <= 95) or (angle >= -5 and angle <= 5):
            angle = 165.0 * rnd.random() - 30.0

        self.restart(angle)

    def restart(self, angle: float):
        angle = math.pi * angle / 180.0

        self.x = self.windowSize[1] / 2.0
        self.y = self.windowSize[0] / 2.0

        self.vX = math.cos(angle) * self.VELOCITY()
        self.vY = math.sin(angle) * self.VELOCITY()

    def VELOCITY(self) -> float:
        return self.size / 2

    def draw(self, screen: pygame.Surface, showTargetPoint = True):
        color = [255, 0, 0]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

        if not showTargetPoint:
            return

        collisionPoints = self.getCollisionPoints()
        point = [0.0, 0.0]

        if collisionPoints["wallUP"] != -1.0:
            point[0] = collisionPoints["wallUP"]
            point[1] = Player.SPACE() + Player.WIDTH()

        elif collisionPoints["wallRIGHT"] != -1.0:
            point[0] = self.windowSize[1] - Player.SPACE() - Player.WIDTH()
            point[1] = collisionPoints["wallRIGHT"]

        elif collisionPoints["wallDOWN"] != -1.0:
            point[0] = collisionPoints["wallDOWN"]
            point[1] = self.windowSize[0] - Player.SPACE() - Player.WIDTH()

        elif collisionPoints["wallLEFT"] != -1.0:
            point[0] = Player.SPACE() + Player.WIDTH()
            point[1] = collisionPoints["wallLEFT"]

        point[0] = int(point[0])
        point[1] = int(point[1])

        pygame.draw.circle(screen, color, point, 5)

    def getDifferences(self) -> dict:
        return { "wallUP": self.y,
                 "wallDOWN": self.windowSize[0] - self.y,
                 "wallRIGHT": self.windowSize[1] - self.x,
                 "wallLEFT": self.x }

    def getCollisionPoints(self) -> dict:
        points =  { "wallUP": -1.0, "wallRIGHT": -1.0, "wallDOWN": -1.0, "wallLEFT": -1.0 }

        if self.vY != 0:
            t = (Player.SPACE() + Player.WIDTH() - self.y) / self.vY
        else:
            t = -1
        points["wallUP"] = self.x + self.vX * t
        if t < 0 or points["wallUP"] < 0 or points["wallUP"] > self.windowSize[1] or self.vY > 0:
            points["wallUP"] = -1.0


        if self.vX != 0:
            t = (self.windowSize[1] - self.x - Player.SPACE() - Player.WIDTH()) / self.vX
        else:
            t = -1
        points["wallRIGHT"] = self.y + self.vY * t
        if t < 0 or points["wallRIGHT"] < 0 or points["wallRIGHT"] > self.windowSize[0] or self.vX < 0:
            points["wallRIGHT"] = -1.0

        if self.vY != 0:
            t = (self.windowSize[0] - self.y - Player.SPACE() - Player.WIDTH()) / self.vY
        else:
            t = -1
        points["wallDOWN"] = self.x + self.vX * t
        if t < 0 or points["wallDOWN"] < 0 or points["wallDOWN"] > self.windowSize[1] or self.vY < 0:
            points["wallDOWN"] = -1.0

        if self.vX != 0:
            t = (Player.SPACE() + Player.WIDTH() - self.x) / self.vX
        else:
            t = -1
        points["wallLEFT"] = self.y + self.vY * t
        if t < 0 or points["wallLEFT"] < 0 or points["wallLEFT"] > self.windowSize[0] or self.vX > 0:
            points["wallLEFT"] = -1.0

        return points

    def move(self):
        self.x += self.vX
        self.y += self.vY

    def getWinner(self):
        wallNum = self.collideWall()
        if wallNum == 0:
            return -1

        return 0 if wallNum == 1 or wallNum == 2 else 1

    def collideWall(self) -> int:
        if self.x - self.size > self.windowSize[0]:
            return 1

        if self.y - self.size > self.windowSize[1]:
            return 2

        if self.x + self.size < 0:
            return 3

        if self.y + self.size < 0:
            return 4

        return 0

    def reflectVX(self):
        self.vX *= -1
        angle = math.atan2(self.vY, self.vX)
        self.vX += 0.1 * math.cos(angle)
        self.vY += 0.1 * math.sin(angle)

    def reflectVY(self):
        self.vY *= -1
        angle = math.atan2(self.vY, self.vX)
        self.vX += 0.1 * math.cos(angle)
        self.vY += 0.1 * math.sin(angle)
