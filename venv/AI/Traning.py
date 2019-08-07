import pandas as pd
from AI.Population import Population
from GAME.TraningGame import TraningGame
from AI.Genome import MIN_FITNESS
from AI.Genome import Genome
from AI.AIPlayer import AI_Model as model
import random as rnd

class Traning:
    def __init__(self):
        self.population = Population()

    def train(self, maxIter = 1000):
        print("Starts...")
        iter = 0
        bestSpecies = rnd.choice(self.population.species)
        counter = 0

        while iter < maxIter:
            histories = []
            for (i, species) in enumerate(self.population.species):
                game = TraningGame(species, bestSpecies)
                game.play()
                fitness = game.calculateFitness()
                histories.append(game.players[1].history)

                if fitness > 100:
                    print("%d. species - Fitness: %d" % (i, fitness))

                if i == 0 and fitness > 100:
                    counter += 1
                elif i == 0 and fitness <= 100:
                    counter = 0

            self.population.tournamentSelection()

            if iter > 0:
                self.population.backPropagation(histories)

            if iter % 2 == 0:
                bestSpecies = self.population.getFittest()

            if iter % 10 == 0 and iter > 0:
                print("Saving...")
                self.save()
                print("Saved.")


            if self.isConverged(counter) and iter > 250:
                print("Converged!!! at %d"%(iter))
                print("--------------------------------------------------")
                print("%d. Iteration completed. Best Fitness: %d" % (iter, self.population.getFittest().gene.fitness))
                print("--------------------------------------------------")
                break

            print("--------------------------------------------------")
            print("%d. Iteration completed. Best Fitness: %d"%(iter, self.population.getFittest().gene.fitness))
            print("--------------------------------------------------")

            iter += 1

        print("Completed.")
        print("Saving...")
        self.save()
        print("Saved.")

    def save(self, path: str = "C:\\Rates\\PingPong\\"):
        self.population.getFittest().gene.model = model
        self.population.getFittest().gene.updateModel()

        self.population.getFittest().gene.model.save("%smodel.h5"%(path))

    def isConverged(self, counter: int) -> bool:
        bestGenome = self.population.getFittest().gene
        if counter > 4:
            return True

        if bestGenome.fitness > 200 and bestGenome.lifeTime > 3:
            return True

        if bestGenome.fitness > 300:
            return True

        return False

if __name__ == "__main__":
    traning = Traning()
    traning.train()