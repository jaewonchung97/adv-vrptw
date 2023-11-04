class Dataset:
    def __init__(self, x, y, due, customers: list):
        depot = {x: x, y: y}
        due_time = due
        customers = customers
        distance_matrix = [[]]
