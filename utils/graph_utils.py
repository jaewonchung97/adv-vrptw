from matplotlib import pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

from config import FILE_SAVE, INSTANCE_NAME, DRAW_GRAPH
from domain.Chromosome import Chromosome
from domain.Dataset import Dataset


def draw_routes(chromosome: Chromosome):
    if not DRAW_GRAPH:
        return
    fig, ax = plt.subplots()
    for chrom in chromosome.routes:
        x = []
        y = []
        x.append(Dataset.customers[0].x)
        y.append(Dataset.customers[0].y)
        for i, custom_i in enumerate(chrom):
            x.append(Dataset.customers[custom_i].x)
            y.append(Dataset.customers[custom_i].y)
        x.append(Dataset.customers[0].x)
        y.append(Dataset.customers[0].y)
        ax.scatter(x, y, color=f'C{i % 9}')
        path_cor = []
        for custom_i in range(len(x)):
            path_cor.append((x[custom_i], y[custom_i],))

        patch = patches.PathPatch(Path(path_cor), facecolor='none', lw=1, zorder=0)
        ax.add_patch(patch)

    if FILE_SAVE:
        plt.savefig(
            f"resources/images/{INSTANCE_NAME}_v{chromosome.vehicle_num}_d{round(chromosome.total_distance, 0)}.jpg")
    plt.show()
