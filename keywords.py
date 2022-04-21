from keywords_raw import cold_kws_m, avg_kws_m, warm_kws_m, hot_kws_m, cold_kws_p, avg_kws_p, warm_kws_p, hot_kws_p


def create_mw_kw_map(kw_list):
    mw_kws = list(filter(lambda kw: len(kw.split(' ')) > 1, kw_list))
    mw_map = {}
    for kw in mw_kws:
        kwl = kw.split(' ')
        key = kwl[0]
        # rest_l = kwl[1:]
        # rest_s = ' '.join(rest_l)
        rest_s = set(kwl)
        if key in mw_map:
            mw_map[key].append(rest_s)
        else:
            mw_map[key] = [rest_s]
    return mw_map


kw_configs = {
    'p': [
        {
            'terms': set(hot_kws_p),
            'mw_map': create_mw_kw_map(hot_kws_p),
            'weight': 20,
        },
        {
            'terms': set(warm_kws_p),
            'mw_map': create_mw_kw_map(warm_kws_p),
            'weight': 4,
        },
        {
            'terms': set(avg_kws_p),
            'mw_map': create_mw_kw_map(avg_kws_p),
            'weight': 1,
        },
        {
            'terms': set(cold_kws_p),
            'mw_map': create_mw_kw_map(cold_kws_p),
            'weight': 0,
        },
    ],
    'm': [
        {
            'terms': set(hot_kws_m),
            'mw_map': create_mw_kw_map(hot_kws_m),
            'weight': 20,
        },
        {
            'terms': set(warm_kws_m),
            'mw_map': create_mw_kw_map(warm_kws_m),
            'weight': 4,
        },
        {
            'terms': set(avg_kws_m),
            'mw_map': create_mw_kw_map(avg_kws_m),
            'weight': 1,
        },
        {
            'terms': set(cold_kws_m),
            'mw_map': create_mw_kw_map(cold_kws_m),
            'weight': 0,
        },
    ],
}

# match_set: set of matched keywords
# type : 'p' or 'm', for manufacturer or product kws
def get_kw_match_score(match_set, type):
    score = 0
    score_report = {}
    # track used kws to skip terms that've already been counted
    used_set = set()
    # print(match_set)
    for kw_config in kw_configs[type]:
        # print('\n---   Looking at weight: ', kw_config['weight'], score, used_set)
        for kw in match_set:
            # print('\n - considering kw: ', kw, score, used_set, '\n')
            if kw in used_set:
                # print(kw, 'was already found')
                # move on to next kw in loop
                continue

            if kw in kw_config['terms']:
                # print('found ', kw, ' score was ', score)
                score += kw_config['weight']
                score_report[kw] = kw_config['weight']
                used_set.add(kw)
                # print('now ', score, ' used set ', used_set)
                # move on to next kw in loop
                continue

            elif kw in kw_config['mw_map']:
                # print('in elif')
                # check if kw is starting term of a multi-word kw
                for kw_set in kw_config['mw_map'][kw]:
                    # print('potential mw match with terms: ', kw_set)
                    # if yes, check if all terms in the mw kw are in the matched set
                    if len(match_set & kw_set) >= len(kw_set):
                        # print('found ', kw_set, ' score was ', score)
                        score += kw_config['weight']
                        score_report['_'.join(kw_set)] = kw_config['weight']
                        # add all terms in the mw kw to the used_set
                        used_set = used_set | kw_set
                        # print('now ', score, ' used set ', used_set)
                        # match found, so end this loop and move to next kw in loop
                        break
                    # print('not found')

    # print('done matching', score, match_set, used_set)
    unused_set = match_set - used_set
    # print(unused_set)
    score += len(unused_set)
    if len(unused_set) > 0:
        score_report[','.join(unused_set)] = '1ea'
    # print('final ', score, str(score_report))
    return (score, str(score_report))
