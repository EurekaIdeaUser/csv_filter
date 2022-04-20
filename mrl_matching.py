import pandas as pd
from datetime import datetime
import re
from helpers import print_preview_row
from consts import F_MRL_M_KEY, F_MRL_P_KEY, F_MRL_UID, F_TA_EXP_NAME, F_TA_P_DETAILS, ROW_PREV_FORMAT_STRING
from keywords import get_kw_match_score

# how heavily to prefer *more* keyword matches when ratio of matches is equal
# MATCH_RANKING = (MATCHES ^ MATCH_POWER) / NUMBER_OF_KEYWORDS
# setting MATCH_POWER = 1 makes the MATCH_RANKING a simple ratio
MATCH_POWER = 2

def string_to_set(input, col, row, filter_chars):
    # exporter name is sometimes blank (converted to NaN“)
    if type(input) != str:
        # print("bad string: ", input, col, row)
        return set()

    if filter_chars:
        # NOTE: keep in sync with how p/m_keywords are created in MRL
        # currently: drop non-alphanumeric chars, replacing "-" with " "
        f_input = re.sub("[^a-zA-Z\s0-9\-]", '', input)
        s = set(f_input.lower().replace('-', ' ').split(" "))
    else:
        s = set(input.lower().split(" "))
    if '' in s:
        s.remove('')
    # print(s, str)
    return s


def get_match_score(tag_set, value_set, type):
    match_set = tag_set & value_set
    if len(match_set) == 0:
        # print(tag_set, "!")
        return 0, ''
    if type == 'm':
        # TODO: implement kws for M, for now return tuple with empty scoreport
        return (len(match_set)**MATCH_POWER) / len(tag_set), ''

    else:
        unmatched_set = tag_set - match_set
        s, sr = get_kw_match_score(match_set)
        # print(match_set, tag_set, unmatched_set)
        # print((s / (len(unmatched_set) + 1), sr), 'score\n')
        return (s / (len(unmatched_set) + 1), sr)


