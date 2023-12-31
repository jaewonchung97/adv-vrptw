import copy
import random
from typing import List

from config import RECOMBINATION_RATE, MIGRATION, MAX_GENERATIONS, POPULATION_SIZE, FILE_SAVE
from domain.Chromosome import Chromosome
from domain.Population import Population
from log.log_config import log
from operators.OperatorConfig import OperatorConfig

from utils.graph_utils import draw_routes
from utils.file_utils import save_file


def main():
    population_1 = Population()
    population_2 = Population()
    log.info(f"Before--------------------------------------")
    log.info(f"pop1_best : {population_1.chromosomes[0]}")
    log.info(f"pop1_worst : {population_1.chromosomes[POPULATION_SIZE - 1]}")
    log.info(f"pop1_std : {population_1.std}")
    log.debug(f"pop2_best : {population_2.chromosomes[0]}")
    log.debug(f"pop1_worst : {population_2.chromosomes[POPULATION_SIZE - 1]}")
    draw_routes(population_1.chromosomes[0])

    log.debug(f"GA--------------------------------------")
    for gen_i in range(MAX_GENERATIONS):
        do_ga(population_1)
        do_ga(population_2)
        migration(population_1, population_2)
        log.debug(f"[{gen_i}] pop1 len: {len(population_1.chromosomes)}")
        log.debug(f"[{gen_i}] pop1 Best: {population_1.chromosomes[0]}")
        log.debug(f"[{gen_i}] pop1_worst : {population_1.chromosomes[POPULATION_SIZE - 1]}")
        log.debug(f"[{gen_i}] pop2 Best: {population_2.chromosomes[0]}")
        log.debug(f"[{gen_i}] pop1_worst : {population_2.chromosomes[POPULATION_SIZE - 1]}")

    log.info(f"After--------------------------------------")
    log.info(f"pop1_best : {population_1.chromosomes[0]}")
    log.info(f"pop1_worst : {population_1.chromosomes[POPULATION_SIZE - 1]}")
    log.info(f"pop1_std : {population_1.std}")
    log.debug(f"pop2_best : {population_2.chromosomes[0]}")
    log.debug(f"pop1_worst : {population_2.chromosomes[POPULATION_SIZE - 1]}")
    if population_1.chromosomes[0].fitness < population_2.chromosomes[0].fitness:
        draw_routes(population_1.chromosomes[0])
    else:
        draw_routes(population_2.chromosomes[0])

    log.debug(f"pop1--------------------------------------")
    for idx, chromosome in enumerate(population_1.chromosomes):
        log.debug(f"[{idx}]\t{chromosome}")

    log.debug(f"pop2--------------------------------------")
    for idx, chromosome in enumerate(population_2.chromosomes):
        log.debug(f"[{idx}]\t{chromosome}")

    if FILE_SAVE:
        chrom = population_1.chromosomes[0]
        save_file(chrom.routes,
                  file_name=f"route_{chrom.vehicle_num}_{round(chrom.total_distance, 1)}")
        chrom = population_2.chromosomes[0]
        save_file(chrom.routes,
                  file_name=f"route_{chrom.vehicle_num}_{round(chrom.total_distance, 1)}")


def migration(pop1: Population, pop2: Population) -> None:
    pop1_best = copy.deepcopy(pop1.chromosomes[0:MIGRATION])
    pop2_best = copy.deepcopy(pop2.chromosomes[0:MIGRATION])
    pop1.chromosomes[0:MIGRATION] = pop2_best
    pop2.chromosomes[0:MIGRATION] = pop1_best
    pop1.sync_instances()
    pop2.sync_instances()


def replace(pop: Population, offsprings: List[Chromosome]):
    pop.chromosomes[-len(offsprings):] = offsprings
    pop.sync_instances()


def do_ga(pop):
    offsprings = []
    while len(offsprings) != POPULATION_SIZE * RECOMBINATION_RATE / 100:
        r = random.random()
        if r > RECOMBINATION_RATE / 100:
            continue
        parents = OperatorConfig.selection.select(pop)
        log.debug(f"[Select] parents1 = {pop.chromosomes.index(parents[0])}")
        log.debug(f"[Select] parents2 = {pop.chromosomes.index(parents[1])}")
        offspring = OperatorConfig.crossover.cross(parents)
        offspring = OperatorConfig.mutation.mutate(offspring)
        offsprings.append(offspring)
    replace(pop, offsprings)
