import pandas as pd
from datetime import datetime
import re
import os


def read_spreadsheet(path, sheet_name):
    if path.endswith('xlsx'):
        df = pd.read_excel(path, sheet_name, engine='openpyxl')


# reinstall xlrd if we want to try to
# elif path.endswith('xls'):
# df = pd.read_excel(path, engine='xlrd')
    elif path.endswith('csv'):
        df = pd.read_csv(path)
    return df


def trunc(stri, length_str):
    max_length = int(length_str) - 3
    # print(stri, max_length)
    if len(stri) > max_length:
        return stri[0:max_length] + '...'
    else:
        return stri


def print_preview_row(f_string, items):
    lengths = str.strip(re.sub('\D+', ' ', f_string)).split(' ')
    # print(items)
    tup_items = (trunc(item, lengths[items.index(item)]) for item in items)
    print(f_string.format(*tup_items))


def do_stats(sheet_name, country_path, stats_path, result_len, dropped_len,
             run_filters, filters, run_classifiers, classifiers):
    f_strings = ''
    if run_filters:
        f_strings = ' '.join(str(f) for f in filters)

    c_strings = ''
    if run_classifiers:
        c_strings = ' '.join(str(c) for c in classifiers)

    stats = {
        'output_rows': result_len,
        'rows_dropped': dropped_len,
        'input_files': (",").join(os.listdir(country_path)),
        'sheet_name': sheet_name,
        'filters': f_strings,
        'classifiers': c_strings,
    }
    stats_df = pd.DataFrame(data=stats, index=[0])
    stats_df.to_json(stats_path, 'records')
    print(f'wrote {stats_path}')


def print_update(start_time, message):
    now = datetime.now()
    print('\n\n', message, '\ntime elapsed: ', now - start_time)
