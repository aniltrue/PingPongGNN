import numpy as np
import pygame
from GAME import Ball

def SPACE() -> float:
    return 10.0

def WIDTH() -> float:
    return 5.0

class Player:
    def __init__(self, playerID: int, windowSize: (int, int)):
        self.playerID = playerID
        self.windowSize = windowSize
        self.x = windowSize[1] / 2.0
        self.y = windowSize[0] / 2.0
        self.size = windowSize[0] / 10.0 if windowSize[0] < windowSize[1] else windowSize[1] / 10.0
        self.point = 0
        self.vX = 0.0
        self.vY = 0.0
        self.lastAction = [0 for i in range(9)]

    def VELOCITY(self) -> float:
        return self.size / 7

    def getAction(self, enemy, ball: Ball) -> np.ndarray:
        pass

    def play(self, enemy, ball: Ball):
        action = self.getAction(enemy, ball)
        act = np.argmax(action)

        if act == 0:
            self.vY = -self.VELOCITY()
            self.vX = -self.VELOCITY()
        elif act == 1:
            self.vY = -self.VELOCITY()
            self.vX = 0
        elif act == 2:
            self.vY = -self.VELOCITY()
            self.vX = self.VELOCITY()
        elif act == 3:
            self.vY = 0
            self.vX = -self.VELOCITY()
        elif act == 4:
            self.vY = 0
            self.vX = 0
        elif act == 5:
            self.vY = 0
            self.vX = self.VELOCITY()
        elif act == 6:
            self.vY = self.VELOCITY()
            self.vX = -self.VELOCITY()
        elif act == 7:
            self.vY = self.VELOCITY()
            self.vX = 0
        elif act == 8:
            self.vY = self.VELOCITY()
            self.vX = self.VELOCITY()

        self.lastAction = action[0]

    def move(self):
        self.x += self.vX

        if self.x < SPACE():
            self.x = SPACE()
            self.vX = 0.0

        if self.x + self.size > self.windowSize[1] - SPACE():
            self.x = self.windowSize[1] - SPACE() - self.size
            self.vX = 0.0

        self.y += self.vY

        if self.y < SPACE():
            self.y = SPACE()
            self.vY = 0.0

        if self.y + self.size > self.windowSize[0] - SPACE():
            self.y = self.windowSize[0] - SPACE() - self.size
            self.vY = 0.0

    def draw(self, screen: pygame.Surface):
        color = [120, 120, 120] if self.playerID == 0 else [130, 130, 130]

        x1 = self.x
        y1 = SPACE() if self.playerID == 0 else self.windowSize[0] - SPACE() - WIDTH()
        pygame.draw.rect(screen, color, pygame.Rect(x1, y1, self.size, WIDTH()))

        x2 = SPACE() if self.playerID == 0 else self.windowSize[1] - SPACE() - WIDTH()
        y2 = self.y
        pygame.draw.rect(screen, color, pygame.Rect(x2, y2, WIDTH(), self.size))

    def collide(self, ball: Ball) -> bool:
        collision = False

        if self.playerID == 0:
            if ball.y - ball.size < SPACE() + WIDTH() and ball.x > self.x - ball.size and ball.x < self.x + self.size - ball.size:
                ball.y = SPACE() + WIDTH() + ball.size
                ball.reflectVY()
                ball.vX += self.vX * 0.4
                self.point += 10
                collision = True

            if ball.x - ball.size < SPACE() + WIDTH() and ball.y > self.y - ball.size and ball.y < self.y + self.size - ball.size:
                ball.x = SPACE() + WIDTH() + ball.size
                ball.reflectVX()
                ball.vY += self.vY * 0.4
                self.point += 10
                collision = True

            return collision

        if ball.y + ball.size > self.windowSize[0] - SPACE() - WIDTH() and ball.x > self.x - ball.size and ball.x < self.x + self.size - ball.size:
            ball.y = self.windowSize[0] - SPACE() - WIDTH() - ball.size
            ball.reflectVY()
            ball.vX += self.vX * 0.4
            self.point += 10
            collision = True

        if ball.x + ball.size > self.windowSize[1] - SPACE() - WIDTH() and ball.y > self.y - ball.size and ball.y < self.y + self.size - ball.size:
            ball.x = self.windowSize[1] - SPACE() - WIDTH() - ball.size
            ball.reflectVX()
            ball.vY += self.vY * 0.4
            self.point += 10
            collision = True

        return collision

    def getDiferences(self, ball: Ball) -> (float, float):
        return self.x - ball.x, self.y - ball.y

    def old2New(self, action: list) -> list:
        return_action = [0 for i in range(9)]

        if action == [0, 0, 1, 1, 0, 0]:
            return_action[0] = 1
        elif action == [0, 1, 0, 1, 0, 0]:
            return_action[1] = 1
        elif action == [1, 0, 0, 1, 0, 0]:
            return_action[2] = 1
        elif action == [0, 0, 1, 0, 1, 0]:
            return_action[3] = 1
        elif action == [0, 1, 0, 0, 1, 0]:
            return_action[4] = 1
        elif action == [1, 0, 0, 0, 1, 0]:
            return_action[5] = 1
        elif action == [0, 0, 1, 0, 0, 1]:
            return_action[6] = 1
        elif action == [0, 1, 0, 0, 0, 1]:
            return_action[7] = 1
        elif action == [1, 0, 0, 0, 0, 1]:
            return_action[8] = 1

        return return_action