import itertools
import operator
import glob
import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

from util import *

LOG_SCALE = False

def gen_graph(data, dist, beta, inum):
    # data = data[0]
    # searches = data['updates']
    # import pdb; pdb.set_trace()

    fig, axs = plt.subplots(len(data))
    plt.gca().invert_yaxis()

    [w, h] = fig.get_size_inches()
    h += len(data) - 1
    fig.set_size_inches(w, h)

    x_max = 0
    y_max = 0
    for ax, run_data in zip(axs, data):
        searches = run_data['updates']
        for search in searches:
            x = np.array(list(map(operator.itemgetter(0), search)), dtype=np.float64)
            y = np.array(list(map(operator.itemgetter(1), search)), dtype=np.float64)
            ax.plot(x, y)
            if not run_data['success']:
                ax.set_facecolor((1.0, 0.9, 0.9))
        x_max = max(x_max, max(map(lambda s: max(map(operator.itemgetter(0), s)), searches)))
        y_max = max(y_max, max(map(lambda s: max(map(operator.itemgetter(1), s)), searches)))

    raw_name = f'dist_{dist}_beta_{beta}_inum_{inum}'
    outname = f'{raw_name}.png'
    # title = ' '.join(raw_name.split('_')).title()
    title = f'Dist: {dist}, Beta: {beta}, Inum: {inum}'

    for i, ax in enumerate(axs):
        if LOG_SCALE:
            ax.set_yscale('log')
            ax.set_ylim([1, y_max * 1.1])
        else:
            ax.set_ylim([0, y_max * 1.1])
        ax.set_xlim([0, x_max * 1.1])
        ax.grid()
        if y_max > 1000000:
            def millions(x, pos):
                return '%1.1fM' % (x * 1e-6)
            ax.yaxis.set_major_formatter(FuncFormatter(millions))
        if i != len(axs) - 1:
            ax.xaxis.set_ticklabels([])

    axs[0].set(title=title)
    # ax[-1].set(xlabel='Time (s)', ylabel='Cost')
    axs[-1].set(xlabel='Time (s)')
    axs[len(axs)//2].set(ylabel='Cost')

    # plt.subplots_adjust(
    #     left=0.1,
    #     bottom=0.1,
    #     right=0.9,
    #     top=0.9,
    #     wspace=0.2,
    #     hspace=0.63)

    fig.savefig(outname, dpi=250)

# data_base_dir = '../stoke/embedder_eval/param_sweep/results'
# data_base_dir = 'archive/tc_restrict_num/2-3-21'
# data_base_dir = 'archive/tc_restrict_content/2-8-21'
data_base_dir = 'archive/tc_unused_reg/2-15-21'
benchmark = 'binary_affine'

# {
#     'dist': ['hamming', 'affine'],
#     # 'beta': [0.1, 0.3],
#     # 'inum': [5, 8, 16],
#     'beta': [0.005, 0.01, 0.1, 0.3],
#     'inum': [6],
# }
PARAMS = get_params(data_base_dir, benchmark)
# print(PARAMS)

def get_cell_data(data_base_dir, benchmark, dist, beta, inum):
    return [get_search_data(l) for l in get_logs(data_base_dir, benchmark, dist, beta, inum)]


for (beta, inum) in itertools.product(PARAMS['beta'], PARAMS['inum']):
    # hamming_data = get_cell_data(data_base_dir, benchmark, 'hamming', beta, inum)
    # gen_graph(hamming_data, 'hamming', beta, inum)
    # affine_data = get_cell_data(data_base_dir, benchmark, 'affine', beta, inum)
    # gen_graph(affine_data, 'affine', beta, inum)
    affine_all_reg_data = get_cell_data(data_base_dir, benchmark, 'affine_all_reg', beta, inum)
    gen_graph(affine_all_reg_data, 'affine_all_reg', beta, inum)
