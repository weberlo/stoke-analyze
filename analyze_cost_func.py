import itertools
import operator
import glob
import os
import pprint
import numpy as np

from util import *

data_base_dir = 'archive/tc_unused_reg/2-11-21'
# data_base_dir = '../stoke/embedder_eval/param_sweep/results'
benchmark = 'binary_affine'

PARAMS = get_params(data_base_dir, benchmark)
print(PARAMS)

def calc_best_params(data_base_dir, benchmark, dist):
    times = []
    for (beta, inum) in itertools.product(PARAMS['beta'], PARAMS['inum']):
        curr_avg_time = np.mean(aggregate_on_key(get_logs(data_base_dir, benchmark, dist, beta, inum), 'total_search_time'))
        times.append(((beta,inum), curr_avg_time))
    return min(times, key=lambda t: t[1])[0]


def calc_diff_avgs(data_base_dir, benchmark, dist):
    res = []
    for (beta, inum) in itertools.product(PARAMS['beta'], PARAMS['inum']):
        updates = flatten(map(lambda s: get_search_data(s)['updates'], glob.glob(f'{data_base_dir}/{benchmark}/*/dist_{dist}*beta_{beta}*inum_{inum}*')))
        ys = list(map(lambda s: list(map(operator.itemgetter(1), s)), updates))
        diffs = []
        for search in ys:
            diffs += list(map(lambda x: x[0] - x[1], zip(search, search[1:])))
        res.append(((beta,inum), (np.mean(diffs), np.std(diffs))))
    return res


all_diff_avgs = {}
for dist in ['hamming', 'affine', 'affine_all_reg']:  # PARAMS['dist']:
    all_diff_avgs[dist] = dict(calc_diff_avgs(data_base_dir, benchmark, dist))

for (beta, inum) in itertools.product(sorted(PARAMS['beta'], key=lambda s: float(s)), sorted(PARAMS['inum'])):
    cells = []
    for dist in ['hamming', 'affine', 'affine_all_reg']:  # PARAMS['dist']:
        cells += list(all_diff_avgs[dist][(beta,inum)])
    print(f'({beta};{inum}),' + ','.join(map(str, cells)))

    # print(dict(diff_avgs)[calc_best_params(data_base_dir, benchmark, dist)])
