import json
import pandas as pd
import re
import sys, getopt
import argparse
from pprint import pprint
from urllib.request import urlopen as urlopen

def splitJson(input_file, url, sun, output_file_nouni, output_file_uni,json_file_out):
   
   if input_file != "":
       with open(input_file, 'r') as f:
           data = f.read()
   
   if url != "":
       print("Donwloading data from ", url)
       response = urlopen(url)
       data = response.read()
   
   #loading data into json dict
   dpm_dict = json.loads(data)
   
   users=dpm_dict['rows']
   
   #convert dict to dataframe
   df = pd.DataFrame(users)
   
   #filter by column mail not equalt to
   #results=df.loc[df['mail'] != '*@uniroma1.it']
   
   #try lamba function for filter
   print("Extracting json data from downladed file...") 
   nouniroma1 = df.apply(lambda row: row[~df['mail'].str.contains("@*uniroma1.it")])
   nostruct =  df.apply(lambda row: row[df['structure_name'].str.contains("NON ASSEGNATO")])
   
   if sun:
       print("sun is true, restrict only to @uniroma1.it")
       atuniroma1 = df.apply(lambda row: row[df['mail'].str.contains("@uniroma1.it")])
   else:
       print ("sun is false, include all @*uniroma1.it")
       atuniroma1 = df.apply(lambda row: row[df['mail'].str.contains("@*uniroma1.it")])
   
   uniroma1= atuniroma1.apply(lambda row: row[~atuniroma1['structure_name'].str.contains("NON ASSEGNATO")])
   
   nouniroma1=nouniroma1.append(nostruct)
   print("Saving extracted data to file...") 
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
   print("all done.")
   