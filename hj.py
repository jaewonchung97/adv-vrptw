import random

# 고객 데이터셋
customers = [
    (0, 40.00, 50.00, 0.00, 0.00, 240.00, 0.00),
    (1, 25.00, 85.00, 20.00, 145.00, 175.00, 10.00),
    (2, 22.00, 75.00, 30.00, 50.00, 80.00, 10.00),
    (3, 22.00, 85.00, 10.00, 109.00, 139.00, 10.00),
    (4, 20.00, 80.00, 40.00, 141.00, 171.00, 10.00),
    (5, 20.00, 85.00, 20.00, 41.00, 71.00, 10.00),
    (6, 18.00, 75.00, 20.00, 95.00, 125.00, 10.00),
    (7, 15.00, 75.00, 20.00, 79.00, 109.00, 10.00),
]

# 차량 데이터
vehicle_capacity = 100  # 차량 수용량
num_vehicles = 4  # 차량 수
depot = (0, 40.00, 50.00, 0.00, 0.00, 240.00, 0.00)  # 출발 및 도착 위치

# 유전 알고리즘 파라미터
population_size = 8  # 개체 집단 크기
generations = 100  # 최대 세대 수


# 적합도 함수
def fitness(route):
    total_distance = 0
    total_demand = 0
    current_time = 0

    for vehicle_route in route:
        if not vehicle_route:
            continue

        vehicle_demand = 0  # 각 차량의 수요 초기화
        vehicle_time = 0  # 각 차량의 시간 초기화
        prev_customer = depot

        for customer_index in vehicle_route:
            customer = customers[customer_index]

            # 거리 계산
            distance = ((prev_customer[1] - customer[1]) ** 2 + (prev_customer[2] - customer[2]) ** 2) ** 0.5
            total_distance += distance

            # 수요 계산
            vehicle_demand += customer[3]

            # 시간 계산 (도착 시간 윈도우 준수)
            vehicle_time = max(vehicle_time + distance, customer[4])
            if vehicle_time > customer[5]:
                total_distance += vehicle_time - customer[5]
                vehicle_time = customer[5]

            prev_customer = customer

        # 출발지로 돌아가는 거리 및 시간 추가
        distance_to_depot = ((prev_customer[1] - depot[1]) ** 2 + (prev_customer[2] - depot[2]) ** 2) ** 0.5
        total_distance += distance_to_depot
        vehicle_time = max(vehicle_time + distance_to_depot, depot[4])

        total_demand += vehicle_demand

    return total_distance


# 초기 개체 생성
def generate_initial_solution():
    customers_indices = list(range(1, len(customers)))  # 고객 인덱스 리스트
    random.shuffle(customers_indices)
    routes = [[] for _ in range(num_vehicles)]
    vehicle_capacity_left = [vehicle_capacity] * num_vehicles

    for customer_index in customers_indices:
        # 각 차량에 대해 수용량을 초과하지 않으면 추가
        for i, route in enumerate(routes):
            if vehicle_capacity_left[i] >= customers[customer_index][3]:
                route.append(customer_index)
                vehicle_capacity_left[i] -= customers[customer_index][3]
                break

    return routes


# 교차 연산 (순서 교환)
def crossover(parent1, parent2):
    # 부모 경로에서 서로 다른 차량에 있는 고객을 교차
    child1 = [customer for customer in parent1]
    child2 = [customer for customer in parent2]

    for i in range(num_vehicles):
        if i % 2 == 0:
            continue  # 짝수 인덱스 차량은 parent1에서, 홀수 인덱스 차량은 parent2에서

        # 차량의 경로를 서로 교환
        for customer in parent1[i]:
            if customer in parent2[i]:
                child1[i].remove(customer)
                child2[i].append(customer)

    return child1, child2


# 돌연변이 연산 (두 고객 위치 교환)
def mutate(route):
    if not route:
        return

    mutation_point1, mutation_point2 = random.sample(range(len(route)), 2)
    route[mutation_point1], route[mutation_point2] = route[mutation_point2], route[mutation_point1]


# 유전 알고리즘 실행
def genetic_algorithm():
    population = [generate_initial_solution() for _ in range(population_size)]

    for generation in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.choices(population, k=2)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        population = new_population
        best_route = min(population, key=lambda route: fitness(route))
        best_distance = fitness(best_route)
        print(f"세대 {generation + 1}: 최단 거리 - {best_distance}")

    best_route = min(population, key=lambda route: fitness(route))
    best_distance = fitness(best_route)
    print(f"최종 최단 거리: {best_distance}")
    print("최적 경로:", best_route)


if __name__ == "__main__":
    genetic_algorithm()