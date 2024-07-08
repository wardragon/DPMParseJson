import json
import pandas as pd
import re
import sys, getopt
import argparse
from pprint import pprint
from collections import OrderedDict, defaultdict

input_file=''
output_file=''
parser = argparse.ArgumentParser(description="Argument parser for command line options")
parser.add_argument('-i','--input', nargs = '?', help = 'Input file to read values in json format', dest="inputFile", required = True)
parser.add_argument('-ono', '--outputno', nargs = '?', default = sys.stdout, help = 'Output file xlsx to write nouniroma1 to, default standard output', dest = "outputFileNo")
parser.add_argument('-o', '--output', nargs = '?', default = sys.stdout, help = 'Output file xlsx to write uniroma1 to, default standard output', dest = "outputFile")
parser.add_argument('-ojson', '--outputjson', nargs = '?', default = sys.stdout, help = 'Output file json to write uniroma1 to, default none', dest = "outputFileJson")
args = parser.parse_args()

input_file=args.inputFile
output_file_nouni=args.outputFileNo
output_file_uni=args.outputFile
json_file_out=args.outputFileJson

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

nouniroma1 = df.apply(lambda row: row[~df['mail'].str.contains("@*uniroma1.it")])
nostruct =  df.apply(lambda row: row[df['structure_name'].str.contains("NON ASSEGNATO")])
atuniroma1 = df.apply(lambda row: row[df['mail'].str.contains("@*uniroma1.it")])
uniroma1= atuniroma1.apply(lambda row: row[~atuniroma1['structure_name'].str.contains("NON ASSEGNATO")])

nouniroma1=nouniroma1.append(nostruct)

if output_file_nouni == sys.stdout or output_file_uni==sys.stdout:
    print("--- Elenco No Uniroma1 ----------------")
    pprint(nouniroma1)
    print("---------------------------------------")
    print("--- Elenco Uniroma1 ----------------")
    pprint(uniroma1)
    print("---------------------------------------")
else:
    nouniroma1.to_excel(excel_writer=output_file_nouni, sheet_name='No_uniroma1_email')
    uniroma1.to_excel(excel_writer=output_file_uni, sheet_name='Uniroma1_email')

    data = {"rows":uniroma1.to_dict('records')}

    if json_file_out != sys.stdout:
     with open(json_file_out, 'w') as json_file:
            #json_file.write(json.dumps(data.to_dict('records')))
            json_file.write(json.dumps(data))