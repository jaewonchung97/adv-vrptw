from domain.Population import Population
from utils.load_dataset import load_dataset
from log.log_config import log


def main():
    population = Population(load_dataset())
    log.debug(f"[End] Population Route----------------------------")
    for i in range(len(population.chromosomes)):
        log.debug(f"[{i}] Population Route: {population.chromosomes[i].routes}")
    log.debug(
        f"[Best] fitness: {population.chromosomes[0].fitness}\troutes : {population.chromosomes[0].routes_num}\twaiting: {population.chromosomes[0].waiting_time}")
    log.debug(
        f"[Worst] fitness: {population.chromosomes[49].fitness}\troutes : {population.chromosomes[49].routes_num}\twaiting: {population.chromosomes[49].waiting_time}")
