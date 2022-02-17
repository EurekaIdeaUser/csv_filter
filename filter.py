import pandas as pd
import numpy as np
import os
import re

INPUT_DIR = 'inputs'
OUTPUT_DIR = 'outputs'

SET_MANUALLY = True

if SET_MANUALLY:
    country = "india"
    name = "xx"
    sheet_name = 'Trade Atlas Records'

    COUNTRY_PATH = INPUT_DIR + '/' + country
    OUTPUT_PATH_FRAG = f'{OUTPUT_DIR}/{country}-{name}'
    OUTPUT_PATH = f'{OUTPUT_PATH_FRAG}.csv'
    OUTPUT_STATS_PATH = f'{OUTPUT_PATH_FRAG}-stats.json'

    filters = [  # if multiple contents, column value can match any
        {
            'col': 'PRODUCT DETAILS',
            'contents': ['sars', 'covid']
        }, {
            'col': 'PRODUCT DETAILS',
            'contents': ['test']
        }
    ]
else:
    country = input('country name (must match inputs folder name): ')
    sheet_name = input('provide the sheet name of the data tab for any xslx input files (eg "Trade Atlas Records": ')

    name = input(
        'identifier for the output file name (for your own use, can be left blank): '
    )

    COUNTRY_PATH = INPUT_DIR + '/' + country
    OUTPUT_PATH_FRAG = f'{OUTPUT_DIR}/{country}-{name}'
    OUTPUT_PATH = f'{OUTPUT_PATH_FRAG}.csv'
    OUTPUT_STATS_PATH = f'{OUTPUT_PATH_FRAG}-stats.json'

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

    filterCol = 'x'
    filterContents = ''
    while filterCol:
        filterCol = input('col name: ')
        if filterCol:
            filterContents = input('values, separated by commas: ')
            filters.append({
                'col': filterCol,
                'contents': filterContents.split(',')
            })

    print('_____________________________________________\n')
    print('data will be output to: ' + OUTPUT_PATH)
    print('with a stats file at: ' + OUTPUT_STATS_PATH)
    print('filters: ', filters)
    input("Hit enter to begin.")

results = []
rows_dropped = 0
for path in os.listdir(COUNTRY_PATH):
    # source = pd.read_excel('inputs/' + path)
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

    for filter in filters:
        # print(filter)
        # print(filter['col'])
        # df = df[filter['col']].str.contains(filter['contents'])
        # pred = False
        if filter['col'] in df.columns:
            # be sure filter['contents'] is a list? or don't use the regex approach
            wilded = ['.*' + c for c in filter['contents']]
            r = re.compile("|".join(wilded), re.IGNORECASE)
            df = df[df[filter['col']].str.contains(pat=r, regex=True, na=False)]

        else:  # erase df if it doesn't contain filtered column
            df = pd.DataFrame()
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
stats = {
    'rows_dropped': rows_dropped,
    'output_rows': len(result),
    'filters': f_strings
}
stats_df = pd.DataFrame(data=stats, index=[0], sheet_name=sheet_name)
stats_df.to_json(OUTPUT_STATS_PATH, 'records')
print(f'wrote {OUTPUT_STATS_PATH}')
print('DONE')
