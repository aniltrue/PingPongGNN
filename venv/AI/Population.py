import random as rnd
import numpy as np
import keras
from keras.optimizers import Nadam
from keras.layers import Dense
from AI.AIPlayer import AI_Model
from AI.Species import Species
from AI.PopulationSorter import sort


POPULATION_SIZE = 32 # POPULATION_SIZE % 4 == 0
ELITISM = 0.25

class Population:
    # Initial Random Population
    def __init__(self):
        self.species = []
        for i in range(POPULATION_SIZE):
            self.species.append(Species())

    def tournamentSelection(self):
        sort(self.species)

        elitismSize = int(POPULATION_SIZE * ELITISM)

        # Survive Elites
        nextGeneration = self.species[:elitismSize]

        # The best Crossing-Over
        nextGeneration.append(self.species[0].crossingOver(self.species[1]))

        # Elitist Random Crossing-Over
        notElits = self.species[elitismSize:]
        while len(nextGeneration) < POPULATION_SIZE:
            parent1 = rnd.choice(notElits)
            parent2 = rnd.choice(notElits)

            nextGeneration.append(parent1.crossingOver(parent2))

        sort(nextGeneration)

        self.species = nextGeneration

    def getFittest(self) -> Species:
        return self.species[0]

    def backPropagation(self, histories: list):
        print("Back Propagation starts...")
        bestHistories = []

        for i in range(3):
            inputs = []
            actions = []
            history = histories[i]

            for i in range(25):
                index = rnd.randrange(0, len(history))
                hist = history[index]
                inputs.append(hist[0])
                actions.append(hist[1][0])

            inputs = np.asarray(inputs)
            actions = np.asarray(actions)

            bestHistories.append([inputs, actions])

        for (i, species) in enumerate(self.species):
            if i == 0:
                continue

            species.gene.model = AI_Model
            species.gene.updateModel()

            if i > 2:
                self._backPropagation(bestHistories[2], species, epochs=1)
            if i > 1:
                self._backPropagation(bestHistories[1], species, epochs=2)

            self._backPropagation(bestHistories[0], species, epochs=3)

            weights = []
            for layer in species.gene.model.layers:
                if isinstance(layer, Dense):
                    weights.append(layer.get_weights())

            species.gene.weights = weights

        print("Back Propagation completed.")

    def _backPropagation(self, history: list, species: Species, epochs: int):
        inputs = history[0]
        actions = history[1]
        species.gene.model.fit(inputs, actions, epochs=epochs, verbose=0)