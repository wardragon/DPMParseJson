import json
import pandas as pd
import re
import sys, getopt
import argparse
from pprint import pprint
from urllib.request import urlopen as urlopen
from splitJson import *


input_file=''
output_file=''

parser = argparse.ArgumentParser(description="Argument parser for command line options")
parser.add_argument('-i','--input', nargs = '?', default="", help = 'Input file to read values in json format', dest="inputFile")
parser.add_argument('-u','--url', nargs = '?', default="",help = 'Input url where to read values in json format', dest="urlJson")
parser.add_argument('-ono', '--outputno', nargs = '?', default = sys.stdout, help = 'Output file xlsx to write nouniroma1 to, default standard output', dest = "outputFileNo")
parser.add_argument('-o', '--output', nargs = '?', default = sys.stdout, help = 'Output file xlsx to write uniroma1 to, default standard output', dest = "outputFile")
parser.add_argument('-ojson', '--outputjson', nargs = '?', default = sys.stdout, help = 'Output file json to write uniroma1 to, default none', dest = "outputFileJson")
parser.add_argument('-sun', '--strictuni', help = 'Strict includ only @uniroma1.it an no subsets', action=argparse.BooleanOptionalAction, dest="sun" )
args = parser.parse_args()

if args.inputFile == "" and args.urlJson == "":
    parser.error("--urlJson or --InputFile is required.")

if args.inputFile != "" and args.urlJson != "":
    parser.error("--urlJson and --inpuFile can be use only exclusively each other")
    
input_file=args.inputFile
output_file_nouni=args.outputFileNo
output_file_uni=args.outputFile
json_file_out=args.outputFileJson
url = args.urlJson
sun = args.sun

splitJson(input_file, url, sun, output_file_nouni, output_file_uni,json_file_out)