def process_mrl(mrl, ta):
    ta['Matching P Tags'] = ''
    ta['Top P Score Reports'] = ''

    ta['Matching M Tags'] = ''
    ta['Top M Score Reports'] = ''

    ta['Top P Match Score'] = 0
    ta['Top M Match Score'] = 0
    ta['Top Agg Match (P&M)'] = 0
	
    ta['Top P Match UIDs'] = ''
    ta['Top M Match UIDs'] = ''
    ta['Top Agg Match UIDs'] = ''

    top_score_p_idx = ta.columns.get_loc('Top P Match Score')
    tags_p_idx = ta.columns.get_loc('Matching P Tags')
    top_scoreport_p_idx = ta.columns.get_loc('Top P Score Reports')

    top_score_m_idx = ta.columns.get_loc('Top M Match Score')
    tags_m_idx = ta.columns.get_loc('Matching M Tags')
    top_scoreport_m_idx = ta.columns.get_loc('Top M Score Reports')

    top_score_agg_idx = ta.columns.get_loc('Top Agg Match (P&M)')

    top_match_p_idx = ta.columns.get_loc('Top P Match UIDs')
    top_match_m_idx = ta.columns.get_loc('Top M Match UIDs')
    top_match_agg_idx = ta.columns.get_loc('Top Agg Match UIDs')

    start_mrl_time = datetime.now()
    print(start_mrl_time, 'beginning long tag comparison process...')
    print("Preview of first 50 rows' results: ")

    one_percent_done = round(len(ta) / 100)
    for i, ta_row in ta.iterrows():

        if i % one_percent_done == 0:
            print(i / one_percent_done, '% done')
        # if i > 100:
        # 	break
        top_match_p = ''
        top_score_p = 0
        tags_p = ''
        top_scoreport_p = ''

        top_match_m = ''
        top_score_m = 0
        tags_m = ''
        top_scoreport_m = ''

        top_match_agg = ''
        top_score_agg = 0

        # print(i, " of ", len(ta))
        p_val = ta_row[F_TA_P_DETAILS]
        p_val_set = string_to_set(p_val, F_TA_P_DETAILS, ta_row, True)

        m_val = ta_row[F_TA_EXP_NAME]
        m_val_set = string_to_set(m_val, F_TA_EXP_NAME, ta_row, True)

        for j, mrl_row in mrl.iterrows():
            # if j % 50 > 0:
            # 	break
            # print(i, j, p_val)

            # PRODUCT
            p_tags = mrl_row[F_MRL_P_KEY]
            p_tags_set = string_to_set(p_tags, F_MRL_P_KEY, mrl_row, False)
            p_score, p_scoreport = get_match_score(p_tags_set, p_val_set, 'p')

            if p_score > top_score_p:
                top_score_p = p_score
                top_match_p = mrl_row[F_MRL_UID]
                # add matching tags
                tags_p = ",".join(list(p_tags_set & p_val_set))
                top_scoreport_p = p_scoreport
            elif (p_score > 0) & (p_score == top_score_p):
                top_match_p += " | " + mrl_row[F_MRL_UID]
                # add matching tags
                tags_p += " | " + ",".join(list(p_tags_set & p_val_set))
                top_scoreport_p += " | " + p_scoreport

            # MANUFACTURER
            m_tags = mrl_row[F_MRL_M_KEY]
            m_tags_set = string_to_set(m_tags, F_MRL_M_KEY, mrl_row, False)
            m_score, m_scoreport = get_match_score(m_tags_set, m_val_set, 'm')

            if m_score > top_score_m:
                top_score_m = m_score
                top_match_m = mrl_row[F_MRL_UID]
                # add matching tags
                tags_m = ",".join(list(m_tags_set & m_val_set))
                top_scoreport_m = m_scoreport
            elif (m_score > 0) & (m_score == top_score_m):
                top_match_m += " | " + mrl_row[F_MRL_UID]
                # add matching tags
                tags_m += " | " + ",".join(list(m_tags_set & m_val_set))
                top_scoreport_m += " | " + m_scoreport

            # AGG
            agg_score = m_score + p_score
            if (m_score > 0) & (p_score > 0):
                # give matchers of both an added boost
                # TODO: extract multiplier as var?
                agg_score *= 2

            if agg_score > top_score_agg:
                top_score_agg = agg_score
                top_match_agg = mrl_row[F_MRL_UID]
                # add matching tags
                # tags_m = ",".join(list(m_tags_set&m_val_set))
            elif (agg_score > 0) & (agg_score == top_score_agg):
                top_match_agg += " | " + mrl_row[F_MRL_UID]
                # add matching tags
                # tags_m += " | " + ",".join(list(m_tags_set&m_val_set))

        ta.iloc[i, top_match_m_idx] = top_match_m
        ta.iloc[i, top_score_m_idx] = top_score_m
        ta.iloc[i, tags_p_idx] = tags_p
        ta.iloc[i, top_scoreport_p_idx] = top_scoreport_p

        ta.iloc[i, top_match_p_idx] = top_match_p
        ta.iloc[i, top_score_p_idx] = top_score_p
        ta.iloc[i, tags_m_idx] = tags_m
        ta.iloc[i, top_scoreport_m_idx] = top_scoreport_m

        ta.iloc[i, top_match_agg_idx] = top_match_agg
        ta.iloc[i, top_score_agg_idx] = top_score_agg

        if (i < 50):
            print('\n row: ', i)
            print_preview_row(
                ROW_PREV_FORMAT_STRING,
                ('', 'Match Score', 'Match UIDs', 'Score Report / Tags'))
            print_preview_row(ROW_PREV_FORMAT_STRING, ('P: ', (str(
                round(top_score_p, 4))), top_match_p, top_scoreport_p))
            print_preview_row(
                ROW_PREV_FORMAT_STRING,
                ('M: ', (str(round(top_score_m, 4))), top_match_m, tags_m))
            print_preview_row(
                ROW_PREV_FORMAT_STRING,
                ('Agg: ', (str(round(top_score_agg, 4))), top_match_agg, ''))
        if (i == 50):
            print('\n___PREVIEW COMPLETE___\n')

    end_time = datetime.now()
    print(ta.head(100))
    print(end_time - start_mrl_time, 'time elapsed for mrl\n')
    return ta

def MRL_MATCHING_MAIN(df, mrl_csv):
    # get aggregated mrl
    # drop 1st row, keep 3 cols (as strings)
    mrl = pd.read_csv(mrl_csv,
                      skiprows=1)[[F_MRL_M_KEY, F_MRL_P_KEY,
                                   F_MRL_UID]].astype(str)
    # merge rows if both types of keywords are equivalent
    # merge by joining UIDs with a ","
    mrl = mrl.groupby(
        [F_MRL_M_KEY,
         F_MRL_P_KEY])[F_MRL_UID].agg(lambda x: ','.join(x)).drop_duplicates()
    mrl = mrl.reset_index()
    ta = df.reset_index()
    return process_mrl(mrl, ta)
