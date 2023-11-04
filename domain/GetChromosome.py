from typing import List

from domain.DatasetDTO import Dataset


def get_chrom(permutation: List[int], dataset: Dataset):
    chrom = []
    capacity = dataset.capacity
    due_time = dataset.depot.due_time

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
    if not cur_route:
        chrom.append(cur_route)
    return chrom
