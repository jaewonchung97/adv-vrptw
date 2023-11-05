from domain.Population import Population
from log.log_config import log
from operators.OperatorConfig import OperatorConfig


def 


def main():
    population_1 = Population()
    population_2 = Population()

    parents = OperatorConfig.selection.select(population_1)
    log.info(f"p1 = {parents[0].routes}\tp2 = {parents[1].routes}")
    new_chrom = OperatorConfig.crossover.cross(parents)
    log.info(f"Crossed = {new_chrom.routes}")
    mutated = OperatorConfig.mutation.mutate(new_chrom)
    log.info(f"Mutated = {mutated.routes}")
