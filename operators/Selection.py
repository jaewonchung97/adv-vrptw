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
        point = random.random()
        point *= population.total_fitness
        log.debug(f"[Roulette] point:{point}\tpop_total_fit:{population.total_fitness}")

        sum_val = 0
        for i in range(len(population.chromosomes)):
            chromosome = population.chromosomes[i]
            sum_val += chromosome.fitness
            log.debug(f"[Roulette] sum_val:{sum_val}\tpoint:{point}")
            if point < sum_val:
                return chromosome

    def select(self, population: Population) -> List[Chromosome]:
        return [self.sel_one(population), self.sel_one(population)]
