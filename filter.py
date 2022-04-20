import pandas as pd
import numpy as np
import os
import re
from keywords import get_kw_match_score
from datetime import datetime

INPUT_DIR = 'inputs'
OUTPUT_DIR = 'outputs'
start_time = datetime.now()

# FIELDS
# MRL FIELDS
F_MRL_P_KEY = 'product_keywords'
F_MRL_M_KEY = 'manufacturer_keywords'
F_MRL_UID = 'Unique Identifier'
# TA FIELDS
F_TA_P_DETAILS = 'product details'
F_TA_EXP_NAME = 'exporter name'




# PARAMETERS
# _______________MANUAL SETTINGS SECTION_______________

# set to True if you prefer setting param values here
SET_STATIC_PARAMS = True 

# converts columns to lower case - leave as True
CONVERT_CASE = True

# how heavily to prefer *more* keyword matches when ratio of matches is equal
# MATCH_RANKING = (MATCHES ^ MATCH_POWER) / NUMBER_OF_KEYWORDS
# setting MATCH_POWER = 1 makes the MATCH_RANKING a simple ratio
MATCH_POWER = 2

#UMAIR'S PARAMS:
##################SET FILE NAMES#################################
Trade_Atlas='Indonesia 2021-Including Exchange Rates WA V2_Updated with Verification.xlsx'
#Trade Atlas File Requires extension xlsx

Trade_Atlas_Sheet='Indonesia 2021-Indonesia 2021V1'
#Sheet doesn't require an extension

MRL_FILE='Master reference list V2 CD.xlsx'
#MRL requires the extension

MRL_Sheet='Master Sheet 3.0-Deduped'
#Sheet doesn't require an extension

Exchange_Rate='Indonesia 2021-Including Exchange Rates WA V2_Updated with Verification.xlsx'
#Requires Extension xlsx

Exhchange_Rate_Sheet='Exchange rates'
#Sheet doesn't require an extension 
##################################################################
if SET_STATIC_PARAMS:
    # if SET_STATIC_PARAMS = True the script will use the values set here.
    PROC_MRL = True # set to True to process the MRL found at mrl.csv
    # CONVERT_CASE = True
    country = "India 2021"
    name = "version-12"
    sheet_name = 'Trade Atlas Records'

    filters = [  # if multiple contents, column value can match any
        {
            'col': F_TA_P_DETAILS,               # <-- "product details" column
            'contents': ['SAR', 'COV', 'corona'] # <-- filter out rows w/o one of these terms in the above col
            # }, {
            #     'col': F_TA_P_DETAILS,
            #     'contents': ['test']
        }
    ]

    classifiers = [
        # {
        #     'matchingCol': F_TA_P_DETAILS,
        #     'matchingValue': 'pcr',
        #     'labelCol': 'Test Type',
        #     'labelValue': 'Manual PCR',
        # },
        # {
        #     'matchingCol': F_TA_P_DETAILS,
        #     'matchingValue': 'Panbio',
        #     'labelCol': 'Test Type',
        #     'labelValue': 'Ag RDT',
        # },
        # {
        #     'matchingCol': F_TA_EXP_NAME,
        #     'matchingValue': 'Abbot',
        #     'labelCol': 'Test Type',
        #     'labelValue': 'Ag RDT',
        # },
    ]
    # __________________END MANUAL SETTINGS__________________
    # _______No changes should be made past this point_______

    COUNTRY_PATH = INPUT_DIR + '/' + country
    OUTPUT_PATH_FRAG = f'{OUTPUT_DIR}/{country}-{name}'
    OUTPUT_PATH = f'{OUTPUT_PATH_FRAG}.csv'
    OUTPUT_STATS_PATH = f'{OUTPUT_PATH_FRAG}-stats.json'
    print('using values from the _MANUAL SETTINGS SECTION_ of filters.py')
    print('data will be output to: ' + OUTPUT_PATH)
    print('with a stats file at: ' + OUTPUT_STATS_PATH)
