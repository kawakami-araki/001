import json
import numpy as np
import pandas as pd

class OpenFile:
    def __init__(self, path, signal_list=None):
        self.data = self.open_file(path)
        self.data_analysis(signal_list)
    def open_file(self, path):
        try:
            f = open(path, 'r', encoding='utf8').read()
            if f:
                json_data = json.loads(f)
        except Exception as e:
            return False
        else:
            return json_data
    def data_analysis(self, signal_list=None):
        if self.data:
            value_data_list = []
            for key,value in self.data.items():
                keyId = value['keyId']
                sampleTime = value['sampleTime']
                if signal_list:
                    dataList = {}
                    while True:
                        try:
                            signal = signal_list.pop()
                        except IndexError as e:
                            break
                        else:
                            dataList[signal] = value['dataList'][signal]
                else:
                    dataList = value['dataList']
                value_data_list.append({
                    'keyId': keyId,
                    'sampleTime': sampleTime,
                    'dataList': dataList
                })
            value_data_list = sorted(value_data_list,key=lambda keys: keys['keyId'])
            
            data_list = {}
            for i in value_data_list:
                if i['keyId'] not in data_list.keys():
                    data_list[i['keyId']] = []
                data_list[i['keyId']].append({'sampleTime':i['sampleTime'], 'dataList': i['dataList']})
            for key, value in data_list.items():
                data_list[key] = sorted(value, key=lambda keys: keys['sampleTime'])
            return data_list
        else:
            print('文件开启失败')
            return False