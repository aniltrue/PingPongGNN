import pandas as pd
import numpy as np
from GAME.Game import Game
from GAME.Game import WINDOW_SIZE
from GAME.BasicAI import BasicAIPlayer
from AI.Species import Species
from AI.Genome import Genome, LAYER_SIZE, OUTPUT_SIZE
from AI.AIPlayer import AIPlayer
from AI.AIPlayer import AI_Model as model

class TestGame(Game):
    def __init__(self, species: Species):
        super().__init__(BasicAIPlayer(0, WINDOW_SIZE), AIPlayer(1, WINDOW_SIZE, species, store_history=False))
        self.species = species


    def play(self, fps = 60, showTargetPoint = True):
        super().play(fps, showTargetPoint)

    def calculateFitness(self):
        return self.species.calculateFitness(self.players[1], self.players[0], self.ball)

def readGenome(path: str = "C:\\Rates\\PingPong\\") -> Genome:
    gene = Genome()
    gene.model = model
    gene.model.load_weights("%smodel.h5"%(path))

    return gene

if __name__ == "__main__":
    game = TestGame(Species(readGenome()))
    game.play()
    print(game.calculateFitness())