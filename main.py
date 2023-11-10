from typing import List

from domain.Chromosome import Chromosome
from domain.Population import Population
from log.log_config import log
from operators.OperatorConfig import OperatorConfig
from config import RECOMBINATION_RATE, MIGRATION, MAX_GENERATIONS, POPULATION_SIZE
import random

from utils.graph_utils import draw_routes


def main():
    population_1 = Population()
    population_2 = Population()
    log.info(f"Before--------------------------------------")
    log.info(f"pop1_best : {population_1.chromosomes[0]}")
    log.info(f"pop2_best : {population_2.chromosomes[0]}")
    draw_routes(population_1.chromosomes[0])

    log.debug(f"GA--------------------------------------")
    for gen_i in range(MAX_GENERATIONS):
        do_ga(population_1)
        do_ga(population_2)
        migration(population_1, population_2)
        log.debug(f"[{gen_i}] pop1 len: {len(population_1.chromosomes)}")
        log.info(f"[{gen_i}] pop1 Best: {population_1.chromosomes[0]}")
        log.info(f"[{gen_i}] pop2 Best: {population_2.chromosomes[0]}")

    log.info(f"After--------------------------------------")
    log.info(f"pop1_best : {population_1.chromosomes[0]}")
    # log.info(f"pop2_best : {population_2.chromosomes[0]}")
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


def migration(pop1: Population, pop2: Population) -> None:
    pop1_best = pop1.chromosomes[0:MIGRATION]
    pop2_best = pop2.chromosomes[0:MIGRATION]
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
        log.debug(f"[Select] parents = {parents}")
        offspring = OperatorConfig.crossover.cross(parents)
        offspring = OperatorConfig.mutation.mutate(offspring)
        offsprings.append(offspring)
    replace(pop, offsprings)
