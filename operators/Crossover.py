from abc import abstractmethod, ABCMeta

from domain.Chromosome import Chromosome


class Crossover(metaclass=ABCMeta):
    @abstractmethod
    def crossover(self, c1: Chromosome, c2: Chromosome) -> Chromosome:
        pass
