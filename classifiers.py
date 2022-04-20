import numpy as np

def process_classifier(classifier, df):
	if classifier['matchingCol'] in df.columns:
            if classifier['labelCol'] not in df.columns:
                df[classifier['labelCol']] = ""

            df[classifier['labelCol']] = np.where(
                df[classifier['matchingCol']].str.lower().str.contains( 
                    classifier['matchingValue'].lower()),
				# give it new label, otherwise preserve value (in case already labeled)
                classifier['labelValue'], df[classifier['labelCol']])

def CLASSIFIERS_MAIN(df, classifiers):
	# https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
	for classifier in classifiers:
		process_classifier(classifier, df)

	return df