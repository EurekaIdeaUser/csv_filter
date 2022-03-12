# Combine multiple csv/xslx files into a single csv, optionally filtering
# the rows by user-defined filters.
#
# INSTRUCTIONS:
#
# To run the tool, place any input files in the inputs folder on the left
# <----------------------------------------------------------------------
# These should be placed in a subfolder named with the country the data
# pertain to (eg "india"). Then click the green Run button above ↑↑↑↑↑↑↑↑
# It may take a minute to install the python packages used by the script.
# You will then be prompted to enter a few things in the console ------->
#
# country name: must match the name of the folder you created (eg "india")
#
# sheet name: must match the name of the tab containing the relevant data
#   in any xslx files provided (eg "Trade Atlas Records")
#
# file identifier: arbitrary, it will be tacked on to the output file name
#   (distinguishing it from others generated for the same country)
#
# filters: this is how you filter rows from the output. A row will be kept
#   if its column value contains ANY of the values provided for EVERY
#   filter, case insensitive. Enter multiple filters on the same column to
#   capture only rows that match multiple values.
#   For example, to filter down to only rows that contain in their DETAILS
#   column value the word "test" and *either* "covid" or "sars", enter the
#   following filters:
#
#  col name: details
#  values, separated by commas: test
#
#  col name: details
#  values, separated by commas: covid,sars
#
#  NOTE: once you have entered all filters, simply hit ENTER when the next
#   "col name" is requested to continue.
#
# Wait for the script to execute. This may take a few minutes depending on
# the size of the input files. You'll know the script has finished when it
# prints DONE to the screen. You'll then find your output files in the
# outputs folder (a csv with the resulting data, and a json file with some
# details like how many rows were dropped).
#
# NOTE: if you prefer, you can enter these values in filter.py in the
# _MANUAL SETTINGS SECTION_ this may be easier if you are running the
# script repeatedly, as you will not need to re-enter the values each time
#

# exec(open("filter.py").read())
