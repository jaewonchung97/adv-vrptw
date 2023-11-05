import random

from abc import abstractmethod, ABCMeta
from typing import List

from domain.Chromosome import Chromosome


class Crossover(metaclass=ABCMeta):
    @abstractmethod
    def crossover(self, parents: List[Chromosome]) -> Chromosome:
        pass


class IBXCrossover(Crossover):
    @staticmethod
    def select_route(chromosome: Chromosome) -> int:
        point = random.random()
        total_waiting_time = 0
        for i in range(len(chromosome.waiting_time)):
            total_waiting_time += chromosome.waiting_time[i]
        point *= total_waiting_time
        sum_val = 0
        for i in range(len(chromosome.routes)):
            sum_val += chromosome.waiting_time[i]
            if point < sum_val:
                return i

    def crossover(self, parents: List[Chromosome]) -> Chromosome:
        # Select Randomly One of P1's Routes by waiting time
        route_idx = self.select_route(parents[0])
        pass
