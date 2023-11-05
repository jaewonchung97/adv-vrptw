from domain.Dataset import Dataset
from log.log_config import log


class Chromosome:
    dataset = None

    def __init__(self, permutation: list, dataset: Dataset = None):

        if Chromosome.dataset is None:
            Chromosome.dataset = dataset

        self.routes, self.waiting_time, self.total_distance = self.get_chromosome(permutation)
        if self.routes:
            self.vehicle_num = len(self.routes)
            self.fitness = None

    @staticmethod
    def get_chromosome(permutation: list):
        dataset = Chromosome.dataset

        total_routes = []
        waiting_time = []
        total_distance = 0

        cur_route = []
        cur_waiting = 0

        prev_demand = 0
        prev_time = 0
        prev_customer_idx = 0

        for cur_customer_idx in permutation:
            cur_customer = dataset.customers[cur_customer_idx]
            cur_demand = prev_demand + cur_customer.demand

            # + 방문
            cur_time = prev_time + dataset.distance[prev_customer_idx][cur_customer_idx]

            # Validate Constraint
            is_fit = True

            ready_time = dataset.customers[cur_customer_idx].ready_time

            # Waiting
            if cur_time <= ready_time:
                cur_waiting += (ready_time - cur_time)
                cur_time = ready_time

            # TODO -- Due time이 Service 시간 포함(순서 변경)인지 아닌지
            #   # + Service
            #  cur_time += cur_customer.service_time

            log.debug(f"[{cur_customer_idx}] -------------------------------------------------")
            log.debug(f"Demand Check {cur_demand}(cur) > {dataset.capacity}(cap)")
            log.debug(f"Cus_Due Check {cur_time}(cur_t) > {cur_customer.due_time}(cus_due)")
            log.debug(
                f"Total_Due Check {cur_time + dataset.distance[cur_customer_idx][0]}(cur_t with return) > {dataset.customers[0].due_time}(due_time)")

            # Constraint Check
            # Constraint: Demand
            if cur_demand > dataset.capacity:
                is_fit = False

            # Constraint: Current Due
            elif cur_time > cur_customer.due_time:
                is_fit = False

            # Constraint: Total Due(With Return)
            elif cur_time + dataset.distance[cur_customer_idx][0] > dataset.customers[0].due_time:
                is_fit = False

            # TODO -- Service Time 추가
            cur_time += cur_customer.service_time

            log.debug(f"[{cur_customer_idx}] is_fit: {is_fit}")
            # Constraint Fitted
            if is_fit:
                # 루트에 추가
                cur_route.append(cur_customer_idx)

                total_distance += dataset.distance[prev_customer_idx][cur_customer_idx]
                prev_demand = cur_demand
                prev_time = cur_time
                prev_customer_idx = cur_customer_idx

            else:
                # Constraint 안 맞을 시 -> 다음 Route

                # Impossible Solution
                if not cur_route:
                    log.Error(f"[{cur_customer_idx}] Impossible {cur_route}")
                    return None, None, None

                # 복귀
                total_distance += dataset.distance[prev_customer_idx][0]

                # 저장
                total_routes.append(cur_route)
                waiting_time.append(cur_waiting)

                # 다음 차량 새로 출발
                total_distance += dataset.distance[0][cur_customer_idx]

                # Sync
                cur_route = [cur_customer_idx]
                prev_demand = cur_customer.demand
                prev_time = dataset.distance[0][cur_customer_idx] + cur_customer.service_time
                cur_waiting = 0

                # Waiting 확인
                if prev_time <= cur_customer.ready_time:
                    cur_waiting = cur_customer.ready_time - prev_time

                    prev_time = cur_customer.ready_time + cur_customer.service_time

                prev_customer_idx = cur_customer_idx

        # 마지막 찌꺼기 저장
        if cur_route:
            # 복귀
            total_distance += dataset.distance[prev_customer_idx][0]

            # 저장
            total_routes.append(cur_route)
            waiting_time.append(cur_waiting)

        # # Constraint: Vehicle Num
        # if len(total_routes) <= dataset.vehicle_num:
        #     return total_routes, waiting_time, total_distance
        # else:
        #     log.error(f"[End] Too Many Routes {total_routes}")
        #     return None, None, None

        return total_routes, waiting_time, total_distance
