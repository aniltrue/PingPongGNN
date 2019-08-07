import pygame
import OpenGL
from GAME.Player import Player
from GAME.Ball import Ball

WINDOW_SIZE = (800, 800)
clock = pygame.time.Clock()

class Game:
    def __init__(self, player1: Player, player2: Player, render: bool = True):
        self.render = render

        if render:
            self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.players = [ player1, player2 ]
        self.ball = Ball(WINDOW_SIZE)
        self.isPlaying = True

    def play(self, fps: int, showTargetPoint: bool):
        while self.isPlaying:
            if self.render:
                for event in pygame.event.get():
                    if event == pygame.QUIT:
                        self.isPlaying = False

            self.gameLoop(showTargetPoint)
            if self.render:
                clock.tick(fps)

    def gameLoop(self, showTargetPoint: bool):
        if self.render:
            self.screen.fill((255, 255, 255))
            for player in self.players:
                player.draw(self.screen)

            self.ball.draw(self.screen, showTargetPoint=showTargetPoint)

        self.ball.move()
        for (i, player) in enumerate(self.players):
            enemyID = (i + 1) % 2
            player.play(self.players[enemyID], self.ball)
            player.move()
            player.collide(self.ball)

        if self.ball.collideWall() > 0:
            self.isPlaying = False

        if self.render:
            pygame.display.flip()
