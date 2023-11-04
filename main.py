from domain.Population import Population
from operators.Selection import Selection, RouletteWheelSelection


def main():
    population = Population()
    selection = RouletteWheelSelection()
    parents = selection.select(population)
    print(parents[0].routes)
    print(parents[1].routes)

