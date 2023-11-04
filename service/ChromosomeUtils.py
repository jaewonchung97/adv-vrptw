from typing import List

from domain.DatasetDTO import Dataset


def get_chromosome(permutation: list, dataset: Dataset):
    chrom = []
    capacity = dataset.capacity
    due_time = dataset.customers[0].due_time

    cur_route = []
    prev_demand = 0
    prev_time = 0
    prev_customer_idx = 0
    for cur_customer_idx in permutation:
        cur_customer = dataset.customers[cur_customer_idx]
        cur_demand = prev_demand + cur_customer.demand
        cur_time = prev_time \
                   + dataset.distance[prev_customer_idx][cur_customer_idx] \
                   + cur_customer.service_time \
                   + dataset.distance[cur_customer_idx][0]
        if cur_demand <= capacity and cur_time <= due_time:
            cur_route.append(cur_customer_idx)
            prev_demand = cur_demand
            prev_time = cur_time - dataset.distance[cur_customer_idx][0]
        else:
            chrom.append(cur_route)
            cur_route = [cur_customer_idx]
            prev_demand = cur_customer.demand
            prev_time = dataset.distance[0][cur_customer_idx] \
                        + cur_customer.service_time
            prev_customer_idx = cur_customer_idx
    if cur_route:
        chrom.append(cur_route)
    return chrom


def get_fitness(chromosome: List[List[int]], dataset: Dataset):
    print(chromosome)
    fitness = 0
    for route in chromosome:
        distance = 0
        prev_cus_id = 0
        for cur_cus_id in route:
            distance += dataset.distance[prev_cus_id][cur_cus_id]
            prev_cus_id = cur_cus_id
        fitness += distance
    print(fitness)