else:
    country = input('country name (must match inputs folder name): \n')
    sheet_name = input(
        'sheet name of the data tab for any xslx input files (default is "Trade Atlas Records": \n'
    )
    if sheet_name == '':
        sheet_name = 'Trade Atlas Records'
    name = input(
        'identifier for the output file name (for your own use, can be left blank): \n'
    )
    COUNTRY_PATH = INPUT_DIR + '/' + country
    OUTPUT_PATH_FRAG = f'{OUTPUT_DIR}/{country}-{name}'
    OUTPUT_PATH = f'{OUTPUT_PATH_FRAG}.csv'
    OUTPUT_STATS_PATH = f'{OUTPUT_PATH_FRAG}-stats.json'

    PROC_MRL = input(
        'run MRL process to label top matches (any response but "n" will be taken to mean "yes"): \n'
    ) != "n"
	# CONVERT_CASE = input(
    #     'convert column names to lowercase (any response but "n" will be taken to mean "yes"): \n'
    # ) != "n"

    print('_____________________________________________\n')
    print(
        'you will now be asked to define filters. enter an empty col name when you are done.\n'
    )
    print(
        'row will be kept if its column value contains ANY of the values provided, case insensitive. enter multiple filters on the same column to filter to rows that match multiple values.\n'
    )
    print(
        'for example, to filter down to only rows that contain in their DETAILS column value the word "test" and *either* "covid" or "sars", enter the following filters:\n'
        + 'col name: details\n' + 'values, separated by commas: test\n' +
        'col name: details\n' + 'values, separated by commas: covid,sars\n')
    filters = []
    filterCol = 'x'
    filterContents = ''
    while filterCol:
        filterCol = input('col name: \n')
        if filterCol:
            filterContents = input('values, separated by commas: \n')
            filters.append({
                'col': filterCol,
                'contents': filterContents.split(',')
            })
            print('\n  Next filter (hit enter to continue):\n')

    print('_____________________________________________\n')

    print(
        'you will now be asked to define classifiers. enter an empty matching col name when you are done.\n'
    )
    print(
        'rows will be tested to see if their {matchingCol} value contains the {matchingValue} (case insensitive). if so, the row will be given a value of {labelValue} in its {labelCol} column (this can be a new column not in the original data).\n'
    )
    classifiers = []
    matchingCol = 'x'
    matchingValue = ''
    labelCol = ''
    labelValue = ''
    while matchingCol:
        matchingCol = input('matching col name: \n')
        if matchingCol:
            matchingValue = input('value to match: \n')
            labelValue = input('label to be given: \n')
            labelCol = input('column name to add label to: \n')
            classifiers.append({
                'matchingCol': matchingCol,
                'matchingValue': matchingValue,
                'labelValue': labelValue,
                'labelCol': labelCol,
            })
            print('\n  Next classifier (hit enter to continue):\n')

    print('_____________________________________________\n')
    print('data tab to be used: ' + sheet_name)
    print('data will be output to: ' + OUTPUT_PATH)
    print('with a stats file at: ' + OUTPUT_STATS_PATH)
    # print('will columns be made lower case: ', CONVERT_CASE)
    print('filters: ', filters)
    print('classifiers: ', classifiers)
    input("Hit enter to begin.")

# HELPERS
def read_spreadsheet(path): 
	if path.endswith('xlsx'):
		df = pd.read_excel(path, sheet_name, engine='openpyxl')
# reinstall xlrd if we want to try to
# elif path.endswith('xls'):
# df = pd.read_excel(path, engine='xlrd')
	elif path.endswith('csv'):
		df = pd.read_csv(path)
	return df

def process_filter(filter, df):
	# print(filter)
	# print(filter['col'])
	# df = df[filter['col']].str.contains(filter['contents'])
	# pred = False
	if filter['col'] in df.columns:
		# filtering: https://www.geeksforgeeks.org/get-all-rows-in-a-pandas-dataframe-containing-given-substring/
		# be sure filter['contents'] is a list? or don't use the regex approach
		df[filter['col']] = df[filter['col']].astype(str)
		wilded = ['.*' + c for c in filter['contents']]
		r = re.compile("|".join(wilded), re.IGNORECASE)
		return df[df[filter['col']].str.contains(pat=r, regex=True, na=False)]

	else:  # erase df if it doesn't contain filtered column
		return pd.DataFrame()

def process_classifier(classifier, df):
	if classifier['matchingCol'] in df.columns:
            if classifier['labelCol'] not in df.columns:
                df[classifier['labelCol']] = ""

            df[classifier['labelCol']] = np.where(
                df[classifier['matchingCol']].str.lower().str.contains( 
                    classifier['matchingValue'].lower()),
				# give it new label, otherwise preserve value (in case already labeled)
                classifier['labelValue'], df[classifier['labelCol']])

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
  match_set = tag_set&value_set
  if len(match_set) == 0:
	  # print(tag_set, "!")
	  return 0, ''
  if type == 'm':
    # TODO: implement kws for M, for now return tuple with empty scoreport
    return (len(match_set) ** MATCH_POWER) / len(tag_set), ''

  else:
    unmatched_set = tag_set - match_set
    s, sr = get_kw_match_score(match_set)
    # print(match_set, tag_set, unmatched_set)
    # print((s / (len(unmatched_set) + 1), sr), 'score\n')
    return (s / (len(unmatched_set) + 1), sr)


def trunc(stri, length_str):
	max_length = int(length_str) - 3
	# print(stri, max_length)
	if len(stri) > max_length:
		return stri[0:max_length] + '...'
	else:
		return stri

format_string = "{:<6} {:<12} {:<30} {:<50}"
def print_preview_row(f_string, items):
	lengths = str.strip(re.sub('\D+', ' ', f_string)).split(' ')
	# print(items)
	tup_items = (trunc(item, lengths[items.index(item)]) for item in items)
	print(f_string.format(*tup_items))

