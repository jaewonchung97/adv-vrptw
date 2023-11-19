import random

from domain.Chromosome import Chromosome
from abc import abstractmethod, ABCMeta
from domain.Chromosome import Chromosome


class Node:
    def __init__(self, solution, lower_bound):
        self.solution = solution
        self.lower_bound = lower_bound


class Mutation(metaclass=ABCMeta):
    @abstractmethod
    def mutate(self, chromosome: Chromosome) -> Chromosome:
        pass


class TypicalMutation(Mutation):
    def mutate(self, chromosome: Chromosome) -> Chromosome:
        points = sorted(random.sample(range(0, len(chromosome.routes)), 2))
        permutation = Chromosome.routes_to_permutation(chromosome.routes)
        permutation[points[0]], permutation[points[1]
                                            ] = permutation[points[1]], permutation[points[0]]
        return Chromosome(permutation)


class LNSBMutation(Mutation):
    def __init__(self, d=3, D=15):
        self.d = d  # Discrepancy factor
        self.D = D  # Parameter controlling determinism

    def mutate(self, chromosome: Chromosome, distance_matrix, time_matrix) -> Chromosome:
        # 주어진 Chromosome을 복사
        permutation = chromosome.routes_to_permutation(chromosome.routes)

        # 무작위로 고객 선택
        L = len(permutation)
        rand = random.uniform(0, 1)

        # 매개변수 D에 따라 선택을 조정
        if self.D == 1:
            selected_customer = random.randint(0, L - 1)
        else:
            selected_customer = int(L * rand)

        # LNSB-M(d) 전략을 사용하여 다양한 삽입 위치에 대한 분기 및 바운드 검색 수행
        tree_expansion_factor = random.choice([1, 2, 3])

        queue = [Node(permutation, boundary(
            permutation, distance_matrix, time_matrix))]
        best_solution = permutation
        best_value = float('inf')

        while queue:
            # FIFO 큐 사용하여 너비 우선 탐색
            current_node = queue.pop(0)

            if current_node.lower_bound < best_value:
                if len(current_node.solution) == len(permutation):
                    current_value = objective_function(
                        current_node.solution, distance_matrix, time_matrix)
                    if current_value < best_value:
                        best_value = current_value
                        best_solution = current_node.solution

                else:
                    # 분기 및 자식 노드 생성
                    children = branch(
                        current_node, distance_matrix, time_matrix)
                    queue.extend(children)

        # 찾은 최적해 반환
        return Chromosome(best_solution)


def boundary(solution, distance_matrix, time_matrix):
    # 경계 함수 계산 함수
    total_distance = calculate_total_distance(solution, distance_matrix)
    total_time = calculate_total_time(solution, time_matrix)
    cost = total_distance + total_time
    opportunities = len(solution)
    rank = cost + opportunities
    return rank


# def calculate_total_distance(solution, distance_matrix):
#     # 총 이동 거리 계산 함수
#     total_distance = 0
#     for i in range(len(solution) - 1):
#         from_customer = solution[i]
#         to_customer = solution[i + 1]
#         total_distance += distance_matrix[from_customer][to_customer]
#     return total_distance
# 예외처리
def calculate_total_distance(solution, distance_matrix):
    # 총 이동 거리 계산 함수
    if solution is None:
        # 예외 처리: solution이 None인 경우 0 반환 또는 다른 처리 수행
        return 0

    total_distance = 0
    for i in range(len(solution) - 1):
        from_customer = solution[i]
        to_customer = solution[i + 1]

        if from_customer is not None and to_customer is not None:
            total_distance += distance_matrix[from_customer][to_customer]
        else:
            # 예외 처리: from_customer 또는 to_customer가 None인 경우 0 반환 또는 다른 처리 수행
            return 0

    return total_distance


# def calculate_total_time(solution, time_matrix):
#     # 총 이동 시간 계산 함수
#     total_time = 0
#     for i in range(len(solution) - 1):
#         from_customer = solution[i]
#         to_customer = solution[i + 1]
#         total_time += time_matrix[from_customer][to_customer]
#     return total_time
# 예외처리
def calculate_total_time(solution, time_matrix):
    # 총 이동 시간 계산 함수
    if solution is None:
        # 예외 처리: solution이 None인 경우 0 반환 또는 다른 처리 수행
        return 0

    total_time = 0
    for i in range(len(solution) - 1):
        from_customer = solution[i]
        to_customer = solution[i + 1]

        if from_customer is not None and to_customer is not None:
            total_time += time_matrix[from_customer][to_customer]
        else:
            # 예외 처리: from_customer 또는 to_customer가 None인 경우 0 반환 또는 다른 처리 수행
            return 0

    return total_time


def branch(node, distance_matrix, time_matrix):
    # 노드 분기 규칙 구현
    children = []
    for i in range(len(node.solution)):
        for j in range(i + 1, len(node.solution)):
            child_solution = node.solution.copy()
            child_solution[i], child_solution[j] = child_solution[j], child_solution[i]
            child_lower_bound = boundary(
                child_solution, distance_matrix, time_matrix)
            child_node = Node(child_solution, child_lower_bound)
            children.append(child_node)
    return children


def objective_function(solution, distance_matrix, time_matrix):
    total_distance = calculate_total_distance(solution, distance_matrix)
    total_time = calculate_total_time(solution, time_matrix)

    # 해당 문제에 따라 적절한 방식으로 가중치를 조절하고 합산하여 최종 목적 함수 값을 계산합니다.
    # 아래는 간단한 형태로 총 이동 거리와 총 이동 시간을 더한 값을 반환하는 예시입니다.
    # 문제에 따라 가중치 또는 다른 요소를 추가하여 수정이 필요합니다.
    weighted_distance = 0.7  # 총 이동 거리의 가중치
    weighted_time = 0.3  # 총 이동 시간의 가중치

    objective_value = weighted_distance * total_distance + weighted_time * total_time
    return objective_value
