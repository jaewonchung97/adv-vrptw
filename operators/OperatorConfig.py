from operators.Mutation import TypicalMutation, LNSBMutation
from operators.Selection import Selection, RouletteWheelSelection
from operators.Crossover import Crossover, IBXCrossover, PMXCrossover
from log.log_config import log


class OperatorConfig:
    selection = None
    crossover = None
    mutation = None

    def __init__(self):
        if OperatorConfig.selection is None:
            OperatorConfig.selection = RouletteWheelSelection()
        if OperatorConfig.crossover is None:
            OperatorConfig.crossover = PMXCrossover()
        if OperatorConfig.mutation is None:
            OperatorConfig.mutation = LNSBMutation()
