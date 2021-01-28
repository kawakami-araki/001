import numpy as np
import pandas as pd



# 广汽状态机4 to 7
b = [
    'ADAS_HWA_ILCLeftSt','ADAS_HWA_ILCRighttSt', #状态机or
    'EPS_StrngWhlTorq',  #驾驶员没有注意力集中（前置条件）
    #自车处于目标车道（前置条件）
    'ADAS_LnMarkingCurvature',#曲率半径不符合变道条件
    #Manoeuvre 未在规定时间内结束
    'BCM_TurnLightSwitchSt'#转向灯关闭或拨到反向
    ]

class ILC:
    def __init__(self, data):
        self.data = data
    def data_analysis(self, signal_list):
        all_sampleTime = []
        all_data = {}
        for this_value in self.data:
            sampleTime = [int(this_value['sampleTime']) - 1000*i for i in range(10)]
            sampleTime.reverse()
            all_sampleTime.extend(sampleTime)
            for key in signal_list:
                if key in this_value['dataList']:
                    data = this_value['dataList'][key]
                    if data == '':
                        data = [0 for i in range(10)]
                    elif 1 < len(data) < 10:
                        if ',' not in data:
                            data = [data] + [0 for i in range(9)]
                        else:
                            data = data.split(',') + [0 for i in range(10-len(data))]
                    else:
                        data = data.split(',')
                else:
                    continue
                data.reverse()
                if key in all_data:
                    all_data[key].extend(data)
                else:
                    all_data[key] = data
        #print('all_data:',all_data)      
        return (all_sampleTime, all_data)
    def create_DataFrame(self, data):
        sample_data = {}
        for key in data.keys():
            sample_data[key] = data[key]['samples']
        index_list = []
        index_num = 0
        print('开始构建DataFrame')
        data_len = []
        key_list = []
        for key,value in sample_data.items():
            data_len.append(len(value))
            key_list.append(key)
        for i in range(len(data_len)):
            if data_len[i] < max(data_len):
                sample_data[key_list[i]].extend([0 for j in range(max(data_len)-data_len[i])])
        this_data = pd.DataFrame(sample_data)
        message_list = []
        columns_list = list(this_data)
        print('开始计算单一时间的状态')
        for indexs in this_data.index:
            # 单行数据转化列表
            one_result = []
            one_data = this_data.loc[indexs].values.tolist()
            for i in range(len(one_data)):
                if i== 0:
                    if one_data[i] == 0:
                        pass
                    else:
                        for key,value in data[columns_list[i]]['condition'].items():
                            if one_data[i] == value:
                                one_result.append(columns_list[i] + ': ' + key)
                                break

                elif i==1:
                    if one_data[i] == 0:
                        pass
                    else:
                        for key,value in data[columns_list[i]]['condition'].items():
                            if one_data[i] == value:
                                one_result.append(columns_list[i] + ': ' + key)
                                break
                elif i==2:
                    if one_data[i] == 0:
                        pass
                    else:
                        for key,value in data[columns_list[i]]['condition'].items():
                            if one_data[i] == value:
                                one_result.append(columns_list[i] + ': ' + key)
                                break
                elif i==3:
                        for key,value in data[columns_list[i]]['condition'].items():
                            if one_data[i] == value:
                                one_result.append(columns_list[i] + ': ' + key)
                                break
            if one_result == []:
                message = '功能运行正常。'
            else:
                message = ';'.join(one_result)
            message_list.append(message)
        this_data['Final_result'] = message_list
        return this_data
    def ILC_to_seven(self):
        timestamps, datalist = self.data_analysis(b)
        result = {
            # 1 ILC状态机
            'ILC_state': {'key': ['ADAS_HWA_ILCLeftSt','ADAS_HWA_ILCRighttSt'], 'samples': [], 'timestamps': [], 'condition':{'Not_TOR': 0, 'TOR_left': 1,'TOR_right': 2}},
            # 2 驾驶员没有注意力集中（前置条件）
            'Driver_attention': {'key': ['EPS_StrngWhlTorq'], 'samples': [], 'timestamps': [], 'condition':{'Attention': 0,'No_attention': 1}},
            # 3 自车处于目标车道（前置条件）（暂无信号）
            # 4 曲率半径不符合变道条件
            'Curvature_radius': {'key': ['ADAS_LnMarkingCurvature'], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 5 Manoeuvre 未在规定时间内结束（暂无信号）
            # 6 转向灯关闭或拨到反向
            'Turnlight_state': {'key': ['BCM_TurnLightSwitchSt'], 'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Turn_left': 1,'Turn_right':2,'Error':3}},
            
        }
        '''
        判断条件
        '''
        for key in result.keys():
            result[key]['timestamps'] = timestamps
            if key == 'ILC_state':
                key_1, key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 7:
                            result[key]['samples'].append(1)
                        elif int(datalist[key_2][i]) == 7:
                            result[key]['samples'].append(2)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Driver_attention':
                key_1= str(result[key]['key'])
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        try:
                            if float(datalist[key_1][i]) < 0.6:
                                result[key]['samples'].append(1)
                            else:
                                result[key]['samples'].append(0)
                        except IndexError:
                            break

            if key == 'Curvature_radius':
                key_1= str(result[key]['key'])
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) > 0.00142857:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            
            if key == 'Turnlight_state':
                key_1= str(result[key]['key'])
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 0:
                            result[key]['samples'].append(0)
                        elif int(datalist[key_1][i]) == 1:
                            result[key]['samples'].append(1)
                        elif int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(2)
                        else:
                            result[key]['samples'].append(3)


            
        this_dataFrame = self.create_DataFrame(result)
        print(this_dataFrame)
        return this_dataFrame