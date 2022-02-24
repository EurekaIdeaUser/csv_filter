import pandas as pd
import numpy as np
import os
import re

df = pd.read_csv('inputs/test/p.csv')

df.columns= df.columns.str.lower()
print(df.columns)

# classifier = {
# 			'matchingCol': 'product details',
# 			'matchingValue': 'pCr',
# 			'labelCol': 'Test Type',
# 			'labelValue': 'Ag RDT',
# 		}
classifiers = [
	# {
	# 	'matchingCol': 'product details',
	# 	'matchingValue': 'text indicating Ag RDT',
	# 	'labelCol': 'Test Type',
	# 	'labelValue': 'Ag RDT',
	# },
	# {
	# 	'matchingCol': 'product details',
	# 	'matchingValue': 'text indicating Manual PCR',
	# 	'labelCol': 'Test Type',
	# 	'labelValue': 'Manual PCR',
	# }
	{
		'matchingCol': 'product details',
		'matchingValue': 'pcr',
		'labelCol': 'Test Type',
		'labelValue': 'Manual PCR',
	},
	{
		'matchingCol': 'product details',
		'matchingValue': 'Panbio Ag RDT',
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

for classifier in classifiers:
	# print(df[classifier['matchingCol']].str.lower().str.contains(classifier['matchingValue'].lower()))
	# print(df[classifier['matchingCol']].str.lower())
	print("-------")
	# print(df['bueoat'])
	
	# df.loc[df[classifier['matchingCol']].str.lower().str.contains(classifier['matchingValue'].lower()), classifier['labelCol']] = classifier['labelValue']
	
	
	# if df[classifier['matchingCol']].str.lower().str.contains(classifier['matchingValue'].lower()):
	# 	df[classifier['labelCol']] = classifier['labelValue']
	if classifier['labelCol'] not in df.columns:
		df[classifier['labelCol']] = ""
	df[classifier['labelCol']] = np.where(df[classifier['matchingCol']].str.lower().str.contains(classifier['matchingValue'].lower()), classifier['labelValue'], df[classifier['labelCol']])
	
print(df[classifier['labelCol']])
print(df.head)