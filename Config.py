"""
- Population size: 50 (2 populations)
- Maximum number of generations: 100
- Migration: 5
- Population replacement scheme: elitism
- Recombination rate: 60%
    IB_X:
        customer removal procedure (from route r1 of parent solution P1):
        random: 25% distance-based: 25% largest waiting time: 50%
    customer insertion acceptance procedure:
        scheduling period T: 20 generations
    insertion probability (over T generations): min {1/2 + i/T, 1}, i=1..T
- Mutation rate: 60%
    if best fitness improves from one generation to the next then
        IB_M
    else apply with a 50% probability an alternate mutation operator:
        NNR_M: 70%
        DCR_M: 30%
"""

POPULATION_SIZE = 50
MAX_GENERATIONS = 100
MIGRATION = 5
RECOMBINATION_RATE = 60
MUTATION_RATE = 60
INSTANCE_NAME = "r101"
CUSTOMER_SIZE = 100

FILE_SAVE = False
