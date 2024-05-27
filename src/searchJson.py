import json
import pandas as pd
import re
import sys, getopt
import argparse
from pprint import pprint


input_file=''
output_file=''
parser = argparse.ArgumentParser(description="Argument parser for command line options")
parser.add_argument('-i','--input', nargs = '?', help = 'Input file to read values in json format', dest="inputFile", required = True)
parser.add_argument('-o', '--output', nargs = '?', default = sys.stdout, help = 'Output file to write to, defualt standard output', dest = "outputFile")
args = parser.parse_args()

input_file=args.inputFile
output_file=args.outputFile

with open(input_file, 'r') as f:
    data = f.read()

#loading data into json dict
dpm_dict = json.loads(data)

users=dpm_dict['rows']

#convert dict to dataframe
df = pd.DataFrame(users)

#filter by column mail not equalt to
#results=df.loc[df['mail'] != '*@uniroma1.it']

#try lamba function for filter

results = df.apply(lambda row: row[~df['mail'].str.contains("@*uniroma1.it")])

if output_file == sys.stdout:
    print(results)
else:
    results.to_excel(excel_writer=output_file, sheet_name='Nouniroma1')