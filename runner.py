from lib.dem_parser import parse
import os
file = os.path.realpath('./dem/FG-GML-5339-35-96-DEM5A-20190130.xml')
output = os.path.realpath('./result/result.json')
parse(file, output)
