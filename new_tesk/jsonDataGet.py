import json
import os
import time
import numpy as np
import pandas as pd
from get_path import getPath
from open_json import OpenFile
from myencode import MyEncoder




def get_signal_list():
    signal = input('请输入要获取的信号（多个信号以“,”分隔）：')
    print('要获取的信号为：', signal if signal else '无信号。')
    if signal != '':
        if ',' in signal:
            signal_list = signal.split(',')
        else:
            signal_list.append(signal)

def get_data(path):
    file_list = getPath(path)
    signal_list = []
    get_signal_list()
    json_file_data_list = []
    while True:
        try:
            file_path = file_list.pop()
        except IndexError as e:
            break
        else:
            file_name = file_path.split('\\')[-1].split('.')[0]
            print(file_name,'读取ing')
            of = OpenFile(file_path)
            json_file_data = of.data_analysis(signal_list=signal_list)
            if json_file_data:
                json_file_data_list.append(json_file_data)
        break
    return json_file_data_list