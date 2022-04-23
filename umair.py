#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
from datetime import datetime
# pd.options.mode.chained_assignment = None
# pd.options.display.float_format = '{:,.2f}'.format


def UMAIR_MAIN(
    df1,
	run_rdt_filter,
    mrl_csv,
	exchange_rates_csv,
	output_name,
    # Exchange_Rate_Sheet,
    # Trade_Atlas,
    # MRL_Sheet,
    # Exchange_Rate,
    # Trade_Atlas_Sheet,
):

    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("Start Time Cleaning =", current_time)

	# TODO: standardize (ie use upper or lower) throughout BP
    df1.columns = df1.columns.str.upper()
	
    #Reading the file
    # pd.set_option('display.max_colwidth', None)
    # print('Reading the Trade Atlas Indonesia File')
    # df = pd.read_excel(Trade_Atlas, sheet_name=Trade_Atlas_Sheet)

    # <b>Data cleaning </b>
    # - Removing starting and trailing spaces
    # - Removing the identified terms
    # - Removing punctuation
    # - Removing double spaces
    # - Adding Keywords as columns in the dataframe. These columns are used as indicators/boolean checks for the presence of keywords.

    # In[210]:

    # df1 = Data_Frame
    print(
        'Preparing Product Details Column for the extraction of number of tests'
    )
    #Adding the keywards to the pandas dataframe
    Keyword_list = [
        'T', 'TES', 'TEST', 'BOX', 'CASSETTES', 'RXN', 'RNX', 'REACTION',
        'KIT', 'PCS', 'PCE', 'STRIP'
    ]
    df1 = df1.reindex(columns=df1.columns.tolist() +
                      Keyword_list)  #Adding empty columns to the python list

    #PDC CLEANING
    df1['PDC'] = df1[
        'PRODUCT DETAILS']  #NEW COLUMN PDC (Product Details Cleaning) has the the product detail data in it now.

    #Removing starting and trailing spaces
    df1['PDC'] = df1['PDC'].str.strip()  #

    #Remove COVID-19 OR COVID 19 from the string
    df1['PDC'] = df1['PDC'].str.replace('COVID-19', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('COVID 19', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace(' COVID 19 ', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('COVID -19', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('COVID- 19', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('COVID TEST 19', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('QUANT 20', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('POCKIT', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('1KIT', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('SCNTH', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('SCNTL', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('DETECTION KIT', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('EAR99', ' ', case=False)

    #Remove COV-2 related keywords from the string
    df1['PDC'] = df1['PDC'].str.replace('COV-2', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('COV 2', ' ', case=False)
    df1['PDC'] = df1['PDC'].str.replace('COV2', ' ', case=False)

    #Remove VAR-2 from the string
    df1['PDC'] = df1['PDC'].str.replace('VAR2', ' ',
                                        case=False)  #SOLVES THE ISSUE

    #Remove SARS COV 2 related keywords from the string
    df1['PDC'] = df1['PDC'].str.replace('SARS COV 2', ' ',
                                        case=False)  #SOLVES THE ISSUE
    df1['PDC'] = df1['PDC'].str.replace('SARS-COV-2', ' ',
                                        case=False)  #SOLVES THE ISSUE
    df1['PDC'] = df1['PDC'].str.replace('SARSCOV3', ' ',
                                        case=False)  #SOLVES THE ISSUE

    #Remove the punctuation and the brackets.
    df1['PDC'] = df1['PDC'].str.replace(r'[^\w\s]+', '')

    #Removing double spaces between the words
    df1['PDC'] = df1['PDC'].replace('\s+', ' ', regex=True)

    # <b> Checking presence of keywords in every row of product details </b>

    # In[211]:

    #Checking presence of keywords in every row of product details
    df1 = df1.reset_index()
    for x in range(0, len(df1['PDC'])):
        for y in range(0, len(Keyword_list)):
            if (Keyword_list[y] != 'T'):
                if (Keyword_list[y] in df1['PDC'][x]):
                    df1[Keyword_list[y]][x] = 1
                else:
                    df1[Keyword_list[y]][x] = 0

    # <b> Splitting the product detail column in to words </b>

    # In[212]:

    print(
        'Processing Product Details Column for the extraction of number of tests'
    )

    #Splitting the product detail column in to words
    df1['PDC_SPLIT'] = df1['PDC'].str.split()

    # <b> Checking the presence of T </b>

    # In[213]:

    #Checking the presence of T in the split words
    for x in range(0, len(df1['PDC'])):
        for y in range(0, len(df1['PDC_SPLIT'][x])):
            if (df1['PDC_SPLIT'][x][y] == 'T'):
                df1['T'][x] = 1

    # <b>Checking if the word contains a digit</b>

    # In[214]:

    def containsNumber(value):
        for character in value:
            if character.isdigit():
                return True
        return False

    # <b>Creating a column "words" that has words from the product detail split column containing digits or a combination of digits or characters.  </b>

    # In[215]:

    #Creating a column with an empty list
    df1['words'] = np.empty((len(df1), 0)).tolist()
    #Taking the values from the PDC split that has numbers only.
    for i in range(0, len(df1['PDC_SPLIT'])):
        for w in range(0, len(df1['PDC_SPLIT'][i])):

            if (containsNumber(df1['PDC_SPLIT'][i][w]) == True
                ):  #if conition if the word contains a digit
                df1['words'][i].append(
                    df1['PDC_SPLIT'][i]
                    [w])  #appending the list with words that have number in it

    # <b>A new column is generated called refined words. Words that gets in to this column meets the following conditions:</b> <br>
    # 1.There is a digit present and the number is than 2500 <br>
    # 2. The keyword is present with the number.
    #

    # In[216]:

    df1['refined_words'] = np.empty((len(df1), 0)).tolist()
    #selecting only the words that contain numbers
    for x in range(0, len(df1['words'])):
        for y in range(0, len(df1['words'][x])):
            if ((df1['words'][x][y].isdigit()
                 and int(df1['words'][x][y]) <= 2500) or
                ('T' in df1['words'][x][y]) or ('RXN' in df1['words'][x][y])
                    or ('PCE' in df1['words'][x][y])
                    or ('EA' in df1['words'][x][y])
                    or ('CASSE' in df1['words'][x][y])
                    or ('BOX' in df1['words'][x][y])
                    or ('PCS' in df1['words'][x][y])
                    or ('KIT' in df1['words'][x][y])
                    or ('TES' in df1['words'][x][y])
                    or ('STRIP' in df1['words'][x][y])):
                df1['refined_words'][x].append(df1['words'][x][y])

    # <b>A Column for Manual Verification</b>

    # In[217]:

    df1['REQUIRES_MANUAL_VERIFICATION'] = ''

    # <b>Following conditions are implemented in the code below: </b>
    # 1) if the refined words only contain the numbers then check the range of the numbers. If it is >=5 and <=2500 then we take it as valid test. <br>
    # 2) if the refine words column contain numbers only and all are equal, then we remove the duplicates and get one value only. <br>
    # 3) If the number of refined words column has one value and contains digit with characters then check if it has a keyword attached to it. If yes, then take that number. <Br>
    #

    # In[218]:

    import re
    df1['test_quantity'] = np.empty((len(df1), 0)).tolist()

    df1 = df1.fillna(0)
    for x in range(0, len(df1['refined_words'])):
        for y in range(0, len(df1['refined_words'][x])):
            res = all(
                map(str.isdigit, df1['refined_words'][x])
            )  #all the elements in the list are digit only- return true
            if (res == True and len(df1['refined_words'][x]) !=
                    0):  #checking that the list contain all the numbers only
                if (
                        int(df1['refined_words'][x][y]) >= 5
                        and int(df1['refined_words'][x][y]) <= 2500
                ):  #Sanity range taken to be greater than 5 and less than 2500
                    df1['test_quantity'][x].append(
                        re.sub("[^0-9]", "", df1['refined_words'][x][y]))
            result_equal = all(element == df1['refined_words'][x][0]
                               for element in df1['refined_words']
                               [x])  #if all the elements in the list are equal
            if (result_equal == True and len(df1['refined_words'][x]) > 1 and
                    res == True):  #only digits lists being handled uptil now
                df1['test_quantity'][x] = np.unique(
                    np.array(df1['refined_words']
                             [x])).tolist()  #converting to list back again

            #list contains only one value and that value is a number with characters
            elif (
                    len(df1['refined_words'][x]) == 1 and
                    int(re.sub("[^0-9]", "", df1['refined_words'][x][y])) > 5
                    and int(re.sub("[^0-9]", "", df1['refined_words'][x][y]))
                    and res == False
            ):  #if length is one then remove the characters and insert the digits

                if (('T' in df1['refined_words'][x][y])):
                    count_t = df1['refined_words'][x][y].count('T')
                    if (count_t == 1 or count_t == 2 or count_t == 3
                            or count_t == 4):
                        df1['T'][
                            x] = 1  #This T condition is just for the boolean check
                        df1['test_quantity'][x].append(
                            re.sub("[^0-9]", "", df1['refined_words'][x][y]))

                else:
                    df1['test_quantity'][x].append(
                        re.sub("[^0-9]", "", df1['refined_words'][x][y]))

            elif (
                    len(df1['refined_words'][x]) > 1 and res == False
            ):  #if any of the word contains the keyword then we need that value only.
                if ((('TE' in df1['refined_words'][x][y]) or
                     ('KIT' in df1['refined_words'][x][y]) or
                     ('RXN' in df1['refined_words'][x][y]) or
                     ('PCS' in df1['refined_words'][x][y]) or
                     ('PCE' in df1['refined_words'][x][y]) or
                     ('CASSE' in df1['refined_words'][x][y]) or
                     ('BOX' in df1['refined_words'][x][y]) or
                     ('RNX' in df1['refined_words'][x][y]) or
                     ('STRIP' in df1['refined_words'][x][y])) and
                    ((int(re.sub("[^0-9]", "", df1['refined_words'][x][y])) >=
                      5)
                     and int(re.sub("[^0-9]", "",
                                    df1['refined_words'][x][y])) <= 2500)):
                    if (int(re.sub("[^0-9]", "", df1['refined_words'][x][y]))
                            >= 5 and int(
                                re.sub("[^0-9]", "",
                                       df1['refined_words'][x][y])) <= 2500):
                        df1['test_quantity'][x].append(
                            re.sub("[^0-9]", "", df1['refined_words'][x][y]))

                elif (('T' in df1['refined_words'][x][y])):

                    count_t = df1['refined_words'][x][y].count('T')
                    if (
                            count_t == 1
                    ):  #not taking count t==2 because there are more than one words and it may cause confusion
                        if (int(
                                re.sub("[^0-9]", "",
                                       df1['refined_words'][x][y])) >= 5
                                and int(
                                    re.sub("[^0-9]", "",
                                           df1['refined_words'][x][y])) <=
                                2500):
                            df1['test_quantity'][x].append(
                                re.sub("[^0-9]", "",
                                       df1['refined_words'][x][y]))
                            df1['T'][x] = 1

    print('Product Details column processing completed')

    # <b> Boolean Checks / Indicators </b>

    # In[219]:

    print('Creating Boolean checks for the presence of Keywords')

    r = re.compile(
        r'([0-9]+X[0-9]+T+|[0-9]+\*[0-9]+T|[0-9]+\*[0-9]+ T|[0-9]+X[0-9]+ T+)'
    )  #Regex for identifying Multiplication values
    #Creating Keywords boolean checks.
    df1['test_quantity_final'] = np.empty((len(df1), 0)).tolist()
    df1['Auto_Data_Quality_index'] = ""
    boolean_counter = 0
    for x in range(0, len(df1['refined_words'])
                   ):  #can use any column just need to get the length
        for y in range(0, len(Keyword_list)):
            if (df1[Keyword_list[y]][x] == 1):
                boolean_counter = boolean_counter + 1

        if (boolean_counter >= 1 and len(df1['test_quantity'][x]) == 1):

            df1['test_quantity_final'][x] = int(df1['test_quantity'][x][0])
            df1['Auto_Data_Quality_index'][
                x] = 'Keyword and Value both are present'

        if (boolean_counter >= 1 and len(df1['test_quantity'][x]) > 1):
            df1['test_quantity_final'][x] = np.nan
            df1['Auto_Data_Quality_index'][
                x] = 'Keyword and Two Values are present'
            df1['REQUIRES_MANUAL_VERIFICATION'][x] = 1

        if (boolean_counter == 0):
            df1['test_quantity_final'][x] = 1
            df1['Auto_Data_Quality_index'][x] = 'No Keyword present'

        if (boolean_counter >= 1 and len(df1['test_quantity'][x]) == 0):
            df1['test_quantity_final'][x] = 1
            df1['Auto_Data_Quality_index'][x] = 'Keyword found but no value'
        #This condition shall stay in the last
        if (df1['test_quantity_final'][x] > 2500):
            df1['test_quantity_final'][x] = 1
        boolean_counter = 0

        if (r.search(df1['PRODUCT DETAILS'][x])):
            df1['test_quantity_final'][x] = np.nan
            df1['Auto_Data_Quality_index'][x] = 'Multiplication Values'
            df1['REQUIRES_MANUAL_VERIFICATION'][x] = 1

    print('Boolean checks created')
    print('Number of tests extracted from Product details')

    # In[221]:

    #Value counts for the Auto Data Quality Index
    df1['Auto_Data_Quality_index'].value_counts()
    print(df1['Auto_Data_Quality_index'].value_counts())
    print('Auto Data Quality index created')

	# TODO: only do the following if run_rdt_filter?
    df1['Test_Type'] = np.empty((len(df1), 0)).tolist()

    # In[225]:

    #a) Filter All product Details that have "Pcr" in it and Marks them as "Non-RDT". Mark them as "Last Data Quality Step" = 1
    #m) Filter Product Details with "CONT" and mark them as "Control Unit"
    #n) Filter Product Details with Text Filter Contains "QuantCO" and mark them as "Control Unit"
    #o) Filter Product Details with Text Filter Contains "QuantCA" and mark them as "Calibration Unit"

    print('Labelling Non RDT products')
    non_rdt = [
        'PCR', 'CONT', 'CAL', 'CTL', 'QUANTCO', 'QUANTCA', 'QUANT CA',
        'QUANT CO'
    ]

    for x in range(0, len(df1['PRODUCT DETAILS'])):
        for y in range(0, len(non_rdt)):
            if (non_rdt[y] in df1['PRODUCT DETAILS'][x]):
                df1['Test_Type'][x].append('Non-RDT')

        df1['Test_Type'][x] = np.unique(np.array(df1['Test_Type'][x])).tolist()

    # In[226]:

    # b) Filter All product Details that have "Antigen" in it and Marks them as "SARS-CoV-2 Antigen Rapid Diagnostic Tests" in the "Test Type" Column.
    # c) Filter All product Details that have " Ag ", "Ag " and " Ag" in it and Marks them as "SARS-CoV-2 Antigen Rapid Diagnostic Tests" in the "Test Type" Column.

    print('Labelling Antigen products')

    antigen = ["ANTIGEN", " AG ", "AG ", " AG"]

    #Performing the Boolean check
    for x in range(0, len(df1['PRODUCT DETAILS'])):
        for y in range(0, len(antigen)):
            if (antigen[y] in df1['PRODUCT DETAILS'][x]):
                df1['Test_Type'][x].append(
                    'SARS-CoV-2 Antigen Rapid Diagnostic Tests')

        df1['Test_Type'][x] = np.unique(np.array(df1['Test_Type'][x])).tolist()

    # In[227]:

    #Filter All product Details that have "antibod" in it and Marks them as "SARS-CoV-2 Antibody Rapid Diagnostic Tests" in the "Test Type" Column.<br>
    #Filter All product Details that have "igg" in it and Marks them as "SARS-CoV-2 Antibody Rapid Diagnostic Tests" in the "Test Type" Column.<br>
    #Filter All product Details that have "igm" in it and Marks them as "SARS-CoV-2 Antibody Rapid Diagnostic Tests" in the "Test Type" Column.<br>

    print('Labelling Antibody products')

    antibody = ['ANTIBOD', 'IGG', 'IGM']

    #Performing the Boolean check
    for x in range(0, len(df1['PRODUCT DETAILS'])):
        for y in range(0, len(antibody)):
            if (antibody[y] in df1['PRODUCT DETAILS'][x]):
                df1['Test_Type'][x].append(
                    'SARS-CoV-2 Antibody Rapid Diagnostic Tests')

        df1['Test_Type'][x] = np.unique(np.array(df1['Test_Type'][x])).tolist()

    # In[228]:

    #Filter "Blanks" in test types. We are not sure about these products.
    #Primarily we can assume that these are also Non-RDT, Non-PCR, Mark them as "Non-RDT, Non PCR" in the test Type

    print('Labelling Non RDT and Non PCR')

    for x in range(0, len(df1['Test_Type'])):
        if (len(df1['Test_Type'][x]) == 0):
            df1['Test_Type'][x].append('Non-RDT, Non PCR')

    # In[229]:

    #removing the list brackets
    df1['Test_Type'] = df1['Test_Type'].str[0]

    # In[230]:

    # <b>Missing</b> <br>
    # 1) Filter "Number of Tests/Box" column with "2*XXX" and Similar values and mark them as "Calibration + Test Kit" Put value in Manual Entry Number of tests/Box. For 2x100, put 100 (i.e. 100 tests and 100 Calibration unit)<br>
    # 2) Filter "Number of Tests/Box" column with "2*XXX" and Similar values and mark them as "Calibration + Test Kit" Put value in Manual Entry Number of tests/Box. For 2x100, put 100 (i.e. 100 tests and 100 Control unit)

    # # h) Now select "SARS-CoV-2 Antigen Rapid Diagnostic Tests" and "SARS-CoV-2 Antibody Rapid Diagnostic Tests" from Test Types. These are the only considerable products that require manual verification for data Quality Index. <BR>
    #
    #  ASK THIS: p) Filter with "MGM" in the "Quantity Unit" Column and Mark them as Non-RDT

    # # Converting the Price Value in to USD

    # In[245]:

    print('Filtering RDT tests')

    if run_rdt_filter:
        init_size = len(df1)
        df1 = df1[
	        (df1['Test_Type'] == 'SARS-CoV-2 Antigen Rapid Diagnostic Tests') |
	        (df1['Test_Type'] == 'SARS-CoV-2 Antibody Rapid Diagnostic Tests')]
        print('\nDropped ', init_size - len(df1), ' rows from RDT filter.\n')

    # In[262]:

    df1 = df1.reset_index()

    #Reading the exchange rate sheet
    print('Reading the Exchange Rate file')
    # er = pd.read_excel(Trade_Atlas, sheet_name=Exchange_Rate_Sheet)
    er = pd.read_csv(exchange_rates_csv)
    #er = er.iloc[:, 0:10]

    # In[246]:

    er.head(5)

    # In[247]:

    #Converting datetime to date
    df1['Date'] = pd.to_datetime(df1['ARRIVAL DATE'],format="%y/%m/%d").dt.date
    df1['Date'] = df1['Date'].astype('datetime64[ns]')
    # er['Date'] = pd.to_datetime(er['DATE'], format="%d/%m/%y").dt.date
    er['Date'] = er['Date'].astype('datetime64[ns]')
    # In[248]:


    # In[249]:

    df1 = df1.merge(er, on='Date', how='left')

    # In[250]:

    #CURRENCY CONVERSION

    print('Converting Import Value CIF to USD')
    df1["IMPORT_VALUE_CIF_USD"] = np.NaN
    df1['IMPORT VALUE CIF'] = df1['IMPORT VALUE CIF'].astype(float)

    for x in range(0, len(df1['IMPORT VALUE CIF'])):
        if (df1['CURRENCY'][x] == 'USD'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['USD'][x]

        elif (df1['CURRENCY'][x] == 'IDR'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['IDR'][x]

        elif (df1['CURRENCY'][x] == 'JPY'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['JPY'][x]

        elif (df1['CURRENCY'][x] == 'CNY'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['CNY'][x]

        elif (df1['CURRENCY'][x] == 'AUD'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['AUD'][x]

        elif (df1['CURRENCY'][x] == 'GBP'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['GBP'][x]

        elif (df1['CURRENCY'][x] == 'EUR'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['EUR'][x]

        elif (df1['CURRENCY'][x] == 'SGD'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['SGD'][x]

        elif (df1['CURRENCY'][x] == 'VND'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['VND'][x]
		
	elif (df1['CURRENCY'][x] == 'ZAR'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['ZAR'][x]
	
	elif (df1['CURRENCY'][x] == 'UGX'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['UGX'][x]
		
	elif (df1['CURRENCY'][x] == 'INR'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['INR'][x]
		
	elif (df1['CURRENCY'][x] == 'DKK'):
            df1['IMPORT_VALUE_CIF_USD'][
                x] = df1['IMPORT VALUE CIF'][x] * df1['DKK'][x]
		
		
        else:
            df1['IMPORT_VALUE_CIF_USD'][x] = 'unidentified currency'

    print('Processing Volume Calculations: ')

    for x in range(0,len(df1)):
	if (df1['QUANTITY'][x]==0):
		df1['QUANTITY'][x]=1


    df1['test_quantity_final'] = df1['test_quantity_final'].astype(float)
    df1['VOLUME1_PCE'] = df1['QUANTITY']
    df1['VOLUME2_BOX'] = df1['QUANTITY'] * df1['test_quantity_final']

    # In[255]:

    #PER UNIT GROSS WEIGHT

    print('PER UNIT GROSS WEIGHT - Volume1')
    print('PER UNIT GROSS WEIGHT - Volume2')

    #Divide the Gross Weight / Volume1
    df1['PER_PCE_GROSS_WEIGHT'] = df1['GROSS WEIGHT'] / df1['VOLUME1_PCE']
    #Divide the Gross Weight / Volume2

    df1['PER_BOX_GROSS_WEIGHT'] = df1['GROSS WEIGHT'] / df1['VOLUME2_BOX']

    # In[256]:

    #PER UNIT NET WEIGHT
    print('PER UNIT NET WEIGHT - Volume1')
    print('PER UNIT NET WEIGHT - Volume2')

    #Divide the NET Weight / Volume1
    df1['PER_PCE_NET_WEIGHT'] = df1['NET WEIGHT'] / df1['VOLUME1_PCE']

    #Divide the NET Weight / Volume2
    df1['PER_BOX_NET_WEIGHT'] = df1['NET WEIGHT'] / df1['VOLUME2_BOX']

    # In[257]:

    #7) PER UNIT PRICE
    print('PER UNIT PRICE - Volume1')
    print('PER UNIT PRICE - Volume2')

    #DIVIDE THE IMPORT VALUE CIF (CONVERTED TO USD) / VOLUME1
    df1['PER_PCE_UNIT_PRICE'] = df1['IMPORT_VALUE_CIF_USD'] / df1['VOLUME1_PCE']

    #DIVIDE THE IMPORT VALUE CIF (CONVERTED TO USD) / VOLUME2
    df1['PER_BOX_UNIT_PRICE'] = df1['IMPORT_VALUE_CIF_USD'] / df1['VOLUME2_BOX']

    # In[258]:

    #WEIGHT RANGES:
    #RANGE: 0.01 TO 0.03 - THIS IS THE NET WEIGHT

    print(
        'Creating Boolean checks for Net weight, Gross weight and Unit price - by Volume1 and Volume 2'
    )
    df1['NEW_QUANTITY_UNIT'] = np.empty((len(df1), 0)).tolist()

    df1['EQUAL_VOLUMES'] = ''
    df1['PCE_NET_WEIGHT_CHECK'] = 0
    df1['PCE_GROSS_WEIGHT_CHECK'] = 0

    df1['BOX_NET_WEIGHT_CHECK'] = 0
    df1['BOX_GROSS_WEIGHT_CHECK'] = 0

    df1['PCE_PRICE_CHECK'] = 0
    df1['BOX_PRICE_CHECK'] = 0

    counter = 0

    for x in range(0, len(df1)):
        if (df1['VOLUME1_PCE'][x] == df1['VOLUME2_BOX'][x]):
            df1['EQUAL_VOLUMES'][x] = 1
        else:
            df1['EQUAL_VOLUMES'][x] = 0

        if (df1['PER_PCE_NET_WEIGHT'][x] >= 0.01
                and df1['PER_PCE_NET_WEIGHT'][x] <= 0.03):
            df1['PCE_NET_WEIGHT_CHECK'][x] = '1'
            counter = counter + 1
            df1['NEW_QUANTITY_UNIT'][x].append('PCE')

        if (df1['PER_BOX_NET_WEIGHT'][x] >= 0.01
                and df1['PER_BOX_NET_WEIGHT'][x] <= 0.03):
            df1['BOX_NET_WEIGHT_CHECK'][x] = '1'
            counter = counter + 1
            df1['NEW_QUANTITY_UNIT'][x].append('BOX')

    #RANGE: 0.01 TO 0.1 - THIS IS FOR THE GROSS WEIGHT

        if (df1['PER_PCE_GROSS_WEIGHT'][x] >= 0.01
                and df1['PER_PCE_GROSS_WEIGHT'][x] <= 0.1):
            df1['PCE_GROSS_WEIGHT_CHECK'][x] = '1'
            counter = counter + 1
            df1['NEW_QUANTITY_UNIT'][x].append('PCE')

        if (df1['PER_BOX_GROSS_WEIGHT'][x] >= 0.01
                and df1['PER_BOX_GROSS_WEIGHT'][x] <= 0.1):
            df1['BOX_GROSS_WEIGHT_CHECK'][x] = '1'
            counter = counter + 1
            df1['NEW_QUANTITY_UNIT'][x].append('BOX')

    #WHATEVER IS THE MAJORITY THAT WILL BE THE QUANTITY UNIT

    #PRICE CHECK - 0.7 TO 12 USD

        if (df1['PER_PCE_UNIT_PRICE'][x] >= 0.7
                and df1['PER_PCE_UNIT_PRICE'][x] <= 12):
            df1['PCE_PRICE_CHECK'][x] = '1'
            counter = counter + 1
            df1['NEW_QUANTITY_UNIT'][x].append('PCE')

        if (df1['PER_BOX_UNIT_PRICE'][x] >= 0.7
                and df1['PER_BOX_UNIT_PRICE'][x] <= 12):
            df1['BOX_PRICE_CHECK'][x] = '1'
            counter = counter + 1
            df1['NEW_QUANTITY_UNIT'][x].append('BOX')

        counter = 0

    # In[259]:

    df1['NEW_QUANTITY_UNIT'].tail(5)

    # # DATA QUALITY INDEX

    # <b>When the Volume 1 equals Volume 2 </b>
    #

    # In[260]:

    print('Assigning correct quantity unit - PCE/BOX')
    df1['DQI'] = np.nan
    df1['QUANTITY_UNIT_FINAL'] = np.nan

    df1['PCE_NET_WEIGHT_CHECK'] = df1['PCE_NET_WEIGHT_CHECK'].astype(float)
    df1['PCE_GROSS_WEIGHT_CHECK'] = df1['PCE_GROSS_WEIGHT_CHECK'].astype(float)
    df1['PCE_PRICE_CHECK'] = df1['PCE_PRICE_CHECK'].astype(float)

    df1['PCE_COUNT_IGNORE'] = 0

    for x in range(0, len(df1['EQUAL_VOLUMES'])):
        if (df1['EQUAL_VOLUMES'][x] == 1):
            df1['PCE_COUNT_IGNORE'][x] = df1['PCE_NET_WEIGHT_CHECK'][x] + df1[
                'PCE_NET_WEIGHT_CHECK'][x] + df1['PCE_PRICE_CHECK'][x]

            # print('EQUAL VOLUME: ',df1['EQUAL_VOLUMES'][x])
            # print('net: ',df1['PCE_NET_WEIGHT_CHECK'][x])
            # print('gross: ',df1['PCE_GROSS_WEIGHT_CHECK'][x])
            # print('price',df1['PCE_PRICE_CHECK'][x])
            df1['DQI'][x] = df1['PCE_NET_WEIGHT_CHECK'][x] + df1[
                'PCE_GROSS_WEIGHT_CHECK'][x] + df1['PCE_PRICE_CHECK'][x]
            # print('dqi: ',df1['DQI'][x])
            if (df1['DQI'][x] != 0):
                df1['QUANTITY_UNIT_FINAL'][x] = 'PCE'
            elif (df1['DQI'][x] == 0):
                df1['DQI'][x] = 0
                df1['QUANTITY_UNIT_FINAL'][x] = ''
                df1['REQUIRES_MANUAL_VERIFICATION'][x] = 1

    #df1['DQI'].head(5)

    df1['BOX_COUNT_IGNORE'] = 0
    df1['BOX_NET_WEIGHT_CHECK'] = df1['BOX_NET_WEIGHT_CHECK'].astype(float)
    df1['BOX_GROSS_WEIGHT_CHECK'] = df1['BOX_GROSS_WEIGHT_CHECK'].astype(float)
    df1['BOX_PRICE_CHECK'] = df1['BOX_PRICE_CHECK'].astype(float)
    df1['PCE_NET_WEIGHT_CHECK'] = df1['PCE_NET_WEIGHT_CHECK'].astype(float)
    df1['PCE_GROSS_WEIGHT_CHECK'] = df1['PCE_GROSS_WEIGHT_CHECK'].astype(float)
    df1['PCE_PRICE_CHECK'] = df1['PCE_PRICE_CHECK'].astype(float)

    #print(df1['BOX_NET_WEIGHT_CHECK'].dtype)
    #print(df1['PCE_NET_WEIGHT_CHECK'].dtype)
    #print(df1['PCE_PRICE_CHECK'].dtype)

    for x in range(0, len(df1['EQUAL_VOLUMES'])):
        if (df1['EQUAL_VOLUMES'][x] == 0):
            df1['PCE_COUNT_IGNORE'][x] = df1['PCE_NET_WEIGHT_CHECK'][x] + df1[
                'PCE_NET_WEIGHT_CHECK'][x] + df1['PCE_PRICE_CHECK'][x]

            df1['BOX_COUNT_IGNORE'][x] = df1['BOX_NET_WEIGHT_CHECK'][x] + df1[
                'BOX_GROSS_WEIGHT_CHECK'][x] + df1['BOX_PRICE_CHECK'][x]

            if (df1['PCE_COUNT_IGNORE'][x] > df1['BOX_COUNT_IGNORE'][x]):
                df1['DQI'][x] = df1['PCE_COUNT_IGNORE'][x]
                df1['QUANTITY_UNIT_FINAL'][x] = 'PCE'

            elif (df1['BOX_COUNT_IGNORE'][x] > df1['PCE_COUNT_IGNORE'][x]):
                df1['DQI'][x] = df1['BOX_COUNT_IGNORE'][x]
                df1['QUANTITY_UNIT_FINAL'][x] = 'BOX'

            elif (df1['PCE_COUNT_IGNORE'][x] == df1['BOX_COUNT_IGNORE'][x]):
                df1['DQI'][x] = 0
                df1['QUANTITY_UNIT_FINAL'][x] = ''
                df1['REQUIRES_MANUAL_VERIFICATION'][x] = 1

    #NEED THE ADDITION OF MRL HERE...

    # Based on this thought process, the proposed scale for Data Quality Index could be: <br>
    # 100%- columns of the product import transaction were logical and the price pertest or box was cross-checked against MRPL (maintaining the rows you’ve already marked as 100%) <br>
    # 75%- columns of the product import transaction were logical and the calculations made sense. We’re highly confident in this data but pricing info on MRPL was not available. <br>
    # 50% - columns of the product import transaction were generally logical but 1 field (aka column) didn’t make sense and therefore decreases our confidence in the validity of the TA transaction row <br>
    # 25%- columns of the product import transaction were somewhat logical, but had 2 fields (columns) that didn’t make sense so we really aren’t all that confident about the validity of the transaction row <br>
    # 0%- Columns of the product import transaction had 3 or more fields that didn’t make sense so we aren’t confident in the transaction row <br>

    # In[147]:

    df1['DQI'].head(5)

    # # Filtration of RDT AND NON RDT

    # Now select "SARS-CoV-2 Antigen Rapid Diagnostic Tests" and "SARS-CoV-2 Antibody Rapid Diagnostic Tests" from Test Types

    # In[261]:

    #Filteration code was previously here..

    # # SAVING THE FILE

    # In[42]:

    #df1.to_csv('Accuracy_Number_Of_Test2.csv', index=False)

    # In[43]:

    #r = re.compile(r'([0-9]+X[0-9]+T+|[0-9]+\*[0-9]+T|[0-9]+\*[0-9]+ T|[0-9]+X[0-9]+ T+)')
    #ANSWER=r.search('YHLO IFLASH SARS-COV-2 IGM DUS,KIT 2*50 TES')
    #if(ANSWER):
    #    print('yes')

    # In[44]:

    #using regex to identify Values like 2*50 and 2X50
    #r = re.compile(r'([0-9]+X[0-9]+|[0-9]+\*[0-9])')

    #for x in range(0,len(df1)):
    #    if(r.search(df1['PRODUCT DETAILS'][x])):
    #        print('True - Index: ',x)

    # # REFERENCE TO MRL

    #READ THE MRL FILE
    print('Reading MRL File')
    mrl = pd.read_csv(mrl_csv, skiprows=1)
    # mrl = pd.read_excel(MRL_FILE, sheet_name=MRL_Sheet, header=1)
    #mrl.head(5)
    #list(mrl)

    # In[46]:

    #df1_mrl = pd.merge(df1, mrl, left_on='PRODUCT DETAILS',right_on='Product Name\n(IVD product)',how='left')

    # In[47]:

    #df1_mrl['Product Name\n(IVD product)'].unique()

    # In[48]:

    #for x in range(0,len(df1_mrl)):
    #    if(df1_mrl['PRODUCT DETAILS'][x]==df1_mrl['Product Name\n(IVD product)'][x]):
    #        df1_mrl['UNIQUE_ID'][x]=df1_mrl['Unique Identifier'][x]

    # In[49]:

    #df1_mrl['UNIQUE_ID'].unique()

    # # Cleaning the PRODUCT DETAILS FOR MATCHING

    # In[264]:

    print('Preparing product details in MRL for matching')
    df1['PDC_NEW_DF'] = df1['PRODUCT DETAILS']

    # In[267]:

    df1['PDC_NEW_DF'] = df1['PDC_NEW_DF'].str.strip()
    df1['PDC_NEW_DF'] = df1['PDC_NEW_DF'].str.replace(r'[^\w\s]+', '')
    #Removing double spaces between the words
    df1['PDC_NEW_DF'] = df1['PDC_NEW_DF'].replace('\s+', ' ', regex=True)
    df1['PDC_NEW_DF'] = df1['PDC_NEW_DF'].str.upper()

    # # Cleaning the Product Name\n(IVD product FROM MRL FOR MATCHING
    #

    # In[268]:

    mrl['PDC_NEW_MRL'] = mrl['Product Name\n(IVD product)']

    # In[269]:

    mrl['PDC_NEW_MRL'] = mrl['PDC_NEW_MRL'].str.strip()
    mrl['PDC_NEW_MRL'] = mrl['PDC_NEW_MRL'].str.replace(r'[^\w\s]+', '')
    #Removing double spaces between the words
    mrl['PDC_NEW_MRL'] = mrl['PDC_NEW_MRL'].replace('\s+', ' ', regex=True)
    mrl['PDC_NEW_MRL'] = mrl['PDC_NEW_MRL'].str.upper()

    # In[271]:

    # https://www.statology.org/fuzzy-matching-pandas/

    print(
        'Creating a column with close matches between product details in Trade Atlas and MRL.\nThis step shall take a while. Please be patient.'
    )
    import difflib

    from difflib import SequenceMatcher

    mrl['product_match'] = mrl['PDC_NEW_MRL']

    #convert product_name_mrl in mrl to product name it most closely matches in df1

    mrl['PDC_NEW_MRL'] = mrl['PDC_NEW_MRL'].apply(lambda x: (
        difflib.get_close_matches(x, df1['PDC_NEW_DF'])[:1] or [None])[0])
    #df2['Unit'] = df2['Unit'].apply(lambda x: (difflib.get_close_matches(x, df1['Unit'])[:1] or [None])[0])

    #https://stackoverflow.com/questions/36557722/python-pandas-difflib-throws-list-index-out-of-range-error

    #convert team name in df2 to team name it most closely matches in df1
    print('Matches completed')

    # In[272]:

    mrl['PDC_NEW_MRL']

    #merge the DataFrames into one
    #new = df1.merge(mrl)
    #view final DataFrame
    #print(new)

    # In[304]:

    len(df1)

    # In[161]:

    #Creating a key in df1
    df1['MERGE_KEY'] = ''

    for x in range(0, len(df1)):
        df1['MERGE_KEY'][x] = x

    # In[58]:

    #df1.to_csv('check4.csv', index=False)

    # In[162]:

    df1_mrl = pd.merge(df1,
                       mrl,
                       left_on='PDC_NEW_DF',
                       right_on='PDC_NEW_MRL',
                       how='left')

    # In[60]:

    #df1_mrl[['PDC_NEW_MRL', 'PDC_NEW_DF']].tail(5)

    # In[163]:

    df1_mrl['PDC_NEW_DF'] = df1_mrl['PDC_NEW_DF'].astype(str)
    df1_mrl['PDC_NEW_MRL'] = df1_mrl['PDC_NEW_MRL'].astype(str)
    df1_mrl['product_match'] = df1_mrl['product_match'].astype(str)

    # In[273]:

    print(
        'Analyzing the match percentage between Product detail (Trade Atlas) and Product Details (MRL)...'
    )
    from difflib import SequenceMatcher
    #df1['MATCH'] = np.empty((len(df1), 0)).tolist()
    df1_mrl['MATCH_PERCENT'] = ''
    for x in range(0, len(df1_mrl)):
        df1_mrl['MATCH_PERCENT'][x] = SequenceMatcher(
            None, df1_mrl['PDC_NEW_DF'][x],
            df1_mrl['product_match'][x]).ratio()

    grouped_df = df1_mrl.groupby(['MERGE_KEY'])['MATCH_PERCENT'].max(
    ).reset_index()  #finding the index and maximum value

    grouped_df = pd.merge(df1_mrl,
                          grouped_df,
                          on=['MERGE_KEY',
                              'MATCH_PERCENT'])  #By Default it is inner join.

    print('Creating MRL Boolean Check')
    grouped_df['MRL_CHECK'] = 0
    for x in range(0, len(grouped_df)):
        if (grouped_df['MATCH_PERCENT'][x] >= 0.70):
            grouped_df['MRL_CHECK'][x] = 1
        else:
            grouped_df['MRL_CHECK'][x] = 0

    # In[70]:

    #Now these are not duplicates. It is possible that a product in the trade atlas matches with two products in the MRL with the same
    #Match percent

    print('Analyzing the Data Quality Index')
    for x in range(0, len(grouped_df)):
        if (grouped_df['QUANTITY_UNIT_FINAL'][x] == 'PCE'):
            grouped_df['DQI'][x] = grouped_df['PCE_NET_WEIGHT_CHECK'][
                x] + grouped_df['PCE_GROSS_WEIGHT_CHECK'][x] + grouped_df[
                    'PCE_PRICE_CHECK'][x] + grouped_df['MRL_CHECK'][x]
        elif (grouped_df['QUANTITY_UNIT_FINAL'][x] == 'BOX'):
            grouped_df['DQI'][x] = grouped_df['BOX_NET_WEIGHT_CHECK'][
                x] + grouped_df['BOX_GROSS_WEIGHT_CHECK'][x] + grouped_df[
                    'BOX_PRICE_CHECK'][x] + grouped_df['MRL_CHECK'][x]
        elif (grouped_df['QUANTITY_UNIT_FINAL'][x] == ''):
            grouped_df['DQI'][x] = grouped_df['MRL_CHECK'][x]

    grouped_df['DQI_FINAL'] = ''

    for x in range(0, len(grouped_df)):
        if (grouped_df['DQI'][x] == 0):
            grouped_df['DQI_FINAL'][x] = '0'
        elif (grouped_df['DQI'][x] == 1):
            grouped_df['DQI_FINAL'][x] = '25'
        elif (grouped_df['DQI'][x] == 2):
            grouped_df['DQI_FINAL'][x] = '50'
        elif (grouped_df['DQI'][x] == 3):
            grouped_df['DQI_FINAL'][x] = '75'
        elif (grouped_df['DQI'][x] == 4):
            grouped_df['DQI_FINAL'][x] = '100'

    print('Pulling MRL Unique Number')
    grouped_df['UNIQUE_ID_PULL'] = ''
    for x in range(0, len(grouped_df)):
        if (grouped_df['MRL_CHECK'][x] == 1):
            grouped_df['UNIQUE_ID_PULL'][x] = grouped_df['Unique Identifier'][
                x]

    print(
        'Boolean check for Unit price match between MRL Unit Price and calculated Unit price'
    )

    grouped_df['UNIT_PRICE_MATCH'] = ''
    for x in range(0, len(grouped_df)):
        if (grouped_df['QUANTITY_UNIT_FINAL'][x] == 'PCE'):
            if ((grouped_df['PER_PCE_UNIT_PRICE'][x]
                 == grouped_df['Global Fund-Reference price per pack EXW, USD']
                 [x])
                    |
                (grouped_df['PER_PCE_UNIT_PRICE'][x] ==
                 grouped_df['ADP- Indicative purchase pricing (per test)'][x])
                    | (grouped_df['PER_PCE_UNIT_PRICE'][x] == grouped_df[
                        'Global Fund- Reference price per test EXW, USD'][x]) |
                (grouped_df['PER_PCE_UNIT_PRICE'][x] == grouped_df[
                    'Consolidated price per test (Global Fund- Reference price per test + ADP- Indicative purchase pricing (per test)']
                 [x])):
                grouped_df['UNIT_PRICE_MATCH'][x] = 1

        if (grouped_df['QUANTITY_UNIT_FINAL'][x] == 'BOX'):
            if ((grouped_df['PER_BOX_UNIT_PRICE'][x]
                 == grouped_df['Global Fund-Reference price per pack EXW, USD']
                 [x])
                    |
                (grouped_df['PER_BOX_UNIT_PRICE'][x] ==
                 grouped_df['ADP- Indicative purchase pricing (per test)'][x])
                    | (grouped_df['PER_BOX_UNIT_PRICE'][x] == grouped_df[
                        'Global Fund- Reference price per test EXW, USD'][x]) |
                (grouped_df['PER_BOX_UNIT_PRICE'][x] == grouped_df[
                    'Consolidated price per test (Global Fund- Reference price per test + ADP- Indicative purchase pricing (per test)']
                 [x])):
                grouped_df['UNIT_PRICE_MATCH'][x] = 1

    print(
        ' Performing Boolean check for Number of tests match between MRL and Trade Atlas '
    )

    r = re.compile(
        r'([0-9]+X[0-9]+T+|[0-9]+\*[0-9]+T|[0-9]+\*[0-9]+ T|[0-9]+X[0-9]+ T+)')
    grouped_df['REFERENCE_DETAIL_CLEAN'] = ''
    grouped_df['REFERENCE_DETAIL_CLEAN'] = grouped_df[
        'REFERENCE_DETAIL_CLEAN'].astype(str)
    grouped_df['Reference detail'] = grouped_df['Reference detail'].astype(str)
    grouped_df['REFERENCE_DETAIL_MATCH'] = ''

    for x in range(0, len(grouped_df)):
        if (r.search(grouped_df['Reference detail'][x])):
            grouped_df['REFERENCE_DETAIL_CLEAN'][
                x] = ''  #find all gets the number as it is
        else:
            grouped_df['REFERENCE_DETAIL_CLEAN'][x] = re.sub(
                "[^0-9]", "", grouped_df['Reference detail'][x])

    grouped_df['REFERENCE_DETAIL_CLEAN'] = grouped_df[
        'REFERENCE_DETAIL_CLEAN'].replace('', np.nan)

    #Compare the quantity with the extracted number of test.
    #if the quantity is equal then Reference Detail Match = 1
    grouped_df['REFERENCE_DETAIL_CLEAN'] = grouped_df[
        'REFERENCE_DETAIL_CLEAN'].astype(float)
    #matching reference detail clean with the the test quantity final..
    for x in range(0, len(grouped_df)):
        if (grouped_df['test_quantity_final'][x] ==
                grouped_df['REFERENCE_DETAIL_CLEAN'][x]):
            grouped_df['REFERENCE_DETAIL_MATCH'][x] = 1

        else:
            grouped_df['REFERENCE_DETAIL_MATCH'][x] = 0

    # In[297]:

    # # Removing duplicates

    # In[301]:

    print('Removing duplicates in the Trade Atlas and MRL product match')
    grouped_df = grouped_df.drop_duplicates(subset='MERGE_KEY').reset_index(
        drop=True)  #removing the duplicated IDS.

    print('Exporting file', output_name)
    grouped_df.to_csv(output_name, index=False)

    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print('completed')
    # print("Completed Time =", current_time)
