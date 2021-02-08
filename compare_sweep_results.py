import itertools
import operator
import os

from log_parse import *

benchmark = '../stoke/embedder_eval/param_sweep/results/binary_affine'

# filenames = map(lambda s: benchmark + s,
# [
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_5.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_16.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_32.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_5.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_16.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_32.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_5.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_16.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_32.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_5.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_16.log',
#     'dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_32.log',
# ])

PARAMS = {
    'dist': ['hamming', 'affine'],
    'beta': [0.1, 0.3, 1, 10],
    'inum': [8, 16, 32],
}

def mk_filename(dist, beta, inum):
    return f'{benchmark}/dist_{dist}_gsm_0_rm_0_cost_correctness_beta_{beta}_inum_{inum}.log'


print('(beta; inum),Hamming Search Time (s),Affine Search Time (s)')
for (beta, inum) in itertools.product(PARAMS['beta'], PARAMS['inum']):
    hamming_data = get_search_data(mk_filename('hamming', beta, inum))
    if os.path.exists(mk_filename('affine', beta, inum)):
        affine_data = get_search_data(mk_filename('affine', beta, inum))
        print(f'({beta}; {inum}),{get_search_time(hamming_data)},{get_search_time(affine_data)}')
    else:
        print(f'({beta}; {inum}),{get_search_time(hamming_data)}')
    # print(f'[{beta=}, {inum=}]')
    # print('hamming:', get_search_time(hamming_data))
    # print('affine:', get_search_time(affine_data))
    # print('')
