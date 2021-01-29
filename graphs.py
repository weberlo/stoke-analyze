import operator
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# filename = 'affine_results.log'
# filename = '../stoke/embedder_eval/results/affine/stoke_results.log'
# filename = '../stoke/embedder_eval/results/affine/affine_results.log'
# filename = '../stoke/embedder_eval/results/affine/stoke_results.log'
# filename = '../stoke/embedder_eval/results/unary_affine/affine_results.log'
# filename = '../stoke/embedder_eval/results/unary_affine/stoke_results.log'
# filename = 'tutorial_correctness_plus_latency.log'

# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_16.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_32.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_8.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_16.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_32.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_8.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_16.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_32.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_8.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_16.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_32.log'
# filename = '../stoke/embedder_eval/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_8.log'

# filenames = [
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_5.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_32.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_5.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_32.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_5.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_32.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_5.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_32.log',
# ]

filenames = [
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.1_inum_5.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.1_inum_16.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.1_inum_32.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.3_inum_5.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.3_inum_16.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.3_inum_32.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_1_inum_5.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_1_inum_16.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_1_inum_32.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_10_inum_5.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_10_inum_16.log',
    '../stoke/embedder_eval/param_sweep/results/unary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_10_inum_32.log',
]

# filenames = [
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.1_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.1_inum_32.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_affine_gsm_0_rm_0_cost_correctness_beta_0.1_inum_8.log',
# ]

# filenames = [
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_32.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.1_inum_8.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_32.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_0.3_inum_8.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_32.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_10_inum_8.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_16.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_32.log',
#     '../stoke/embedder_eval/param_sweep/results/binary_affine/dist_hamming_gsm_0_rm_0_cost_correctness_beta_1_inum_8.log',
# ]

# filename = 'montmul_synth.log'
# filename = 'montmul_opt.log'

LOG_SCALE = False

def gen_graph(filename):
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
            # updates.append((update_time, update_cost))

    if curr_search:
        searches.append(curr_search)

    # searches[0] = [(searches[0][0][0] - 50.0, searches[0][0][1])] + searches[0]

    fig, ax = plt.subplots()
    plt.gca().invert_yaxis()

    for search in searches:
        x = np.array(list(map(operator.itemgetter(0), search)), dtype=np.float64)
        y = np.array(list(map(operator.itemgetter(1), search)), dtype=np.float64)
        ax.plot(x, y)

    raw_name = os.path.splitext(os.path.basename(filename))[0]
    outname = f'{raw_name}.png'
    title = ' '.join(raw_name.split('_')).title()
    ax.set(title=title)
    ax.set(xlabel='Time (s)', ylabel='Cost')

    y_max = max(map(lambda s: max(map(operator.itemgetter(1), s)), searches))

    # print(max(map(lambda s: max(map(operator.itemgetter(0), s)), searches)))
    # ax.set_xlim([0, 29655.0])

    if LOG_SCALE:
        plt.yscale('log')
        ax.set_ylim([1, y_max * 1.1])
    else:
        ax.set_ylim([0, y_max * 1.1])

    ax.grid()

    fig.savefig(outname, dpi=250)

    # plt.show()


for filename in filenames:
    gen_graph(filename)
