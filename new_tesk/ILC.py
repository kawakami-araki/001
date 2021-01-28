import numpy as np
import pandas as pd


# a = [
#     # 变道功能处于释放状态    1：Enabled
#     "ADAS_HWA_EnableSt",
#     # 驾驶员无干涉车辆控制的倾向 >=1.5NM  >0.2s >=1NM >2s
#     'EPS_StrngWhlTorq','EPS_StrngWhlTorq','EPS_StrngWhlTorq','EPS_StrngWhlTorq',
#     # 车辆动态处于可控阈值范围内  <=3 m/s2  <=0.18 rad/s
#     "BCS_ActVehLaltrlAccel","BCS_YawRate",
#     # 车速处于阈值范围内（60-120kph）
#     "BCS_VehSpd",
#     # 曲率半径符合条件  >=750m
#     "ADAS_LnMarkingCurvature",
#     # 本车道与目标车道之间的车道线能被识别到  ！=0
#     "ADAS_LlnMrkingDispSt","ADAS_RlnMrkingDispSt",
#     # 变道侧车道线类型符合变道要求   1 or 2
#     "ADAS_RLnMarkingType","ADAS_LLnMarkingType",
#     # 其他ADAS功能状态支持变道功能被激活  TJA3or4, AEB=0,ELK=0
#     "IFC_TJA_ICA_St","MRR_AEBDecelCtrlReq","IFC_ELKSt",
#     # 变道灯激活    0=Not active   1=Active
#     "BCM_LeftTurnLampSt","BCM_RightTurnLampSt",
#     # 侧向变道允许激活   Permit
#     "ADAS_HWA_ILCLeftIndicator","ADAS_HWA_ILCRightIndicator",
#     # 驾驶员手扶方向盘   >=0.4 Nm
#     "EPS_StrngWhlTorq"
# ]
# b = [
#     'ADAS_HWA_ILCLeftIndicator','ADAS_HWA_ILCRightIndicator'
# ]
b = [
    'ADAS_HWA_ILCLeftSt','ADAS_HWA_ILCRighttSt', #状态机or
    'EPS_StrngWhlTorq',  #驾驶员没有注意力集中（前置条件）
    #自车处于目标车道（前置条件）
    'ADAS_LnMarkingCurvature',#曲率半径不符合变道条件
    #Manoeuvre 未在规定时间内结束
    'BCM_TurnLightSwitchSt'#转向灯关闭或拨到反向
    ]
