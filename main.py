import pandas as pd
import numpy as np
from datetime import datetime
import os
from helpers import read_spreadsheet, do_stats, print_update
from custom_filters import CUSTOM_FILTERS_MAIN
from classifiers import CLASSIFIERS_MAIN
from mrl_matching import MRL_MATCHING_MAIN
from umair import UMAIR_MAIN

################### INSTRUCTIONS:
#
# To run the tool, place any input files in the inputs folder on the left
# <----------------------------------------------------------------------
# These should be placed in a subfolder named with the country the data
# pertain to (eg "india"). Then set the PARAMETERS values described below.
# Once they're set, click the green Run button above ↑↑↑↑↑↑↑↑
# It may take a minute to install the python packages used by the script.
#
# Wait for the script to execute. This may take a few minutes depending on
# the size of the input files. You'll know the script has finished when it
# prints DONE to the screen. You'll then find your output files in the
# outputs folder (a csv with the resulting data, and a json file with some
# details like how many rows were dropped).
#

################### PARAMETERS:

# country name: must match the name of the folder you created (eg "india")
COUNTRY = "Indonesia 2021"

# sheet name: must match the name of the tab containing the relevant data
# in any xslx files provided (eg "Trade Atlas Records")
SHEET_NAME = 'Trade Atlas Records'

# file identifier: arbitrary, it will be tacked on to the output file name
# (distinguishing it from others generated for the same country)
NAME = "version-13"

# MRL file
MRL_CSV = 'mrl.csv'

# RUN FLAGS - determine which code will execute. set each to True or False

# filter rows to only those which pass the custom FILTERS defined below
RUN_CUSTOM_FILTERS = True

# add output columns to label rows that match certain criteria
# define your CLASSIFIERS below
RUN_CLASSIFIERS = True

# adds an output ending in 'mrl-matched.csv' with IDs of the best
# matching MRL items based on product & manufacturer keywords
RUN_MRL_MATCHING = True

# filter rows to only those determined to be RDT tests
# Keeps rows with any of the following in their PRODUCT DETAILS value:
# ANTIGEN, AG, ANTIBOD, IGG, IGM
RUN_RDT_FILTER = True

#
RUN_UMAIR = False

# FILTERS:
#   this is how you filter rows from the output. A row will be kept
#   if its column value contains ANY of the values provided for EVERY
#   filter, case insensitive. Enter multiple filters on the same column to
#   capture only rows that match multiple values.
#   For example, to filter to only rows whose "product details" column value
#   contains the word "test" and *EITHER* "covid" OR "sars", enter the
#   following filters:
#
#	{
# 		'col': 'product details',
# 		'contents': ['test']
# 	}, {
# 		'col': 'product details',
# 		'contents': ['sars', 'covid']
# 	}
#
# Define as many filters as you like.
# Will only run if RUN_CUSTOM_FILTERS above is set to True
FILTERS = [{
    'col': 'product details',
    'contents': ['SAR', 'COV', 'corona']
    # }, {
    #     'col': 'product details',
    #     'contents': ['test']
}]

# CLASSIFIERS:
# 	use these to label (ie "classify") rows based on containing
# 	a certain value in a certain column. rows that contain the
#  	matchingValue in their matchingCol will be given a value of
# 	labelValue in their (newly created) labelCol. For example,
# 	to add a new column "Test Type" and classify rows as
# 	"Manual PCR" or "Ag RDT" depending on their "product details"
# 	column value, you would use the following classifiers:
#
# {
#     'matchingCol': 'product details',
#     'matchingValue': 'pcr',
#     'labelCol': 'Test Type',
#     'labelValue': 'Manual PCR',
# },
# {
#     'matchingCol': 'product details',
#     'matchingValue': 'Panbio',
#     'labelCol': 'Test Type',
#     'labelValue': 'Ag RDT',
# }
#
# Define as many classifiers as you like.
# Will only run if RUN_CLASSIFIERS above is set to True
CLASSIFIERS = [
    # {
    #     'matchingCol': F_TA_EXP_NAME,
    #     'matchingValue': 'Abbot',
    #     'labelCol': 'Test Type',
    #     'labelValue': 'Ag RDT',
    # },
]

