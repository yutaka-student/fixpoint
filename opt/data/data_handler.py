import datetime

class data_handler():
    #ログ(１行)を受け取り、時間・ip・サブネット・応答時間に分けたログを返す
    @staticmethod
    def extract_infomation(log):
        send_time = []
        server_ip = []
        subnet = -1
        response_time = -1

        log = log.split(',')

        send_time = log[0][:4] + '-' + log[0][4:6] + '-' + log[0][6:8] + '-' + log[0][8:10] + '-' + log[0][10:12] + '-' + log[0][12:14]
        send_time = datetime.datetime.strptime(send_time, "%Y-%m-%d-%H-%M-%S")
        #send_time = [int(data) for data in send_time]

        server_ip, subnet = log[1].split('/')
        #ip = ip.split('.')
        #server_ip = [int(data) for data in ip]
        subnet = int(subnet)

        response_time = log[2]
        response_time = -1 if response_time == '-' else int(response_time)

        return send_time, server_ip, subnet, response_time

    #辞書型dic、文字列key、配列dataを受け取り、dic[key]にある配列に追加する
    #dicにkeyがない場合、新しく生成
    @staticmethod
    def append_list_on_dictionary(dic, key, data):
        if key in dic:
            dic[key].append(data)
        else:
            dic[key] = [data]

    #全てのログデータを配列で受け取り、アドレス毎に分けた配列を返す
    @staticmethod
    def divide_each_address_data(logs):
        each_address_data = {}
        for log in logs:
            data = data_handler.extract_infomation(log)
            data_handler.append_list_on_dictionary(each_address_data, data[1], [data[0], data[2], data[3]])

        return each_address_data
    
    #address_data: アドレス毎のデータ
    #n: 故障とみなすまでの回数
    #故障期間を配列で返す(故障開始、故障終了のログが格納される)
    #正常なログがなく終了した場合、故障開始のみ格納された配列を返す
    @staticmethod
    def extract_failure_address_data(address_data, n=1):
        result_data = []
        fail_count = 0
        fail_start_data = []
        for data in address_data:
            if data[2] == -1:
                if fail_count == 0:
                    fail_count += 1
                    fail_start_data = data
                else:
                    fail_count += 1
            else:
                if fail_count >= n:
                    result_data.append([fail_start_data, data])
                    fail_count = 0
                else:
                    fail_count = 0
        if fail_count >= n:
            result_data.append([fail_start_data])
        return result_data
    
    #each_address_data: アドレス毎に別れた全ログデータ
    #n: 故障とみなすまでの回数
    #それぞれのアドレスでの故障期間を配列にして返す
    @staticmethod
    def extract_failure_data(each_address_data, n=1):
        failure_data = {}
        for address in each_address_data:
            failure_data[address] = data_handler.extract_failure_address_data(each_address_data[address], n)
        return failure_data
    
    #address_data: アドレス毎のデータ
    #m: 過負荷とみなす時間
    #t: t回以上mミリ秒を超えたら過負荷とみなす
    #過負荷期間を配列で返す(過負荷開始、過負荷終了のログが格納される)
    #正常なログがなく終了した場合、過負荷開始のみ格納された配列を返す
    @staticmethod
    def extract_overload_condition_data(address_data, m, t):
        result_data = []
        fail_count = 0
        fail_start_data = []
        for data in address_data:
            if data[2] > t:
                if fail_count == 0:
                    fail_count += 1
                    fail_start_data = data
                else:
                    fail_count += 1
            elif data[2] == -1:
                fail_count += 1
            else:
                if fail_count >= m:
                    result_data.append([fail_start_data, data])
                    fail_count = 0
                else:
                    fail_count = 0
        if fail_count >= m:
            result_data.append([fail_start_data])
        return result_data
    
    #each_address_data: アドレス毎に別れた全ログデータ
    #m: 過負荷とみなす時間
    #t: t回以上mミリ秒を超えたら過負荷とみなす
    #それぞれのアドレスでの過負荷期間を配列にして返す
    @staticmethod
    def extract_overload_data(each_address_data, m, t):
        overload_data = {}
        for address in each_address_data:
            overload_data[address] = data_handler.extract_overload_condition_data(each_address_data[address], m, t)
        return overload_data
    
    #ログの日付を表示したい形式に直して返す
    @staticmethod
    def format_date_time(date):
        return date.strftime('%Y年%m月%d日 %H時%M分%S秒')
    
    #アドレス、故障 or 過負荷期間を元に出力する
    @staticmethod
    def print_data(address, result_data, message = '故障'):
        for data_address in result_data:
            if address == data_address:
                if len(result_data[address]) != 0:
                    print(message + '期間')
                    for data in result_data[address]:
                        if len(data) == 0:
                            continue
                        elif len(data) == 1:
                            print(data_handler.format_date_time(data[0][0]) + ' ~ ')
                        elif len(data) == 2:
                            print(data_handler.format_date_time(data[0][0]) + ' ~ ' + data_handler.format_date_time(data[1][0]))
                else:
                    print(message + '期間')
                    print('なし')
    
    #ipアドレスを2進数32bitに変換する
    @staticmethod
    def address2binary(address):
        address_list = address.split('.')
        result = ''
        for address in address_list:
            address = int(address)
            binary = ''
            while(address != 0):
                binary = str(address % 2) + binary
                address = int(address / 2)
            for i in range(len(binary), 8):
                binary = '0' + binary
            result += binary
        return result
    
    #2進数32bit文字列をipアドレスに変換する
    @staticmethod
    def binary2address(binary):
        address_list = []
        for i in range(0, len(binary), 8):
            divided_binary = binary[i:i+8]
            weight = 128
            address = 0
            for j in range(8):
                address += int(divided_binary[j]) * weight
                weight = int(weight / 2)
            address_list.append(str(address))
        return ".".join(address_list)
    
    #prefix情報を元に、ipアドレスをサブネットアドレスに変換して返す
    @staticmethod
    def get_masked_address(address, prefix):
        binary = data_handler.address2binary(address)
        for i in range(prefix, len(binary)):
            binary = binary[:i] + '0' + binary[i+1:]
        return data_handler.binary2address(binary)
    
    #ログを、サブネット毎にグループ化した配列を返す
    @staticmethod
    def group_by_subnet(logs):
        each_data = [data_handler.extract_infomation(log) for log in logs]
        subnet_list = {}
        for data in each_data:
            masked_address = data_handler.get_masked_address(data[1],data[2])
            if masked_address in subnet_list:
                subnet_list[masked_address].append([data[0], data[2], data[3]])
            else:
                subnet_list[masked_address] = [[data[0], data[1], data[3]]]
        return subnet_list
    
    #failure_subnet_list: 故障サブネット
    #each_address_data: それぞれのアドレスに分かれたログデータ
    #故障サブネットに属するipアドレスを、each_address_dataから除いた配列を返す
    @staticmethod
    def exclude_subnet_failure(each_address_data, failure_subnet_list):
        result_data = {}
        for address in each_address_data:
            for i in range(len(each_address_data[address])):
                masked_address = data_handler.get_masked_address(address, each_address_data[address][i][1])
                if len(failure_subnet_list[masked_address]) == 0:
                    data_handler.append_list_on_dictionary(result_data, address, each_address_data[address][i])
                for subnet_data in failure_subnet_list[masked_address]:
                    if len(subnet_data) == 1:
                        begin_failure = subnet_data[0][0]
                        if each_address_data[address][i][0] < begin_failure:
                            data_handler.append_list_on_dictionary(result_data, address, each_address_data[address][i])
                    elif len(subnet_data) == 2:
                        begin_failure = subnet_data[0][0]
                        end_failure = subnet_data[1][0]
                        if not (each_address_data[address][i][0] >= begin_failure and each_address_data[address][i][0] < end_failure):
                            data_handler.append_list_on_dictionary(result_data, address, each_address_data[address][i])
        return result_data