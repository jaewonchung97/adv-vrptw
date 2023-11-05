import os
import sys

from domain.Chromosome import Chromosome

from utils.load_dataset import load_dataset

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

route1 = "81 78 76 71 70 73 77 79 80 57 55 54 53 56 58 60 59 98 96 95 94 92 93 97 100 99 32 33 31 35 37 38 39 36 34 13 17 18 19 15 16 14 12 90 87 86 83 82 84 85 88 89 91 43 42 41 40 44 46 45 48 51 50 52 49 47 67 65 63 62 74 72 61 64 68 66 69 5 3 7 8 10 11 9 6 4 2 1 75 20 24 25 27 29 30 28 26 23 22 21"

sol = """
Route 1 : 2 21 73 41 56 4
Route 2 : 5 83 61 85 37 93
Route 3 : 14 44 38 43 13
Route 4 : 27 69 76 79 3 54 24 80
Route 5 : 28 12 40 53 26
Route 6 : 30 51 9 66 1
Route 7 : 31 88 7 10
Route 8 : 33 29 78 34 35 77
Route 9 : 36 47 19 8 46 17
Route 10 : 39 23 67 55 25
Route 11 : 45 82 18 84 60 89
Route 12 : 52 6
Route 13 : 59 99 94 96
Route 14 : 62 11 90 20 32 70
Route 15 : 63 64 49 48
Route 16 : 65 71 81 50 68
Route 17 : 72 75 22 74 58
Route 18 : 92 42 15 87 57 97
Route 19 : 95 98 16 86 91 100
"""


def txt_to_route(txt: str):
    result = []
    txt_split = txt.split('\n')
    for i, text in enumerate(txt_split):
        if i in [0, len(txt_split) - 1]:
            continue
        slicing = 10
        if i > 10:
            slicing += 1
        values = text[slicing:]
        values = values.strip().split()
        for idx, value in enumerate(values):
            values[idx] = int(value)
        result += values
    return result


def test():
    list_1 = [1, 2, 3, 4, 5]
    list_2 = [99, 98]
    list_1[-len(list_2):] = list_2
    print(list_1)


if __name__ == '__main__':
    test()