c = [
    # 状态机
    'ADAS_HWA_ILCLeftSt','ADAS_HWA_ILCRighttSt',
    # 驾驶员在 manoeuvre 开始的时刻脱手
    'EPS_StrngWhlTorq',
    # 变道功能处于非释放状态
    'ADAS_HWA_EnableSt',
    # 本车道与目标车道之间的车道线不能被识别到
    'ADAS_LlnMrkingDispSt','ADAS_RlnMrkingDispSt',
    # 其他 ADAS 功能状态不支持变道功能被激活
    'IFC_TJA_ICA_St','MRR_AEBDecelCtrlReq','IFC_ELKSt',
    # 危险警示灯开启
    'BCM_HazardLampSt',
    # 驾驶员有干涉车辆控制的倾向
    # 车辆动态超出可控阈值范围内
    'BCS_ActVehLaltrlAccel','BCS_YawRate',
    # 车速超出阈值范围
    'ICM_VehInsSpd',
    # 转向灯关闭或拨到反向
    'BCM_TurnLightSwitchSt',
    # 道路条件不允许变道
    'ACU_IFC_RoadType',
    # 曲率半径不符合变道条件
    'ADAS_LnMarkingCurvature',
    # 驾驶员注意力集中
    'PS_StrngWhlTorq',
    # 变道结束
    'ADAS_HWA_ILCRightSt'
]
d = [
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
        return (all_sampleTime, all_data)
    def create_DataFrame(self, data, Isolation_list):
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
                if i not in Isolation_list:
                    if one_data[i] == 0:
                        pass
                    else:
                        for key,value in data[columns_list[i]]['condition'].items():
                            if one_data[i] == value:
                                one_result.append(columns_list[i] + ': ' + key)
                                break
                else:
                    if one_data[i] == 1:
                        pass
                    else:
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
    def Transition_to_Take_Over_Request(self):
        timestamps, datalist = self.data_analysis(c)
        result_1 = {# 状态机变化
        'State_machine': {'key': ["ADAS_HWA_ILCLeftSt",'ADAS_HWA_ILCRighttSt'], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Trigger_passive': 0}}}
        key_1, key_2 = result_1['State_machine']['key']
        result_1['State_machine']['timestamps'] = timestamps
        if key_1 in datalist:
            for i in range(len(datalist[key_1])):
                if int(datalist[key_1][i]) == 7 and int(datalist[key_1][i-1]) != 7:
                    result_1['State_machine']['samples'].append(1)
                else:
                    result_1['State_machine']['samples'].append(0)
            if key_2 in datalist:
                for j in range(len(datalist[key_2])):
                    if int(datalist[key_2][i]) == 7 and int(datalist[key_2][i-1]) != 7:
                        result_1['State_machine']['samples'][i] = 1
        result = {
            # 驾驶员在 manoeuvre 开始的时刻脱手  <0.4 Nm
            'Driver_out': {'key': ["EPS_StrngWhlTorq"], 'samples': [], 'timestamps': [], 'condition':{'Get_rid_of': 1, 'Not_sold': 0}},
            # 变道功能处于非释放状态  0 = Disable 1 = Enable   0
            'Lane_change_release': {'key': ["ADAS_HWA_EnableSt"], 'samples': [], 'timestamps': [], 'condition':{'Function_release': 1, 'Function_not_released': 0}},
            # 本车道与目标车道之间的车道线不能被识别到   == 0
            'Lane_line': {'key': ["ADAS_LlnMrkingDispSt", 'ADAS_RlnMrkingDispSt'], 'samples': [], 'timestamps': [], 'condition':{'Unrecognized': 0, 'Recognizable': 1}},
            # 其他 ADAS 功能状态不支持变道功能被激活  tja！=3，4  and AEB=1=ELK
            'ADAS_state': {'key': ['IFC_TJA_ICA_St', 'MRR_AEBDecelCtrlReq', 'IFC_ELKSt',], 'samples': [], 'timestamps': [], 'condition':{'Not_Supported': 1, 'support': 0}},
            # 危险警示灯开启 'BCM_HazardLampSt'
            'Hazard_warning_lights': {'key': ['BCM_HazardLampSt'], 'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 驾驶员有干涉车辆控制的倾向 'EPS_StrngWhlTorq'
            'Driver_orientation': {'key': ['EPS_StrngWhlTorq'], 'samples': [], 'timestamps': [], 'condition':{'Not': 0, 'Interference_in_vehicle_control': 1}},
            # 车辆动态超出可控阈值范围内 'BCS_ActVehLaltrlAccel','BCS_YawRate', >3 m/s2  >0.18 rad/s
            'Vehicle_trends': {'key': ['BCS_ActVehLaltrlAccel','BCS_YawRate'], 'samples': [], 'timestamps': [], 'condition':{'No_out_of_range': 0, 'Out_of_range': 1}},
            # 车速超出阈值范围 ICM_VehInsSpd <55 OR >125
            'Speed': {'key': ['ICM_VehInsSpd'], 'samples': [], 'timestamps': [], 'condition':{'No_out_of_range': 0, 'Out_of_range': 1}},
            # 转向灯关闭  'BCM_TurnLightSwitchSt',   =0
            'Cornering_lamp': {'key': ['BCM_TurnLightSwitchSt'], 'samples': [], 'timestamps': [], 'condition':{'open': 1, 'close': 0}},
            # 道路条件不允许变道 'ACU_IFC_RoadType',    1,6不允许
            'Road_conditions': {'key': ['ACU_IFC_RoadType'], 'samples': [], 'timestamps': [], 'condition':{'Lane_change_is_not_allowed': 1, 'Lane_change_allowed': 0}},
            # 曲率半径不符合变道条件 'ADAS_LnMarkingCurvature', <700m
            'Radius_of_curvature': {'key': ['ADAS_LnMarkingCurvature'], 'samples': [], 'timestamps': [], 'condition':{'Meet_lane_change_conditions': 0, 'Lane_change_condition_not_met': 1}},
            # 驾驶员注意力集中 'EPS_StrngWhlTorq','PS_StrngWhlTorq', >=0.6NM  >1s
            'Driver_status': {'key': ['EPS_StrngWhlTorq','PS_StrngWhlTorq'], 'samples': [], 'timestamps': [], 'condition':{'Inattention': 0, 'Focus': 1}},
            # 变道结束 'ADAS_HWA_ILCLeftSt','ADAS_HWA_ILCRightSt'  =5
            'Lane_change_status': {'key': ['ADAS_HWA_ILCLeftSt','ADAS_HWA_ILCRightSt'], 'samples': [], 'timestamps': [], 'condition':{'not_finished': 0, 'end': 1}},
        }
        for key in result.keys():
            result[key]['timestamps'] = timestamps
            if key == 'Driver_out':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) < 0.4:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key in [1,2,4,8]:
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 0:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
            if key == 'ADAS_state':
                key_1,key_2,key_3 = result[key]['key']
                if key_1 in datalist and key_2 in datalist and key_3 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) not in [3, 4] and int(datalist[key_2][i]) == int(datalist[key_3][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            
            if key == 'Driver_orientation':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) > 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Vehicle_trends':
                # >3 m/s2  >0.18 rad/s
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) > 3 or float(datalist[key_2][i]) > 0.18:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) > 3:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_2][i]) > 0.18:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Speed':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if 55 < float(datalist[key_1][i]) < 125:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
            if key == 'Road_conditions':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) in [1, 6]:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Radius_of_curvature':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) < 700:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Driver_status':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) >= 0.6 and float(datalist[key_2][i]) > 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Lane_change_status':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
        Secondary_result = self.create_DataFrame(result, [1,2])
        final_result = pd.DataFrame(result_1['State_machine']['samples'])
        final_result['timestamps'] = timestamps
        final_result['Final_result'] = Secondary_result['Final_result'].tolist()
        print(final_result)
        input()
        # final_result = pd.DataFrame()

    def ILC_to_seven(self):
        timestamps, datalist = self.data_analysis(d)
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


            
        this_dataFrame = self.create_DataFrame(result,[])
        print(this_dataFrame)
        return this_dataFrame