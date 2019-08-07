from GAME.Game import Game
from GAME.Game import WINDOW_SIZE
from GAME.BasicAI import BasicAIPlayer
from AI.Species import Species
from AI.Genome import Genome
from AI.AIPlayer import AIPlayer

class TraningGame(Game):
    def __init__(self, species: Species, bestSpecies: Species):
        super().__init__(AIPlayer(0, WINDOW_SIZE, bestSpecies), AIPlayer(1, WINDOW_SIZE, species, isTarget=True), render=False)
        self.species = species

    def play(self, fps = 360, showTargetPoint = True):
        super().play(fps, showTargetPoint)

    def calculateFitness(self):
        return self.species.calculateFitness(self.players[1], self.players[0], self.ball)
