import operator

def get_search_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    searches = []
    curr_search = []
    total_candidates = None
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

    if not total_candidates:
        import pdb; pdb.set_trace()
    if curr_search:
        searches.append(curr_search)
    return {'updates': searches, 'total_cands': total_candidates, 'total_search_time': total_search_time}
