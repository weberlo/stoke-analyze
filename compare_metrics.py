import itertools
import operator

benchmark = '../stoke/embedder_eval/param_sweep/results/unary_linear'

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

def get_search_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    searches = []
    curr_search = []
    for i, line in enumerate(lines):
        if line.startswith('Doobs'):
            update_time = float(line.split(' ')[-1][:-3]) / 1000.0
            update_cost = int(lines[i+2].split('(')[1].split(')')[0])
            if curr_search and update_cost > curr_search[-1][1]:
                curr_search.append((update_time - 5.0, curr_search[-1][1]))
                searches.append(curr_search)
                curr_search = []
            curr_search.append((update_time, update_cost))

    if curr_search:
        searches.append(curr_search)
    return searches


PARAMS = {
    'dist': ['hamming', 'affine'],
    'beta': [0.1, 0.3, 1, 10],
    'inum': [5, 16, 32],
}

def mk_filename(dist, beta, inum):
    return f'{benchmark}/dist_{dist}_gsm_0_rm_0_cost_correctness_beta_{beta}_inum_{inum}.log'


def get_search_time(search_data):
    return max(map(lambda s: max(map(operator.itemgetter(0), s)), search_data))

print('(beta; inum),Hamming Search Time (s),Affine Search Time (s)')
for (beta, inum) in itertools.product(PARAMS['beta'], PARAMS['inum']):
    hamming_data = get_search_data(mk_filename('hamming', beta, inum))
    affine_data = get_search_data(mk_filename('affine', beta, inum))
    print(f'({beta}; {inum}),{get_search_time(hamming_data)},{get_search_time(affine_data)}')
    # print(f'[{beta=}, {inum=}]')
    # print('hamming:', get_search_time(hamming_data))
    # print('affine:', get_search_time(affine_data))
    # print('')
    pass
