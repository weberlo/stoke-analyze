import glob
import operator

import numpy as np

def get_search_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    searches = []
    curr_search = []
    total_candidates = None
    success = False
    # we sometimes process in-progress search logs with this function
    search_finished = False
    for i, line in enumerate(lines):
        if line.startswith('Doobs'):
            update_time = float(line.split(' ')[-1][:-3]) / 1000.0
            update_cost = int(lines[i+2].split('(')[1].split(')')[0])
            if curr_search and update_cost > curr_search[-1][1]:
                curr_search.append((update_time - 5.0, curr_search[-1][1]))
                searches.append(curr_search)
                curr_search = []
            curr_search.append((update_time, update_cost))
        elif line.startswith('Total search iterations'):
            total_candidates = int(line.split(':')[1].strip())
        elif line.startswith('Total search time'):
            total_search_time = float(line.split(':')[1].strip()[:-1])
        elif 'Search terminated successfully with a verified rewrite!' in line:
            success = True
        elif 'Final update' in line:
            search_finished = True

    if not search_finished and not success:
        # don't mark a search as unsuccessful if it's not finished
        success = True

    if not total_candidates:
        import pdb; pdb.set_trace()
    if curr_search:
        searches.append(curr_search)
    return {
        'updates': searches,
        'total_cands': total_candidates,
        'total_search_time': total_search_time,
        'success': success,
    }


def get_params(data_base_dir, benchmark):
    beta = set()
    inum = set()
    dist = set()
    for fname in glob.glob(f'{data_base_dir}/{benchmark}/0/*'):
        beta.add(fname.split('beta_')[1].split('_')[0])
        inum.add(fname.split('inum_')[1].split('_')[0].split('.')[0])
        dist.add(fname.split('dist_')[1].split('_gsm')[0])
    return {'beta': beta, 'inum': inum, 'dist': dist}


def get_logs(data_base_dir, benchmark, dist, beta, inum):
    return glob.glob(f'{data_base_dir}/{benchmark}/*/dist_{dist}_gsm*beta_{beta}*inum_{inum}*')


def flatten(l):
    return [x for ll in l for x in ll]


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

