import random
from abc import abstractmethod, ABCMeta
from typing import List

from domain.Chromosome import Chromosome
from domain.Population import Population


class Selection(metaclass=ABCMeta):
    @abstractmethod
    def select(self, population: Population) -> List[Chromosome]:
        pass


class RouletteWheelSelection(Selection):
    @staticmethod
    def sel_one(population: Population) -> Chromosome:
        point = random.random()
        point *= population.total_fitness
        sum_val = 0
        for i in range(len(population.chromosomes)):
            chromosome = population.chromosomes[i]
            sum_val += chromosome.fitness
            if point < sum_val:
                return chromosome

    def select(self, population: Population) -> List[Chromosome]:
        return [self.sel_one(population), self.sel_one(population)]
