import random

from abc import abstractmethod, ABCMeta
from typing import List

from domain.Chromosome import Chromosome
from log.log_config import log
from domain.Dataset import Dataset, Customer


class Crossover(metaclass=ABCMeta):
    @abstractmethod
    def cross(self, parents: List[Chromosome]) -> Chromosome:
        pass


class PMXCrossover(Crossover):
    def cross(self, parents: List[Chromosome]) -> Chromosome:
        p1, p2 = parents[0], parents[1]
        p1_perm = [customer for route in p1.routes for customer in route]
        p2_perm = [customer for route in p2.routes for customer in route]

        # 겹치지 않는 루트를 찾을 때까지 반복
        while True:
            # PMX 교차 수행
            points = sorted(random.sample(range(0, len(p1_perm)), 2))
            result = [0 for _ in range(len(p1_perm))]
            result[points[0]: points[1] + 1] = p1_perm[points[0]: points[1] + 1]

            for i, value in enumerate(result):
                if value == 0:
                    while (p2_value := p2_perm.pop(0)) in result:
                        pass
                    result[i] = p2_value

            # 루트가 겹치지 않는지 확인
            child_chromosome = Chromosome(result)
            if not self.routes_overlap(child_chromosome):
                return child_chromosome

    @staticmethod
    def routes_overlap(chromosome: Chromosome) -> bool:
        seen_customers = set()
        for route in chromosome.routes:
            for customer in route:
                if customer in seen_customers:
                    return True
                seen_customers.add(customer)
        return False


class IBXCrossover(Crossover):
    @staticmethod
    def select_route(chromosome: Chromosome) -> int:
        # Select Randomly One of P1's Routes by waiting time
        point = random.random()
        total_waiting_time = sum(chromosome.waiting_time)
        point *= total_waiting_time
        sum_val = 0
        for i in range(len(chromosome.routes)):
            sum_val += chromosome.waiting_time[i]
            if point < sum_val:
                return i

    @staticmethod
    def construct_child_route(parent1: Chromosome, parent2: Chromosome, route_idx: int, centroid: int) -> List[
        int]:
        # Solomon의 영감을 받은 수정된 삽입 휴리스틱의 구현
        child_route = [centroid]  # 중심으로 시작

        # Set to track visited customers for all vehicles
        visited_customers = set([centroid])

        for i in range(1, len(parent1.routes[route_idx])):
            # 만약 해당 고객이 아직 방문되지 않았다면 해당 고객을 자식 경로에 추가
            customer = parent1.routes[route_idx][i]
            if customer not in visited_customers:
                child_route.append(customer)
                visited_customers.add(customer)

        # 이미 자식 경로에 없는 경우 parent2에서 고객을 추가
        for i in range(len(parent2.routes[route_idx])):
            customer = parent2.routes[route_idx][i]
            if customer not in visited_customers:
                child_route.append(customer)
                visited_customers.add(customer)

        return child_route

    def cross(self, parents: List[Chromosome]) -> Chromosome:
        p1, p2 = parents[0], parents[1]
        r1_idx = self.select_route(p1)
        r1 = p1.routes[r1_idx]
        centroid = r1[len(r1) // 2]
        log.debug(f"Centroid : {centroid}\tfrom {r1}")

        # Use the construct_child_route method
        child_route = self.construct_child_route(p1, p2, r1_idx, centroid)

        # Create a new Chromosome with the child route
        child_chromosome = Chromosome(child_route)

        return child_chromosome
