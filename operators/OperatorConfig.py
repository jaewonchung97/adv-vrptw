from operators.Selection import Selection, RouletteWheelSelection
from operators.Crossover import Crossover, IBXCrossover, PMXCrossover
from log.log_config import log


class OperatorConfig:
    selection = None
    crossover = None

    def __init__(self):
        if self.selection is None:
            self.selection = RouletteWheelSelection()
        if self.crossover is None:
            self.crossover = PMXCrossover()


if __name__ == '__main__':
    selection = OperatorConfig().selection
    crossover = OperatorConfig().crossover
    log.debug(f"Selection: {selection}")
    log.debug(f"Crossover: {crossover}")
