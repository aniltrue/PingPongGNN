from GAME.Game import Game
from GAME.Game import WINDOW_SIZE
from GAME.HumanPlayer import HumanPlayer

class HumanVSHumanGame(Game):
    def __init__(self):
        super().__init__(HumanPlayer(0, WINDOW_SIZE), HumanPlayer(1, WINDOW_SIZE))

    def play(self, fps = 60, showTargetPoint = False):
        super().play(fps, showTargetPoint)

if __name__ == "__main__":
    game = HumanVSHumanGame()
    game.play()