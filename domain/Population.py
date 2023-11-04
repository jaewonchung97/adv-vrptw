import numpy

from typing import List

from Config import POPULATION_SIZE, DATASET
from domain.Chromosome import Chromosome


def make_pop() -> List[Chromosome]:
    pop = []
    while len(pop) < POPULATION_SIZE:
        chromosome = Chromosome(numpy.random.permutation(range(1, len(DATASET.customers))).tolist())
        if chromosome.routes:
            pop.append(chromosome)
    return pop


class Population:
    def get_fitness(self, chromosome):
        max_dist = max(self.chromosomes, key=lambda x: x.vehicle_num).vehicle_num
        return chromosome.vehicle_num - max_dist + chromosome.total_distance / max_dist

    # Chromosome Fitness 동기화
    def sync_instances(self):
        for chromosome in self.chromosomes:
            fitness = self.get_fitness(chromosome)
            chromosome.fitness = fitness
            self.total_fitness += fitness

        self.chromosomes.sort(key=lambda x: x.fitness, reverse=True)

    def __init__(self, chromosomes: list = None):
        if not chromosomes:
            chromosomes = make_pop()
        self.chromosomes = chromosomes
        self.max_initial_dist = max(self.chromosomes, key=lambda x: x.total_distance)
        self.total_fitness = 0
        self.sync_instances()
