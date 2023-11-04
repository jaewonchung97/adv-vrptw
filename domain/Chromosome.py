from Config import DATASET


class Chromosome:
    def __init__(self, permutation):
        self.routes, self.total_distance = get_chromosome(permutation)
        if self.routes:
            self.vehicle_num = len(self.routes)
            self.fitness = None


def get_chromosome(permutation: list):
    chrom = []
    # waiting_time = []
    total_distance = 0

    cur_route = []
    prev_demand = 0
    prev_time = 0
    prev_customer_idx = 0
    # prev_waiting = 0
    for cur_customer_idx in permutation:
        cur_customer = DATASET.customers[cur_customer_idx]
        cur_demand = prev_demand + cur_customer.demand

        # + 방문 + Service + Return
        cur_time = prev_time \
                   + DATASET.distance[prev_customer_idx][cur_customer_idx] \
                   + cur_customer.service_time \
                   + DATASET.distance[cur_customer_idx][0]

        # ready_time = DATASET.customers[cur_customer_idx].ready_time
        # Constraint: Ready Time (if wait)
        # if cur_time <= ready_time:
        #     cur_time = ready_time + cur_customer.service_time + DATASET.distance[cur_customer_idx][0]
        #     # Waiting Time
        #     prev_waiting += ready_time - cur_time

        # Constraint 적합: Capacity, 최종 Due_time, 현재 Due_time
        if cur_demand <= DATASET.capacity and \
                cur_time <= DATASET.customers[0].due_time:
                # cur_time <= DATASET.customers[cur_customer_idx].due_time:
            # 방문
            total_distance += DATASET.distance[prev_customer_idx][cur_customer_idx]

            cur_route.append(cur_customer_idx)
            prev_demand = cur_demand
            prev_time = cur_time - DATASET.distance[cur_customer_idx][0]

        else:
            # Constraint 안 맞을 시 -> 다음 Route
            chrom.append(cur_route)
            cur_route = [cur_customer_idx]

            # 도착
            total_distance += DATASET.distance[prev_customer_idx][0]

            # 출발
            total_distance += DATASET.distance[0][cur_customer_idx]

            # 초기화
            prev_demand = cur_customer.demand
            prev_time = DATASET.distance[0][cur_customer_idx] \
                        + cur_customer.service_time
            # 초기화 by Ready TIme
            # if prev_time <= cur_customer.ready_time:
            #     prev_time = cur_customer.ready_time + cur_customer.service_time
            prev_customer_idx = cur_customer_idx

            # Waiting time 초기화
            # waiting_time.append(prev_waiting)
            # prev_waiting = 0

    if cur_route:
        chrom.append(cur_route)

    # Vehicle Num
    if len(chrom) <= DATASET.vehicle_num:
        return chrom, total_distance
    else:
        return None, None
