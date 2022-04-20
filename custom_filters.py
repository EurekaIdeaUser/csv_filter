import pandas as pd
import re

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

def CUSTOM_FILTERS_MAIN(df, filters):
	for filter in filters:
		print('pre filter: ', len(df))
		df = process_filter(filter, df)
		print('post filter: ', len(df))

	return df
