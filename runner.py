from lib import dem_parser
import os

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(
    description='create slope ratio grid from elevation data')    


parser.add_argument('arg1', help='elevation data file')    # 必須の引数を追加
parser.add_argument('--output', '-o', help='slope grid data output file. default ./result/result/json')

args = parser.parse_args()    


#'./dem/FG-GML-5339-35-96-DEM5A-20190130.xml'
file = os.path.realpath(args.arg1)

output = os.path.realpath(args.output)
dem_parser(file, output)
