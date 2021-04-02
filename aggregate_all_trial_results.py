import itertools
import operator
import glob
import os
import pprint
import numpy as np

from util import *

# data_base_dir = '/home/jessemichel/results'
data_base_dir = '../stoke/embedder_eval/param_sweep/results'
benchmark = 'binary_affine'
# benchmark = 'p07'

PARAMS = get_params(data_base_dir, benchmark)

# print('(beta; inum),Avg Hamming Search Time (s),Hamming Std Dev,Avg Affine Search Time (s),Affine Std Dev')
# print('(beta; inum),Avg Num Searches,Std Dev,Avg Updates Per Search,Std Dev,Avg Num Searches,Std Dev,Avg Updates Per Search,Std Dev')
for (beta, inum) in itertools.product(sorted(PARAMS['beta']), sorted(PARAMS['inum'])):
    hamming_logs = get_logs(data_base_dir, benchmark, 'hamming', beta, inum)
    # hamming_inf_logs = get_logs(data_base_dir, benchmark, 'hamming_inf_sig_undef_cost', beta, inum)
    # affine_logs = get_logs(data_base_dir, benchmark, 'affine', beta, inum)  # glob.glob(f'{data_base_dir}/{benchmark}/*/dist_affine_gsm*beta_{beta}*inum_{inum}*')
    # affine_all_reg_logs = get_logs(data_base_dir, benchmark, 'affine_all_reg', beta, inum)

    # print(beta,inum)
    print("num_candidates", get_num_candidates(hamming_logs))
    # print(get_num_candidates(affine_logs))
    # print(get_num_candidates(affine_all_reg_logs))
    # print('')

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

    def get_perf_csv(logs):
        times = get_search_times(logs)
        cands = get_num_candidates(logs)
        return ','.join(map(str, [np.mean(times), np.std(times), np.mean(cands), np.std(cands)]))

    hamming_cells = get_perf_csv(hamming_logs)
    # print("Hamming cells", hamming_cells)
    # affine_cells = get_perf_csv(affine_logs)
    # affine_all_reg_cells = get_perf_csv(affine_all_reg_logs)
    print(f'(Beta, inum), Hamming: ({beta}; {inum}),{hamming_cells}')
    # print(f'({beta}; {inum}),{affine_cells},{affine_all_reg_cells}')
    # print(f'({beta}; {inum}),{affine_cells}')
    # print(f'({beta}; {inum}),{affine_all_reg_cells}')
    # print('---------------------------------------------------')
