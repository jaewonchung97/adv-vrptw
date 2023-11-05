import secrets
from typing import List

import numpy

from config import POPULATION_SIZE, FILE_SAVE
from domain.Chromosome import Chromosome
from log.log_config import log
from utils.file_utils import save_file
from utils.load_dataset import load_dataset


class Population:
    dataset = None

    def __init__(self, chromosomes: List[Chromosome] = None):
        if Chromosome.dataset is None:
            Chromosome.dataset = load_dataset()
        if not chromosomes:
            chromosomes = Population.make_pop()
        self.chromosomes = chromosomes
        self.max_initial_dist = max(self.chromosomes, key=lambda x: x.total_distance)
        self.total_fitness = 0
        self.sync_instances()

    def get_fitness(self, chromosome):
        max_dist = max(self.chromosomes, key=lambda x: x.vehicle_num).vehicle_num
        return chromosome.vehicle_num - max_dist + chromosome.total_distance / max_dist

    # Chromosome Fitness 동기화 및 정렬(오름차순)
    def sync_instances(self):
        self.total_fitness = 0
        for chromosome in self.chromosomes:
            fitness = self.get_fitness(chromosome)
            chromosome.fitness = fitness
            self.total_fitness += fitness

        self.chromosomes.sort(key=lambda x: x.fitness)

    @staticmethod
    def make_pop() -> List[Chromosome]:
        pop = []
        while len(pop) < POPULATION_SIZE:
            chromosome = Chromosome(numpy.random.permutation(range(1, len(Chromosome.dataset.customers))).tolist(),
                                    Chromosome.dataset)
            if chromosome.routes:
                log.debug(f"Chromosome Found {chromosome.routes}")
                if FILE_SAVE:
                    save_file(chromosome.routes, f"routes_{secrets.token_hex(8)}")
                pop.append(chromosome)
        return pop
