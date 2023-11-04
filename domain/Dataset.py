from Customer import Customer
from typing import List


def get_dist(cus_1: Customer, cus_2: Customer):
    return ((cus_1.x - cus_2.x) ** 2 + (cus_1.y - cus_2.y) ** 2) ** 0.5


def get_metrix(customers: List[Customer]) -> List[List[float]]:
    result = [[0] * len(customers)] * len(customers)
    for i in range(len(customers)):
        for j in range(len(customers)):
            result[i][j] = get_dist(customers[i], customers[j])
    return result


class Dataset:
    def __init__(self, num_vehicles, capacity, customers: List[Customer]):
        self.num_vehicles = num_vehicles
        self.capacity = capacity
        self.depot = customers[0]
        self.customers = customers[1:]
        self.distance = get_metrix(customers)
