import random

from abc import abstractmethod, ABCMeta
from typing import List

from domain.Chromosome import Chromosome
from log.log_config import log


class Crossover(metaclass=ABCMeta):
    @abstractmethod
    def cross(self, parents: List[Chromosome]) -> Chromosome:
        pass


class PMXCrossover(Crossover):
    def cross(self, parents: List[Chromosome]) -> Chromosome:
        p1, p2 = parents[0], parents[1]
        p1_perm = []
        p2_perm = []
        for route in p1.routes:
            p1_perm.extend(route)
        for route in p2.routes:
            p2_perm.extend(route)

        points = sorted(random.sample(range(0, len(p1_perm)), 2))

        result = [0 for i in range(len(p1_perm))]
        result[points[0]: points[1] + 1] = p1_perm[points[0]: points[1] + 1]
        for i in result:
            if i == 0:
                continue
            p2_perm.remove(i)

        for value in p2_perm:
            result[result.index(0)] = value

        return Chromosome(result)


class IBXCrossover(Crossover):
    @staticmethod
    def select_route(chromosome: Chromosome) -> int:
        # Select Randomly One of P1's Routes by waiting time
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

    def cross(self, parents: List[Chromosome]) -> Chromosome:
        p1, p2 = parents[0], parents[1]
        r1_idx = self.select_route(p1)
        r1 = p1.routes[r1_idx]
        centroid = r1[len(r1) // 2]
        log.debug(f"Centroid : {centroid}\tfrom {r1}")
        pass


"""
    8   7   1   (3  6   10)   4   9   5   2
    10  2   4   (5   1   3)   6   7   8   9

1:  10   2   4   5  1   3   6   7   8   9
2:  3   2   4   10  6   5   1   7   8   9
3:  5   2   4   10  6   3   1   7   8   9

"""
