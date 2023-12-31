from domain.Dataset import Dataset
from domain.Customer import Customer
from config import INSTANCE_NAME, CUSTOMER_SIZE
import os

"""
0 R101
1 
2 VEHICLE
3 NUMBER     CAPACITY
4   25         200
5 
6 CUSTOMER
7 CUST NO.   XCOORD.   YCOORD.    DEMAND   READY TIME   DUE DATE   SERVICE TIME
8  
9     0          35      35           0       0         230           0
10     1          41      49          10     161         171          10
11     2          35      17           7      50          60          10
...
"""


def get_cus(parameters):
    return Customer(int(parameters[1]), int(parameters[2]), int(parameters[3]), parameters[4], parameters[5],
                    parameters[6])


def load_dataset() -> None:
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"resources/datasets/{INSTANCE_NAME}.txt")
    with open(filepath) as f:
        customers = []
        for idx, line in enumerate(f):
            if idx in [0, 1, 2, 3, 5, 6, 7, 8]:
                pass
            elif idx == 4:
                params = line.strip().split()
                vehicle_num = int(params[0])
                capacity = int(params[1])
            elif idx <= 9 + CUSTOMER_SIZE:
                params = line.strip().split()
                customers.append(get_cus(params))
        Dataset(vehicle_num, capacity, customers)
        f.close()