def process_mrl(mrl, ta):
	ta['Top P Match Score'] = 0
	ta['Top P Match UIDs'] = ''
	ta['Matching P Tags'] = ''
	ta['Top P Score Reports'] = ''

	ta['Top M Match Score'] = 0
	ta['Top M Match UIDs'] = ''
	ta['Matching M Tags'] = ''
	ta['Top M Score Reports'] = ''

	ta['Top Agg Match (P*M)'] = 0
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

	one_percent_done = round(len(ta)/100)
	for i, ta_row in ta.iterrows():
		
		if i % one_percent_done == 0:
			print(i/one_percent_done, '% done')
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
				tags_p = ",".join(list(p_tags_set&p_val_set))
				top_scoreport_p = p_scoreport
			elif (p_score > 0) & (p_score == top_score_p):
				top_match_p += " | " + mrl_row[F_MRL_UID]
				# add matching tags
				tags_p += " | " + ",".join(list(p_tags_set&p_val_set))
				top_scoreport_p += " | " + p_scoreport

			# MANUFACTURER
			m_tags = mrl_row[F_MRL_M_KEY]
			m_tags_set = string_to_set(m_tags, F_MRL_M_KEY, mrl_row, False)
			m_score, m_scoreport = get_match_score(m_tags_set, m_val_set, 'm')
			
			if m_score > top_score_m:
				top_score_m = m_score
				top_match_m = mrl_row[F_MRL_UID]
				# add matching tags
				tags_m = ",".join(list(m_tags_set&m_val_set))
				top_scoreport_m = m_scoreport
			elif (m_score > 0) & (m_score == top_score_m):
				top_match_m += " | " + mrl_row[F_MRL_UID]
				# add matching tags
				tags_m += " | " + ",".join(list(m_tags_set&m_val_set))
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
			print_preview_row(format_string, ('','Match Score','Match UIDs','Score Report / Tags'))
			print_preview_row(format_string, ('P: ', (str(round(top_score_p, 4))), top_match_p, top_scoreport_p))
			print_preview_row(format_string, ('M: ', (str(round(top_score_m, 4))), top_match_m, tags_m))
			print_preview_row(format_string, ('Agg: ', (str(round(top_score_agg, 4))), top_match_agg, ''))
		if (i == 50):
			print('\n___PREVIEW COMPLETE___\n')

	
	end_time = datetime.now()
	print(ta.head(100))
	print(end_time - start_mrl_time, 'time elapsed for mrl\n')
	print(end_time - start_time, 'total time elapsed\n\n')
	ta.to_csv(f'{OUTPUT_PATH_FRAG}-mrl-matched.csv')

	
# BEGIN SCRIPT
results = []
rows_dropped = 0
for path in os.listdir(COUNTRY_PATH):
    # source = pd.read_excel('inputs/' + path) eg inputs/pakistan/p.csv
    abs_path = COUNTRY_PATH + '/' + path
    print(abs_path)
    df = read_spreadsheet(abs_path)
    # df = read_spreadsheet('outputs/pakistan 2021-version7.csv') # UNDO just for testing
    print(abs_path)
    print(df.head)
    size_init = len(df)

    df['source_data_row'] = np.arange(len(df)) + 1
    df['source_file_name'] = path

    if CONVERT_CASE:
        df.columns = df.columns.str.lower()

    for filter in filters:
        print('pre filter: ', len(df))
        df = process_filter(filter, df)
        print('post filter: ', len(df))

# https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
    for classifier in classifiers:
        process_classifier(classifier, df)

    size_end = len(df)
    size_lost = size_init - size_end
    rows_dropped = rows_dropped + size_lost
    print("___________ADDING DATA__________")
    print(df.head)
    results.append(df)

result = pd.concat(results)
print("___________ALL RESULTS__________")
# print(results)
print(result.head(25))
result.to_csv(OUTPUT_PATH, index=False)
print(f'wrote {OUTPUT_PATH}')

f_strings = ' '.join(str(f) for f in filters)
c_strings = ' '.join(str(c) for c in classifiers)
stats = {
    'output_rows': len(result),
    'rows_dropped': rows_dropped,
    'input_files': (",").join(os.listdir(COUNTRY_PATH)),
    'sheet_name': sheet_name,
    'filters': f_strings,
    'classifiers': c_strings,
}
stats_df = pd.DataFrame(data=stats, index=[0])
stats_df.to_json(OUTPUT_STATS_PATH, 'records')
print(f'wrote {OUTPUT_STATS_PATH}')
end_main_time = datetime.now()
print(end_main_time - start_time, 'time elapsed\n\n')

if PROC_MRL:
	# get aggregated mrl
	# drop 1st row, keep 3 cols (as strings)
	mrl = pd.read_csv('mrl.csv', skiprows=1)[[F_MRL_M_KEY, F_MRL_P_KEY, F_MRL_UID]].astype(str)
	# merge rows if both types of keywords are equivalent
	# merge by joining UIDs with a ","
	mrl = mrl.groupby([F_MRL_M_KEY,F_MRL_P_KEY])[F_MRL_UID].agg(lambda x: ','.join(x)).drop_duplicates()
	mrl = mrl.reset_index()
	ta = result.reset_index()
	process_mrl(mrl, ta)

print('DONE')
