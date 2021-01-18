import json
import os
import time
import numpy as np
import pandas as pd
from get_path import getPath
from open_json import OpenFile
from myencode import MyEncoder
from jsonDataGet import get_data
from FCW_AEB import FcwAeb
if __name__ == "__main__":
    base_floder_path = r'C:\Users\FAC2SZH\Desktop\hive_file_code\vms'
    json_data_list = get_data(base_floder_path)
    # with open('./new_file.json', 'w', encoding='utf-8') as f:
    #     json.dump(json_data_list, f, cls=MyEncoder, ensure_ascii=False)
    while True:
        try:
            json_data = json_data_list.pop()
        except IndexError:
            break
        else:
            for key,value in json_data.items():
                '''
                将单个文件中的单条信息放入其中进行获取
                '''
                fa = FcwAeb(value)
                alert_warning_df = fa.alert_warning()
                print(alert_warning_df)
