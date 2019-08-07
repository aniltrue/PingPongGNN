from GAME.Player import Player
from GAME.Ball import Ball
import pygame
import numpy as np

class HumanPlayer(Player):
    def getAction(self, enemy: Player, ball: Ball) -> np.ndarray:
        pressed = pygame.key.get_pressed()

        if self.playerID == 1:
            return self.getActionFromKeys(pressed[pygame.K_UP], pressed[pygame.K_DOWN], pressed[pygame.K_LEFT], pressed[pygame.K_RIGHT])
        else:
            return self.getActionFromKeys(pressed[pygame.K_w], pressed[pygame.K_s], pressed[pygame.K_a], pressed[pygame.K_d])

    def getActionFromKeys(self, up: bool, down: bool, left: bool, right: bool) -> np.ndarray:
        action = []
        if right and not left:
            action.extend([1, 0, 0])
        elif left and not right:
            action.extend([0, 0, 1])
        else:
            action.extend([0, 1, 0])

        if up and not down:
            action.extend([1, 0, 0])
        elif down and not up:
            action.extend([0, 0, 1])
        else:
            action.extend([0, 1, 0])

        return [self.old2New(action)]