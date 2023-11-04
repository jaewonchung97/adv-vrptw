class Customer:
    def __init__(self, x, y, demand, ready_time, due_time, service_time):
        self.x = x
        self.y = y
        self.demand = int(demand)
        self.ready_time = int(ready_time)
        self.due_time = int(due_time)
        self.service_time = int(service_time)
