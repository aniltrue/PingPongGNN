import numpy as np
import keras
from keras.layers import Dense
from keras.models import Sequential
from numpy import matmul as mm

INPUT_SIZE = 31
OUTPUT_SIZE = 9
LAYER_SIZE = 64
INITIAL_RANGE = 1.0
MIN_FITNESS = -1000

class Genome:
    # RANDOM
    def __init__(self, weights: list = None):
        self.fitness = MIN_FITNESS
        self.cumulativeFitness = 0
        self.lifeTime = 0

        if weights != None:
            self.weights = weights
            self.model = None
            return

        W1 = np.random.rand(INPUT_SIZE, LAYER_SIZE) * 2.0 * INITIAL_RANGE - INITIAL_RANGE
        W2 = np.random.rand(LAYER_SIZE, LAYER_SIZE) * 2.0 * INITIAL_RANGE - INITIAL_RANGE
        W3 = np.random.rand(LAYER_SIZE, LAYER_SIZE) * 2.0 * INITIAL_RANGE - INITIAL_RANGE
        W4 = np.random.rand(LAYER_SIZE, OUTPUT_SIZE) * 2.0 *INITIAL_RANGE - INITIAL_RANGE

        B1 = np.random.rand(LAYER_SIZE, ) * 2.0 * INITIAL_RANGE - INITIAL_RANGE
        B2 = np.random.rand(LAYER_SIZE, ) * 2.0 * INITIAL_RANGE - INITIAL_RANGE
        B3 = np.random.rand(LAYER_SIZE, ) * 2.0 * INITIAL_RANGE - INITIAL_RANGE
        B4 = np.random.rand(OUTPUT_SIZE, ) * 2.0 * INITIAL_RANGE - INITIAL_RANGE

        self.weights = [ [W1, B1], [W2, B2], [W3, B3], [W4, B4]]
        self.model = None

    def updateModel(self):
        i = 0
        for layer in self.model.layers:
            if isinstance(layer, Dense):
                layer.set_weights(self.weights[i])
                i += 1

    def getOutput(self, input: np.ndarray):
        return self.model.predict(input)

    def setFitness(self, fitnes: int):
        self.cumulativeFitness += fitnes
        self.lifeTime += 1

        if self.cumulativeFitness != 0:
            self.fitness = self.cumulativeFitness / self.lifeTime
        else:
            self.fitness = 0

    def __lt__(self, other) -> bool:
        if not isinstance(other, Genome):
            return False

        return self.fitness < other.fitness

    def __le__(self, other) -> bool:
        if not isinstance(other, Genome):
            return False

        return self.fitness <= other.fitness

    def __gt__(self, other) -> bool:
        if not isinstance(other, Genome):
            return False

        return self.fitness > other.fitness

    def __ge__(self, other) -> bool:
        if not isinstance(other, Genome):
            return False

        return self.fitness >= other.fitness