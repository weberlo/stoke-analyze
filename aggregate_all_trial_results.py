import itertools
import operator
import glob
import os
import pprint
import numpy as np

from log_parse import *

def aggregate_on_key(log_list, key):
    res = []
    for log in log_list:
        res.append(get_search_data(log)[key])
    return res


def get_search_times(log_list):
    return np.array(aggregate_on_key(log_list, 'total_search_time'))


def get_num_candidates(log_list):
    return np.array(aggregate_on_key(log_list, 'total_cands'))


def get_num_updates_per_search(log_list):
    return np.array(flatten(map(lambda s: list(map(lambda ss: len(ss), s)), aggregate_on_key(log_list, 'updates'))))


def get_num_searches(log_list):
    return np.array(list(map(lambda s: len(s), aggregate_on_key(log_list, 'updates'))))


def flatten(l):
    return [x for ll in l for x in ll]


PARAMS = {
    'dist': ['hamming', 'affine'],
    # 'beta': [0.1, 0.3],
    # 'inum': [5, 8, 16],
    'beta': [0.005, 0.01, 0.1, 0.3],
    'inum': [6],
}

# data_base_dir = 'archive/tc_restrict_content/2-8-21'
data_base_dir = '../stoke/embedder_eval/param_sweep/results'
benchmark = 'binary_affine'

print('(beta; inum),Avg Hamming Search Time (s),Hamming Std Dev,Avg Affine Search Time (s),Affine Std Dev')
# print('(beta; inum),Avg Num Searches,Std Dev,Avg Updates Per Search,Std Dev,Avg Num Searches,Std Dev,Avg Updates Per Search,Std Dev')
for (beta, inum) in itertools.product(PARAMS['beta'], PARAMS['inum']):
    hamming_logs = glob.glob(f'{data_base_dir}/{benchmark}/*/dist_hamming*beta_{beta}*inum_{inum}*')
    affine_logs = glob.glob(f'{data_base_dir}/{benchmark}/*/dist_affine_gsm*beta_{beta}*inum_{inum}*')
    affine_all_reg_logs = glob.glob(f'{data_base_dir}/{benchmark}/*/dist_affine_all_reg*beta_{beta}*inum_{inum}*')

    hamming_logs = filter(lambda s: '/5/' not in s, hamming_logs)
    affine_logs = filter(lambda s: '/5/' not in s, affine_logs)
    affine_all_reg_logs = filter(lambda s: '/5/' not in s, affine_all_reg_logs)
    print(beta,inum)
    print(get_num_candidates(hamming_logs))
    print(get_num_candidates(affine_logs))
    print(get_num_candidates(affine_all_reg_logs))

    # average number of updates
    # def get_search_csv(logs):
    #     num_searches = get_num_searches(logs)
    #     num_updates = get_num_updates_per_search(logs)
    #     return ','.join(map(str, [np.mean(num_searches), np.std(num_searches), np.mean(num_updates), np.std(num_updates)]))
    # hamming_cells = get_search_csv(hamming_logs)
    # affine_cells = get_search_csv(affine_logs)
    # print(f'({beta}; {inum}),{hamming_cells},{affine_cells}')

    # print(get_num_searches(hamming_logs))
    # print(get_num_updates_per_search(hamming_logs))
    # print(get_num_searches(affine_logs))
    # print(get_num_updates_per_search(affine_logs))

    # print(np.average(np.array(list(map(lambda l: len(flatten(get_search_data(l)['updates'])), hamming_logs)))))
    # print(np.average(np.array(list(map(lambda l: len(flatten(get_search_data(l)['updates'])), affine_logs)))))

    # def get_perf_csv(logs):
    #     times = get_search_times(logs)
    #     cands = get_num_candidates(logs)
    #     return ','.join(map(str, [np.mean(times), np.std(times), np.mean(cands), np.std(cands)]))
    # hamming_cells = get_perf_csv(hamming_logs)
    # affine_cells = get_perf_csv(affine_logs)
    # print(f'({beta}; {inum}),{hamming_cells},{affine_cells}')
