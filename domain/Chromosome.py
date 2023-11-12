from domain.Dataset import Dataset
from log.log_config import log
from typing import List


class Chromosome:

    def __init__(self, permutation: list):
        self.routes, self.waiting_time, self.total_distance = Chromosome.permutation_to_chromosome(permutation)
        if self.routes:
            self.vehicle_num = len(self.routes)
            self.fitness = None

    def __str__(self):
        return f"Vehicle Num: {self.vehicle_num}\tDistance: {self.total_distance}\tFitness: {self.fitness}\tRoutes: {self.routes}"

    @staticmethod
    def routes_to_permutation(routes: List[List[int]]) -> List[int]:
        result = []
        for route in routes:
            result.extend(route)
        return result

    @staticmethod
    def permutation_to_chromosome(permutation: list):
        # Return Values
        total_routes = []
        waiting_time = []
        total_distance = 0

        # 각 Route, 대기 시간
        cur_route = []
        cur_waiting = 0

        prev_demand = 0
        prev_time = 0
        prev_customer_idx = 0

        for cur_customer_idx in permutation:

            # + 방문
            cur_time = prev_time + Dataset.distance[prev_customer_idx][cur_customer_idx]
            cur_customer = Dataset.customers[cur_customer_idx]
            cur_demand = prev_demand + cur_customer.demand

            # Validate Constraint
            is_fit = True

            # Waiting
            ready_time = Dataset.customers[cur_customer_idx].ready_time
            if cur_time <= ready_time:
                cur_waiting += (ready_time - cur_time)
                cur_time = ready_time

            log.debug(f"[{cur_customer_idx}] -------------------------------------------------")
            log.debug(f"Demand Check {cur_demand}(cur) > {Dataset.capacity}(cap)")
            log.debug(f"Cus_Due Check {cur_time}(cur_t) > {cur_customer.due_time}(cus_due)")
            log.debug(
                f"Total_Due Check {cur_time + Dataset.distance[cur_customer_idx][0]}(cur_t with return) > {Dataset.customers[0].due_time}(due_time)")

            # Constraint Check
            # Constraint: Demand
            if cur_demand > Dataset.capacity:
                is_fit = False

            # Constraint: Current Due
            elif cur_time > cur_customer.due_time:
                is_fit = False

            # Constraint: Total Due(With Return)
            elif cur_time + Dataset.distance[cur_customer_idx][0] > Dataset.customers[0].due_time:
                is_fit = False

            cur_time += cur_customer.service_time
            log.debug(f"[{cur_customer_idx}] is_fit: {is_fit}")

            # Constraint Fitted
            if is_fit:
                # 현재 경로에 추가
                cur_route.append(cur_customer_idx)

                total_distance += Dataset.distance[prev_customer_idx][cur_customer_idx]
                prev_demand = cur_demand
                prev_time = cur_time
                prev_customer_idx = cur_customer_idx

            else:
                # Constraint 안 맞을 시 -> 다음 Route

                # Impossible Solution
                if not cur_route:
                    log.error(f"[{cur_customer_idx}] Impossible {cur_route}")
                    return None, None, None

                # 복귀
                total_distance += Dataset.distance[prev_customer_idx][0]

                # 저장
                total_routes.append(cur_route)
                waiting_time.append(cur_waiting)

                # 다음 차량 새로 출발
                total_distance += Dataset.distance[0][cur_customer_idx]

                # Sync
                cur_route = [cur_customer_idx]
                prev_demand = cur_customer.demand
                prev_time = Dataset.distance[0][cur_customer_idx] + cur_customer.service_time
                cur_waiting = 0

                # Waiting 확인
                if prev_time <= cur_customer.ready_time:
                    cur_waiting = cur_customer.ready_time - prev_time

                    prev_time = cur_customer.ready_time + cur_customer.service_time

                prev_customer_idx = cur_customer_idx

        # 마지막 저장
        if cur_route:
            # 복귀
            total_distance += Dataset.distance[prev_customer_idx][0]

            # 저장
            total_routes.append(cur_route)
            waiting_time.append(cur_waiting)

        return total_routes, waiting_time, total_distance
