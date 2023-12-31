import random
from abc import abstractmethod, ABCMeta
from typing import List

from domain.Chromosome import Chromosome
from domain.Population import Population
from log.log_config import log


class Selection(metaclass=ABCMeta):
    @abstractmethod
    def select(self, population: Population) -> List[Chromosome]:
        pass


class RouletteWheelSelection(Selection):
    @staticmethod
    def sel_one(population: Population) -> Chromosome:
        log.debug(f"[Roulette] pop:{population}")
        log.debug(f"[Roulette] best_fit:{population.chromosomes[0].fitness}")
        log.debug(f"[Roulette] worst_fit:{population.chromosomes[len(population.chromosomes) - 1].fitness}")
        point = random.random()
        point *= population.total_fitness
        log.debug(f"[Roulette] point:{point}\tpop_total_fit:{population.total_fitness}")

        sum_val = 0
        for i in range(len(population.chromosomes)):
            chromosome = population.chromosomes[i]
            sum_val += (1 / chromosome.fitness)
            if point < sum_val:
                return chromosome

    def select(self, population: Population) -> List[Chromosome]:
        return [self.sel_one(population), self.sel_one(population)]
