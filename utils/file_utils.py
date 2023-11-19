import pickle
import os

from config import INSTANCE_NAME, CUSTOMER_SIZE

filepath = os.path.join(os.path.abspath(os.path.dirname(
    os.path.dirname(__file__))), f"resources/candidates/{INSTANCE_NAME}/{CUSTOMER_SIZE}")
os.makedirs(filepath, exist_ok=True)


def save_file(file, file_name):
    with open(os.path.join(filepath, f"{file_name}.pkl"), "wb") as f:
        pickle.dump(file, f)
        f.close()


def read_file(file_name):
    with open(os.path.join(filepath, f"{file_name}.pkl"), "rb") as f:
        load = pickle.load(f)
        f.close()
    return load
