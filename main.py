from service.ChromosomeUtils import get_chromosome, get_fitness
from utils.LoadDataset import load_dataset
import numpy

def main():
    dataset = load_dataset("r101", 10)
    dataset.capacity = 30
    get_fitness(get_chromosome(numpy.random.permutation(range(1, 11)).tolist(), dataset), dataset)
    get_fitness(get_chromosome(numpy.random.permutation(range(1, 11)).tolist(), dataset), dataset)
    get_fitness(get_chromosome(numpy.random.permutation(range(1, 11)).tolist(), dataset), dataset)
