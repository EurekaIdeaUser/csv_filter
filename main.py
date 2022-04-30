from datetime import datetime
from helpers import do_stats, print_update, merge_inputs
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

# country name: must exactly match the name of the folder you created (eg "India 2021")
COUNTRY = "India 2021"
# COUNTRY = "t" # used for testing, use a real country like in the line above

# sheet name: must match the name of the tab containing the relevant data
# in any xslx files provided (eg "Trade Atlas Records")
SHEET_NAME = 'Trade Atlas Records'

# file identifier: arbitrary, it will be tacked on to the output file name
# (distinguishing it from others generated for the same country)
NAME = "v-15all"

# MRL file: must match the file name of a csv in the files to the left
# <------------- (one already exists as mrl.csv)
MRL_CSV = 'mrl.csv'

# exchange rates file: must match the file name of a csv in the files to the left
# <------------- (one already exists as exchange_rates.csv)
# for use in [Umair process] price calculation/validation
# should inculde the relevant dates and currencies of the Trade Atlas data transactions
EXCHANGE_RATES_CSV = 'Exchange_Rate_New.csv'

# RUN_ FLAGS - determine which code will execute, set each to True or False

# filter rows to only those which pass the custom FILTERS defined below
RUN_CUSTOM_FILTERS = True

# add output columns to label rows that match certain criteria
# define your CLASSIFIERS below
RUN_CLASSIFIERS = True

# adds an output ending in 'mrl-matched.csv' with IDs of the best
# matching MRL items based on product & manufacturer keywords
RUN_MRL_MATCHING = True

# filter rows to only those determined to be RDT tests
# Keeps only rows with any of the following in their PRODUCT DETAILS value:
# ANTIGEN, AG, ANTIBOD, IGG, IGM
RUN_RDT_FILTER = True



# Product Filtration (Antigen Rapid Diagnostic Tests,Antibody Rapid Diagnostic Tests)
# Number of test extraction from Product Details
# Import value conversion to USD
# Volume Calculations (Unit Net Weight, Unit Gross Weight, Unit Price)
# MRL Match (Including Match Percentage. Currently set to 70%)
# DQI (Unit Net Weight, Unit Gross Weight, Unit Price, MRL match found)
# Requires Manual Verification Column (Description Available in PPT)
RUN_UMAIR = True


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
OUTPUT_UMAIR_PATH = f'{OUTPUT_PATH_FRAG} umair.csv'
OUTPUT_STATS_PATH = f'{OUTPUT_PATH_FRAG}-stats.json'

# converts column names to lower case
# expected by BP code, leave as True
CONVERT_CASE = True

start_time = datetime.now()
input_df = merge_inputs(COUNTRY_PATH, SHEET_NAME)

if CONVERT_CASE:
	input_df.columns = input_df.columns.str.lower()

init_size = len(input_df)
if RUN_CUSTOM_FILTERS:
	print_update(start_time, 'Begin Custom Filters')
	input_df = CUSTOM_FILTERS_MAIN(input_df, FILTERS)
rows_dropped = init_size - len(input_df)

if RUN_CLASSIFIERS:
	print_update(start_time, 'Begin Classifiers')
	input_df = CLASSIFIERS_MAIN(input_df, CLASSIFIERS)

print("___________ALL RESULTS__________")
# print(results)
print(input_df.head(25))
input_df.to_csv(OUTPUT_PATH, index=False)
print(f'wrote {OUTPUT_PATH}')

do_stats(SHEET_NAME, COUNTRY_PATH, OUTPUT_STATS_PATH, len(input_df),
         rows_dropped, RUN_CUSTOM_FILTERS, FILTERS, RUN_CLASSIFIERS,
         CLASSIFIERS)

if RUN_MRL_MATCHING:
	print_update(start_time, 'Begin MRL Matching')
	input_df = MRL_MATCHING_MAIN(input_df, MRL_CSV)
	input_df.to_csv(f'{OUTPUT_PATH_FRAG}-mrl-matched.csv')

if RUN_UMAIR:
	print_update(start_time, 'Begin Umair')
	UMAIR_MAIN(input_df, RUN_RDT_FILTER, MRL_CSV, EXCHANGE_RATES_CSV, OUTPUT_UMAIR_PATH)

print_update(start_time, ' DONE. ')
# exec(open("filter.py").read())
# exec(open("scratch_kw.py").read())
