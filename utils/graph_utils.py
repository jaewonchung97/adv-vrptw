from matplotlib import pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

from config import FILE_SAVE, INSTANCE_NAME
from domain.Chromosome import Chromosome
from domain.Dataset import Dataset


def draw_routes(chromosome: Chromosome):
    fig, ax = plt.subplots()
    fig, (ax_routes, ax_boxplot) = plt.subplots(
        1, 2, gridspec_kw={'width_ratios': [3, 1]})

    for route in chromosome.routes:
        x = [Dataset.customers[i].x for i in route]
        y = [Dataset.customers[i].y for i in route]
        ax_routes.scatter(x, y, color='b')  # 원하는 색상으로 변경하세요.
        path_cor = [(x[i], y[i]) for i in range(len(x))]
        patch = patches.PathPatch(
            Path(path_cor), facecolor='none', lw=1, zorder=0)
        ax_routes.add_patch(patch)
    distances = [sum(Dataset.distance[route[i]][route[i+1]]
                     for i in range(len(route)-1)) for route in chromosome.routes]
    ax_boxplot.boxplot(distances, vert=False, widths=0.7,
                       patch_artist=True, showfliers=False)
    ax_boxplot.set_yticklabels(['Routes'])
    ax_boxplot.set_xlabel('Distance')
    ax_hist = ax_boxplot.twiny()
    ax_hist.hist(distances, bins='auto', alpha=0.7,
                 color='gray', orientation='horizontal')
    ax_hist.set_xlabel('Frequency')
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

        patch = patches.PathPatch(
            Path(path_cor), facecolor='none', lw=1, zorder=0)
        ax.add_patch(patch)

    if FILE_SAVE:
        plt.savefig(
            f"resources/images/{INSTANCE_NAME}_v{chromosome.vehicle_num}_d{round(chromosome.total_distance, 0)}.jpg")
    plt.show()
