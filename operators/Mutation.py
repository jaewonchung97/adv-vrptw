import random

from abc import abstractmethod, ABCMeta

from domain.Chromosome import Chromosome


class Mutation(metaclass=ABCMeta):
    @abstractmethod
    def mutate(self, chromosome: Chromosome) -> Chromosome:
        pass


class TypicalMutation(Mutation):
    def mutate(self, chromosome: Chromosome) -> Chromosome:
        points = sorted(random.sample(range(0, len(chromosome.routes)), 2))
        permutation = Chromosome.routes_to_permutation(chromosome.routes)
        permutation[points[0]], permutation[points[1]] = permutation[points[1]], permutation[points[0]]
        return Chromosome(permutation)
