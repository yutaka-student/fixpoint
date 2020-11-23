import sys
sys.path.append('../')
from data.data_handler import data_handler

#データ読み込み
f = open('../data/serverlog.txt')
logs = f.readlines()
f.close()

#改行削除
logs = [str.rstrip(data) for data in logs]

each_address_data = data_handler.divide_each_address_data(logs)
failure_data = data_handler.extract_failure_data(each_address_data, 1)

for address in each_address_data:
    print('ipアドレス: ' + address)
    data_handler.print_data(address, failure_data)
    print()