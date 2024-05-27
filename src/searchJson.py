import json
import pandas as pd
import re
import sys, getopt
from pprint import pprint


def main(argv):
    with open('../example/people-2024-04-29.json', 'r') as f:
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
    
    results.to_excel(excel_writer='../results/export.xlsx', sheet_name='Nouniroma1')