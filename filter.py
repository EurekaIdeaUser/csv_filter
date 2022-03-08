
import pandas as pd
import numpy as np
import os
import re

INPUT_DIR = 'inputs'
OUTPUT_DIR = 'outputs'

# _______________MANUAL SETTINGS SECTION_______________
SET_STATIC_PARAMS = False  # set to True if you prefer setting param values here
if SET_STATIC_PARAMS:
    # if SET_STATIC_PARAMS = True the script will use the values set here.
    convert_case = True
    country = "pakistan"
    name = "version3"
    sheet_name = 'Trade Atlas Records'

    filters = [  # if multiple contents, column value can match any
        {
            'col': 'product details',
            'contents': ['SAR', 'COV']
            # }, {
            #     'col': 'product details',
            #     'contents': ['test']
        }
    ]

    classifiers = [
        {
            'matchingCol': 'product details',
            'matchingValue': 'pcr',
            'labelCol': 'Test Type',
            'labelValue': 'Manual PCR',
        },
        {
            'matchingCol': 'product details',
            'matchingValue': 'Panbio',
            'labelCol': 'Test Type',
            'labelValue': 'Ag RDT',
        },
        {
            'matchingCol': 'importer name',
            'matchingValue': 'Abbot',
            'labelCol': 'Test Type',
            'labelValue': 'Ag RDT',
        },
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

    convert_case = input(
        'convert column names to lowercase (any response but "n" will be taken to mean "yes"): \n'
    ) != "n"

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
    print('will columns be made lower case: ', convert_case)
    print('filters: ', filters)
    print('classifiers: ', classifiers)
    input("Hit enter to begin.")



# BEGIN SCRIPT
results = []
rows_dropped = 0
for path in os.listdir(COUNTRY_PATH):
    # source = pd.read_excel('inputs/' + path) eg inputs/pakistan/p.csv
    abs_path = COUNTRY_PATH + '/' + path
    print(abs_path)
    if path.endswith('xlsx'):
        df = pd.read_excel(abs_path, sheet_name, engine='openpyxl')
# reinstall xlrd if we want to try to
# elif path.endswith('xls'):
# df = pd.read_excel(abs_path, engine='xlrd')
    elif path.endswith('csv'):
        df = pd.read_csv(abs_path)
    size_init = len(df)

    df['source_data_row'] = np.arange(len(df)) + 1
    df['source_file_name'] = path

    if convert_case:
        df.columns = df.columns.str.lower()

    for filter in filters:
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
            df = df[df[filter['col']].str.contains(pat=r, regex=True,
                                                   na=False)]

        else:  # erase df if it doesn't contain filtered column
            df = pd.DataFrame()

# https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
    for classifier in classifiers:
        if classifier['matchingCol'] in df.columns:
            if classifier['labelCol'] not in df.columns:
                df[classifier['labelCol']] = ""

            df[classifier['labelCol']] = np.where(
                df[classifier['matchingCol']].str.lower().str.contains( 
                    classifier['matchingValue'].lower()),
				# give it new label, otherwise preserve value (in case already labeled)
                classifier['labelValue'], df[classifier['labelCol']])

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
print('DONE')
