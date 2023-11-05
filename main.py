from domain.Population import Population
from utils.load_dataset import load_dataset
from log.log_config import log
from operators.OperatorConfig import OperatorConfig


def main():
    population = Population(load_dataset())
    selection = OperatorConfig().selection
    crossover = OperatorConfig().crossover

    parents = selection.select(population)
    crossover.crossover(parents)
