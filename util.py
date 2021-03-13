import glob
import operator
import re

import numpy as np

def _get_search_data_single(lines):
    searches = []
    curr_search = []
    total_candidates = None
    total_search_time = None
    success = False
    # we sometimes process in-progress search logs with this function
    search_finished = False
    for i, line in enumerate(lines):
        if match := re.match('Doobs Time Since Search Start: ([0-9.]+)ms', line):
            update_time = float(match[1]) / 1000.0
            for j in range(i, min(i + 5, len(lines))):
                # if match := re.match('Lowest Cost Discovered \(([0-9]+)\)     Lowest Known Correct Cost \([0-9]+\)', line):
                if match := re.match('.*Lowest Cost Discovered \(([0-9]+)\).*', line):
                    import pdb; pdb.set_trace()
                    update_cost = int(lines[i+2].split('(')[1].split(')')[0])
                    if curr_search and update_cost > curr_search[-1][1]:
                        curr_search.append((update_time - 5.0, curr_search[-1][1]))
                        searches.append(curr_search)
                        curr_search = []
                    curr_search.append((update_time, update_cost))
                    break
        elif (match := re.match('Iterations: +([0-9]+)', line)) or (match := re.match('Total search iterations: +([0-9]+)', line)):
            total_candidates = int(match[1])
        elif (match := re.match('Total search time: +([0-9]+)s', line)) or (match := re.match('Elapsed Time: +([0-9.]+)s', line)):
            total_search_time = float(match[1])
        elif 'Search terminated successfully with a verified rewrite!' in line:
            success = True
        elif 'Final update' in line:
            search_finished = True

    if not search_finished and not success:
        # don't mark a search as unsuccessful if it's not finished
        success = True

    if not total_candidates:
        total_candidates = 0
    if not total_search_time:
        total_search_time = 0.0
    if curr_search:
        searches.append(curr_search)
    return {
        'updates': searches,
        'total_cands': total_candidates,
        'total_search_time': total_search_time,
        'success': success,
    }


def get_search_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    if any(map(lambda l: l.startswith('[Thread '), lines)):
        thread_to_lines = {}
        for line in lines:
            if (match := re.match('\[Thread ([0-9]+)\] ', line)) and not re.match('.+\[Thread [0-9]+\] ', line):
                idx = int(match[1])
                thread_to_lines.setdefault(idx, []).append(line.split('] ')[1])
        return {i: _get_search_data_single(thread_lines) for (i, thread_lines) in thread_to_lines.items()}
    else:
        return _get_search_data_single(lines)


def get_params(data_base_dir, benchmark):
    beta = set()
    inum = set()
    dist = set()
    for fname in (set(glob.glob(f'{data_base_dir}/{benchmark}/0/*')) | set(glob.glob(f'{data_base_dir}/{benchmark}/1/*'))):
        beta.add(fname.split('beta_')[1].split('_')[0])
        inum.add(fname.split('inum_')[1].split('_')[0].split('.')[0])
        dist.add(fname.split('dist_')[1].split('_gsm')[0])
    return {'beta': beta, 'inum': inum, 'dist': dist}


def get_logs(data_base_dir, benchmark, dist, beta, inum):
    return glob.glob(f'{data_base_dir}/{benchmark}/*/dist_{dist}_gsm*beta_{beta}*inum_{inum}*')


def flatten(l):
    return [x for ll in l for x in ll]


def aggregate_on_key(log_list, key, reduction_fn=None):
    res = []
    for log in log_list:
        data = get_search_data(log)
        if reduction_fn is None:
            res.append(data[key])
        else:
            # print(f'NOTE: using reduction function `{reduction_fn}` on multithreaded data')
            # print(key, ':', list(map(lambda d: d[key], data.values())))
            res.append(reduction_fn(map(lambda d: d[key], data.values())))
    return res


def get_search_times(log_list):
    return np.array(aggregate_on_key(log_list, 'total_search_time', reduction_fn=min))


def get_num_candidates(log_list):
    return np.array(aggregate_on_key(log_list, 'total_cands', reduction_fn=sum))


def get_num_updates_per_search(log_list):
    return np.array(flatten(map(lambda s: list(map(lambda ss: len(ss), s)), aggregate_on_key(log_list, 'updates'))))


def get_num_searches(log_list):
    return np.array(list(map(lambda s: len(s), aggregate_on_key(log_list, 'updates'))))

