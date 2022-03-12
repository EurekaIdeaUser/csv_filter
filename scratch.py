import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
from datetime import timedelta

ta = pd.read_csv('outputs/pakistan-xx.csv')

ta.columns= ta.columns.str.lower()
# print(ta.columns)

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

# for classifier in classifiers:
# 	print("-------")
# 	if classifier['labelCol'] not in ta.columns:
# 		ta[classifier['labelCol']] = ""
# 	ta[classifier['labelCol']] = np.where(ta[classifier['matchingCol']].str.lower().str.contains(classifier['matchingValue'].lower()), classifier['labelValue'], ta[classifier['labelCol']])
	
# print(ta[classifier['labelCol']])
# print(ta.head)

# mrl = pd.read_csv('mrl.csv', skiprows=1)[['manufacturer_keywords', 'product_keywords', 'Unique Identifier ']]
# .transform(lambda x: ','.join(x))

# dfx = pd.read_csv('mrl.csv', skiprows=1)[['manufacturer_keywords', 'product_keywords', 'Unique Identifier ']].groupby(['manufacturer_keywords','product_keywords'])['Unique Identifier '].transform(lambda x: ','.join(x))

# dfx = pd.read_csv('mrl.csv', skiprows=1)[['manufacturer_keywords', 'product_keywords', 'Unique Identifier ']].astype(str).groupby(['manufacturer_keywords','product_keywords'])['Unique Identifier ','manufacturer_keywords','product_keywords'].transform(lambda x: ','.join(x))

# dfx = pd.read_csv('mrl.csv', skiprows=1)[['manufacturer_keywords', 'product_keywords', 'Unique Identifier ']].astype(str).groupby(['manufacturer_keywords','product_keywords'])['Unique Identifier ','manufacturer_keywords','product_keywords'].agg(lambda x: ','.join(x)).drop_duplicates()

# dfx = pd.read_csv('mrl.csv', skiprows=1)[['manufacturer_keywords', 'product_keywords', 'Unique Identifier ']].astype(str).groupby(['manufacturer_keywords','product_keywords'])['Unique Identifier ', 'manufacturer_keywords','product_keywords'].agg({
# 	'Unique Identifier ': lambda x: ','.join(x), 
# 	'manufacturer_keywords': lambda x: ','.join(x), 
# 	'product_keywords': lambda x: ','.join(x),
# }).drop_duplicates()

# mrl = pd.read_csv('mrl.csv', skiprows=1)[['manufacturer_keywords', 'product_keywords', 'Unique Identifier ']].astype(str).groupby(['manufacturer_keywords','product_keywords'])['Unique Identifier ', 'manufacturer_keywords','product_keywords'].agg(lambda x: ','.join(x)).drop_duplicates()

def string_to_set(str): 
	s = set(str.lower().split(" "))
	if '' in s:
		s.remove('')
	# print(s, str)
	return s
	
def get_tag_match_ratio(tag_set, value_set):
  if len(tag_set) == 0:
	  # print(tag_set, "!")
	  return 0
  return len(list(tag_set&value_set)) / len(tag_set)

# def compare_row(ta_row, mrl):
# 	print("HI")

# get aggregated mrl
mrl = pd.read_csv('mrl.csv', skiprows=1)[['manufacturer_keywords', 'product_keywords', 'Unique Identifier ']].astype(str)
mrl = mrl.groupby(['manufacturer_keywords','product_keywords'])['Unique Identifier '].agg(lambda x: ','.join(x)).drop_duplicates()
mrl = mrl.reset_index()
# for index, row in mrl.iterrows():
    # print(row['Unique Identifier '], row['product_keywords'])

# print(mrl.head(100))
# mrl.to_csv('mrl-po.csv')


ta['Top P Match Ratio'] = 0
ta['Top P Match UIDs'] = ''
ta['Matching P Tags'] = ''
ta['Top M Match Ratio'] = 0
ta['Top M Match UIDs'] = ''
ta['Matching M Tags'] = ''
top_ratio_p_idx = ta.columns.get_loc('Top P Match Ratio')
top_match_p_idx = ta.columns.get_loc('Top P Match UIDs')
tags_p_idx = ta.columns.get_loc('Matching P Tags')
top_ratio_m_idx = ta.columns.get_loc('Top M Match Ratio')
top_match_m_idx = ta.columns.get_loc('Top M Match UIDs')
tags_m_idx = ta.columns.get_loc('Matching M Tags')

start_time = datetime.now()
print(start_time, 'beginning long tag comparison process...')
one_percent_done = round(len(ta)/100)
for i, ta_row in ta.iterrows():
	
	if i % one_percent_done == 0:
		print(i/one_percent_done, '% done')
	if i > 100:
		break
	top_match_p = ''
	top_ratio_p = 0
	tags_p = ''
	top_match_m = ''
	top_ratio_m = 0
	tags_m = ''
	# print(i, " of ", len(ta))

	p_val = ta_row['product details']
	p_val_set = string_to_set(p_val)
	m_val = ta_row['importer name']
	m_val_set = string_to_set(m_val)
	
	for j, mrl_row in mrl.iterrows():
		# if j % 50 > 0:
		# 	break
		# print(i, j, p_val)
		p_tags = mrl_row['product_keywords']
		p_tags_set = string_to_set(p_tags)
		p_ratio = get_tag_match_ratio(p_tags_set, p_val_set)
		if p_ratio > top_ratio_p:
			top_ratio_p = p_ratio
			top_match_p = mrl_row['Unique Identifier ']
			# add matching tags
			tags_p = ",".join(list(p_tags_set&p_val_set))
		elif (p_ratio > 0) & (p_ratio == top_ratio_p):
			top_match_p += " | " + mrl_row['Unique Identifier ']
			# add matching tags
			tags_p += " | " + ",".join(list(p_tags_set&p_val_set))
		
		m_tags = mrl_row['manufacturer_keywords']
		m_tags_set = string_to_set(m_tags)
		m_ratio = get_tag_match_ratio(m_tags_set, m_val_set)
		if m_ratio > top_ratio_m:
			top_ratio_m = m_ratio
			top_match_m = mrl_row['Unique Identifier ']
			# add matching tags
			tags_m = ",".join(list(m_tags_set&m_val_set))
		elif (m_ratio > 0) & (m_ratio == top_ratio_m):
			top_match_m += " | " + mrl_row['Unique Identifier ']
			# add matching tags
			tags_m += " | " + ",".join(list(m_tags_set&m_val_set))

	ta.iloc[i, top_match_m_idx] = top_match_m
	ta.iloc[i, top_ratio_m_idx] = top_ratio_m
	ta.iloc[i, tags_p_idx] = tags_p
	
	ta.iloc[i, top_match_p_idx] = top_match_p
	ta.iloc[i, top_ratio_p_idx] = top_ratio_p
	ta.iloc[i, tags_m_idx] = tags_m
	

end_time = datetime.now()
print(ta.head(100))
print(end_time - start_time)
ta.to_csv('ptest.csv')