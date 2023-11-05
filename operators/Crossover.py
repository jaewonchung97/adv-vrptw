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
        log.debug(f"[cross] parents: {parents}")
        p1, p2 = parents[0], parents[1]
        p1_perm = []
        p2_perm = []
        for route in p1.routes:
            p1_perm.extend(route)
        for route in p2.routes:
            p2_perm.extend(route)

        new_perm = [0 for i in range(0, len(p1_perm))]

        points = sorted(random.sample(range(0, len(p1_perm)), 2))

        not_visited = [i for i in range(1, len(p1_perm) + 1)]

        new_perm[points[0]:points[1] + 1] = p1_perm[points[0]:points[1] + 1]
        for point in new_perm[points[0]: points[1] + 1]:
            not_visited.remove(point)

        log.debug(f"points: {points}\tp1_perm: {p1_perm}")
        log.debug(f"new_perm : {new_perm}")

        p2_idx = (points[1] + 1) % len(p2_perm)
        log.debug(f"p2_pem: {p2_perm}")
        log.debug(f"idx : {p2_perm.index(p1_perm[points[1]])}\tvalue: {p2_perm[p2_idx]}")
        new_perm_idx = (points[1] + 1) % len(new_perm)

        while not_visited:
            p2_idx = (p2_idx + 1) % len(p2_perm)
            if p2_perm[p2_idx] in not_visited:
                new_perm[new_perm_idx] = p2_perm[p2_idx]
                not_visited.remove(new_perm[new_perm_idx])
                new_perm_idx = (new_perm_idx + 1) % len(new_perm)
        log.debug(f"P1 Perm : {p1_perm}")
        log.debug(f"P2 Perm : {p2_perm}")
        log.debug(f"points : {points}")
        log.debug(f"new perm : {new_perm}")

        return Chromosome(new_perm)


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
