import sys
sys.path.append('../')
from data.data_handler import data_handler
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--n', type=int, help='n回以上連続してタイムアウトした場合にのみ故障とみなす')
args = parser.parse_args()

n = args.n

#データ読み込み
f = open('../data/serverlog.txt')
logs = f.readlines()
f.close()

#改行削除
logs = [str.rstrip(data) for data in logs]

each_address_data = data_handler.divide_each_address_data(logs)
failure_data = data_handler.extract_failure_data(each_address_data, n)

for address in each_address_data:
    print('ipアドレス: ' + address)
    data_handler.print_data(address, failure_data)
    print()