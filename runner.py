from xml.etree.ElementTree import parse
from lib import dem_parser
import os
import json
import argparse   

parser = argparse.ArgumentParser(
    description='create slope ratio grid from elevation data')    


parser.add_argument('--file', '-f', help='elevation data file')
parser.add_argument('--dir', '-d', help='directory of elevation data file')
parser.add_argument('--output', '-o', default='./result/result.json',
                    help='slope grid data output file. default ./result/result.json')

args = parser.parse_args()    


#'./dem/FG-GML-5339-35-96-DEM5A-20190130.xml'
output = os.path.realpath(args.output)
if file := args.file:
    
    data = dem_parser.parse(os.path.realpath(file))
elif directry := args.dir:
    data = dem_parser.parse_dir(os.path.realpath(directry))
else:
    exit('file or directory required')
with open(output, mode='w') as fp:
     json.dump(data, fp)
