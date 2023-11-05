import numpy
import secrets

from typing import List

from config import POPULATION_SIZE, FILE_SAVE
from domain.Chromosome import Chromosome
from domain.Dataset import Dataset
from log.log_config import log
from utils.file_utils import save_file


class Population:
    def get_fitness(self, chromosome):
        max_dist = max(self.chromosomes, key=lambda x: x.vehicle_num).vehicle_num
        return chromosome.vehicle_num - max_dist + chromosome.total_distance / max_dist

    # Chromosome Fitness 동기화 및 정렬(오름차순)
    def sync_instances(self):
        for chromosome in self.chromosomes:
            fitness = self.get_fitness(chromosome)
            chromosome.fitness = fitness
            self.total_fitness += fitness

        self.chromosomes.sort(key=lambda x: x.fitness)

    def make_pop(self) -> List[Chromosome]:
        pop = []
        while len(pop) < POPULATION_SIZE:
            chromosome = Chromosome(numpy.random.permutation(range(1, len(self.dataset.customers))).tolist(),
                                    self.dataset)
            if chromosome.routes:
                log.debug(f"Chromosome Found {chromosome.routes}")
                if FILE_SAVE:
                    save_file(chromosome.routes, f"routes_{secrets.token_hex(8)}")
                pop.append(chromosome)
        return pop

    def __init__(self, dataset: Dataset, chromosomes: list = None):
        self.dataset = dataset
        if not chromosomes:
            chromosomes = self.make_pop()
        self.chromosomes = chromosomes
        self.max_initial_dist = max(self.chromosomes, key=lambda x: x.total_distance)
        self.total_fitness = 0
        self.sync_instances()
