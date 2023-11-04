from abc import abstractmethod, ABCMeta

from domain.Chromosome import Chromosome


class Mutation(metaclass=ABCMeta):
    @abstractmethod
    def mutation(self, chromosome: Chromosome) -> Chromosome:
        pass
