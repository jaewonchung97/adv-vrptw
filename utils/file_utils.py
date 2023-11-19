import pickle
import os
import numpy as np

filepath = os.path.join(os.path.abspath(os.path.dirname(
    os.path.dirname(__file__))), "resources/candidates")


def save_file(file, file_name):
    with open(os.path.join(filepath, f"{file_name}.pkl"), "wb") as f:
        pickle.dump(file, f)
        f.close()


def read_file(file_name):
    with open(os.path.join(filepath, f"{file_name}.pkl"), "rb") as f:
        load = pickle.load(f)
        f.close()
    return load


def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data_start_index = lines.index("NODE_COORD_SECTION\n") + 1
    data_end_index = lines.index("DEMAND_SECTION\n")

    data_lines = lines[data_start_index:data_end_index]
    data = [list(map(float, line.strip().split()[1:3])) for line in data_lines]

    num_customers = len(data)

    coordinates = np.array(data)
    distance_matrix = np.zeros((num_customers, num_customers))

    for i in range(num_customers):
        for j in range(num_customers):
            distance_matrix[i, j] = np.linalg.norm(
                coordinates[i] - coordinates[j])

    ready_times = np.array([0] + [float(line.strip().split()[4])
                           for line in data_lines])
    due_dates = np.array([0] + [float(line.strip().split()[5])
                         for line in data_lines])
    service_times = np.array(
        [0] + [float(line.strip().split()[6]) for line in data_lines])

    time_matrix = np.zeros((num_customers, num_customers))

    for i in range(num_customers):
        for j in range(num_customers):
            time_matrix[i, j] = max(
                0, ready_times[j] - (due_dates[i] + service_times[i]))

    return {
        "distance_matrix": distance_matrix,
        "time_matrix": time_matrix
    }