#UMAIR'S PARAMS:
##################SET FILE NAMES#################################
#Trade Atlas File Requires extension xlsx
Trade_Atlas = 'Indonesia 2021-Including Exchange Rates WA V2_Updated with Verification.xlsx'

#Sheet doesn't require an extension
Trade_Atlas_Sheet = 'Indonesia 2021-Indonesia 2021V1'

#MRL requires the extension
# MRL_FILE = 'Master reference list V2 CD.xlsx'

#Sheet doesn't require an extension
# MRL_Sheet = 'Master Sheet 3.0-Deduped'

# Exchange_Rate = 'Indonesia 2021-Including Exchange Rates WA V2_Updated with Verification.xlsx'
# #Requires Extension xlsx

#Sheet doesn't require an extension
Exhchange_Rate_Sheet = 'Exchange rates'

###################
###################
###################
################### CODE (DO NOT EDIT PAST THIS POINT)
###################
###################

INPUT_DIR = 'inputs'
OUTPUT_DIR = 'outputs'

COUNTRY_PATH = INPUT_DIR + '/' + COUNTRY
OUTPUT_PATH_FRAG = f'{OUTPUT_DIR}/{COUNTRY}-{NAME}'
OUTPUT_PATH = f'{OUTPUT_PATH_FRAG}.csv'
OUTPUT_STATS_PATH = f'{OUTPUT_PATH_FRAG}-stats.json'

# converts columns to lower case - leave as True
CONVERT_CASE = True

start_time = datetime.now()
results = []
rows_dropped = 0
for path in os.listdir(COUNTRY_PATH):
    # source = pd.read_excel('inputs/' + path) eg inputs/pakistan/p.csv
    abs_path = COUNTRY_PATH + '/' + path
    print(abs_path)
    df = read_spreadsheet(abs_path, SHEET_NAME)
    # df = read_spreadsheet('outputs/pakistan 2021-version7.csv') # UNDO just for testing
    print(abs_path)
    print(df.head)
    size_init = len(df)

    df['source_data_row'] = np.arange(len(df)) + 1
    df['source_file_name'] = path

    if CONVERT_CASE:
        df.columns = df.columns.str.lower()

    if RUN_CUSTOM_FILTERS:
        df = CUSTOM_FILTERS_MAIN(df, FILTERS)

    if RUN_CLASSIFIERS:
        df = CLASSIFIERS_MAIN(df, CLASSIFIERS)

    size_end = len(df)
    size_lost = size_init - size_end
    rows_dropped = rows_dropped + size_lost
    print("___________ADDING DATA__________")
    print(df.head)
    results.append(df)

result_df = pd.concat(results)
print("___________ALL RESULTS__________")
# print(results)
print(result_df.head(25))
result_df.to_csv(OUTPUT_PATH, index=False)
print(f'wrote {OUTPUT_PATH}')

do_stats(SHEET_NAME, COUNTRY_PATH, OUTPUT_STATS_PATH, len(result_df),
         rows_dropped, RUN_CUSTOM_FILTERS, FILTERS, RUN_CLASSIFIERS,
         CLASSIFIERS)


if RUN_MRL_MATCHING:
	print_update(start_time, 'Begin MRL Matching')
	result_df = MRL_MATCHING_MAIN(result_df, MRL_CSV)
	result_df.to_csv(f'{OUTPUT_PATH_FRAG}-mrl-matched.csv')

if RUN_UMAIR:
	print_update(start_time, 'Begin Umair')
	UMAIR_MAIN

# exec(open("filter.py").read())
# exec(open("scratch_kw.py").read())
