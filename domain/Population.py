import secrets
from typing import List

import numpy

from config import POPULATION_SIZE, FILE_SAVE
from domain.Chromosome import Chromosome
from domain.Dataset import Dataset
from log.log_config import log
from utils.file_utils import save_file


class Population:
    def __init__(self, chromosomes: List[Chromosome] = None):
        if not chromosomes:
            chromosomes = Population.make_pop()
        self.chromosomes = chromosomes
        self.max_initial_dist = max(self.chromosomes, key=lambda x: x.total_distance).total_distance
        log.debug(f"max_initial: {self.max_initial_dist}")
        self.total_fitness = 0
        self.std = 0
        self.sync_instances()

    def get_fitness(self, chromosome):
        return chromosome.vehicle_num - min(self.chromosomes, key=lambda
            x: x.vehicle_num).vehicle_num + (chromosome.total_distance / self.max_initial_dist)

    # Chromosome Fitness 동기화 및 정렬(오름차순)q
    def sync_instances(self):
        self.total_fitness = 0
        fitness_list = []
        for chromosome in self.chromosomes:
            fitness = self.get_fitness(chromosome)
            chromosome.fitness = fitness
            self.total_fitness += (1 / fitness)
            fitness_list.append(fitness)

        self.chromosomes.sort(key=lambda x: x.fitness)

        self.std = numpy.std(fitness_list)

    @staticmethod
    def make_pop() -> List[Chromosome]:
        pop = []
        while len(pop) < POPULATION_SIZE:
            chromosome = Chromosome(numpy.random.permutation(range(1, len(Dataset.customers))).tolist())
            if chromosome.routes:
                log.debug(f"Chromosome Found {chromosome.routes}")
                # if FILE_SAVE:
                #     save_file(chromosome.routes, f"routes_{secrets.token_hex(8)}")
                pop.append(chromosome)
        return pop
