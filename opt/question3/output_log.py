import sys
sys.path.append('../')
from data.data_handler import data_handler
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--n', type=int, help='n回以上連続してタイムアウトした場合にのみ故障とみなす')
parser.add_argument('--m', type=int, help='直近m回の応答が指定時間を超えたら過負荷状態とみなす')
parser.add_argument('--t', type=int, help='tミリ秒を超えるものを過負荷状態とみなす')
args = parser.parse_args()

n = args.n
m = args.m
t = args.t

#データ読み込み
f = open('../data/serverlog.txt')
logs = f.readlines()
f.close()

#改行削除
logs = [str.rstrip(data) for data in logs]

each_address_data = data_handler.divide_each_address_data(logs)
failure_data = data_handler.extract_failure_data(each_address_data, n)

overload_data = data_handler.extract_overload_data(each_address_data, m, t)

for address in each_address_data:
    print('ipアドレス: ' + address)
    data_handler.print_data(address, failure_data)
    print()
    data_handler.print_data(address, overload_data, '過負荷')
    print()