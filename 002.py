from asammdf import MDF
import json,os,time,sys
import numpy as np
import pandas as pd
from pandas import Series
import plotly.graph_objs as go
import plotly as py
import plotly.offline as pltoff
from plotly.subplots import make_subplots
from plotly.graph_objs import Scatter,Layout


# MF4文件开启
class openMDF:
    def __init__(self, path):
        '''
        parms:  {path} Data file path
        '''
        self.open_file(path)

    def open_file(self, path):
        print('Open mf4 file')
        self.mf = MDF(path)
        self.file_name = path.split('\\')[-1].split('.')[0]
    def close_file(self):
        print('Close mf4 file')
        self.mf.close()
        
    def find_odometer(self, data_1:list, data_2):
        norm = 0
        new_dict = {'samples': [], 'timestamps': []}
        while norm <= 120:
            ec_hpa_df = pd.Series(data_1)
            range_min = ec_hpa_df[ec_hpa_df <= norm].max()
            sample = data_2.samples.tolist()[data_1.index(range_min)]
            timestamp = data_2.timestamps.tolist()[data_1.index(range_min)]
            new_dict['samples'].append(sample)
            new_dict['timestamps'].append(timestamp)
            norm += 0.01
        return new_dict

    def task(self):
        if self.mf:
            try:
                # 车道线丢失
                # Left_lane_line
                signal_for_Left_lane_line = self.mf.get('ADAS_LlnMrkingDispSt') # 左侧
                signal_for_Right_lane_line = self.mf.get('ADAS_RlnMrkingDispSt') # 右侧
                # 检测到变道
                Lane_change_1 = self.mf.get('EPS_StrngWhlTorq') # 变道1
                Lane_change_2 = self.mf.get('SAS_SteeringAngleSpd') # 变道2
                Lane_change_3 = self.mf.get('BCM_TurnLightSwitchSt') # 变道3
                # print(Lane_change_1,Lane_change_2,Lane_change_3)
                # 驾驶员踩刹车
                signal_for_BrkPedal = self.mf.get('EBB_BrkPedalApplied')
                # # 驾驶员操作 ACC 关闭
                # signal_for_ACCButtInfo_main = self.mf.get('EMS_ACCButtInfo')
                # # 驾驶员取消 ACC（慢速退出）
                # signal_for_ACCButtInfo_cancel = self.mf.get('EMS_ACCButtInfo')
                # 报警信号持续3s
                signal_for_IFC = self.mf.get('IFC_LKS_TakeoverReq')
                # EPS未就绪
                signal_for_EPS = self.mf.get('EPS_SteeringModeSt')
                # 危险报警灯开启
                signal_for_Hazard = self.mf.get('BCM_HazardLampSt')
                # 横摆角速率过高
                signal_for_YawRate = self.mf.get('BCS_YawRate')
                # 车道线曲率过低
                signal_for_LnMarkingCurvature = self.mf.get('ADAS_LnMarkingCurvature')
            except Exception as e:
                print(e)
                return False
            else:
                print('数据获取完毕')
                data_dict = {
                    'Left_lane_line': {'samples': [], 'timestamps': [], 'condition':{'No_display': 0, 'tracking': 1, 'intervening': 2, 'warning': 3}},
                    'Right_lane_line': {'samples': [], 'timestamps': [], 'condition':{'No_display': 0, 'tracking': 1, 'intervening': 2, 'warning': 3}},
                    'Lane_lines_on_both_sides': {'samples': [], 'timestamps': [], 'condition':{'No_display': 0, 'normal': 1}},
                    'BrkPedal': {'samples': [], 'timestamps': [], 'condition':{'Brake_pedal_not_applied': 0, 'Brake_pedal_applied': 1}},
                    # 'ACCButtInfo_main': {'samples': [], 'timestamps': [], 'condition':{'Brake_pedal_not_applied': 0, 'Brake_pedal_applied': 1}},
                    # 'ACCButtInfo_cancel': {'samples': [], 'timestamps': [], 'condition':{'Brake_pedal_not_applied': 0, 'Brake_pedal_applied': 1}},
                    'IFC': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
                    'EPS': {'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1, 'In_transition': 2, 'Fault': 3}},
                    'Hazard': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
                    'YawRate': {'samples': [], 'timestamps': [], 'condition':{'Yaw_rate_not_too_high': 0, 'Yaw_rate_too_high': 1}},
                    'LnMarkingCurvature': {'samples': [], 'timestamps': [], 'condition':{'Lane_curvature_not_too_low': 0, 'Lane_curvature_too_low': 1}},
                }
                data_for_Left_lane_line = self.find_odometer([x-signal_for_Left_lane_line.timestamps.tolist()[0] for x in signal_for_Left_lane_line.timestamps.tolist()],signal_for_Left_lane_line)
                # 1 左侧车道线丢失
                """
                0 = No display
                1= tracking
                2 = intervening
                3= warning
                """
                for sample in data_for_Left_lane_line['samples']:
                    if sample == b'No display':
                        data_dict['Left_lane_line']['samples'].append(0)
                    elif sample == b'tracking':
                        data_dict['Left_lane_line']['samples'].append(1)
                    elif sample == b'intervening':
                        data_dict['Left_lane_line']['samples'].append(2)
                    elif sample == b'warning':
                        data_dict['Left_lane_line']['samples'].append(3)
                    else:
                        data_dict['Left_lane_line']['samples'].append(-1)
                data_for_Right_lane_line = self.find_odometer([x-signal_for_Right_lane_line.timestamps.tolist()[0] for x in signal_for_Right_lane_line.timestamps.tolist()],signal_for_Right_lane_line)
                # 2右侧车道线丢失
                """
                0 = No display
                1= tracking
                2 = intervening
                3= warning
                """
                for sample in data_for_Right_lane_line['samples']:
                    if sample == b'No display':
                        data_dict['Right_lane_line']['samples'].append(0)
                    elif sample == b'tracking':
                        data_dict['Right_lane_line']['samples'].append(1)
                    elif sample == b'intervening':
                        data_dict['Right_lane_line']['samples'].append(2)
                    elif sample == b'warning':
                        data_dict['Right_lane_line']['samples'].append(3)
                    else:
                        data_dict['Right_lane_line']['samples'].append(-1)
                # 3
                # 双侧车道线丢失
                for i in range(len(data_dict['Right_lane_line']['samples'])):
                    if data_dict['Right_lane_line']['samples'][i] == data_dict['Left_lane_line']['samples'][i] == 0:
                        data_dict['Lane_lines_on_both_sides']['samples'].append(1)
                    else:
                        data_dict['Lane_lines_on_both_sides']['samples'].append(0)
                # 4 检测到变道
                # 



                # 5 驾驶员踩刹车
                '''
                0=Brake pedal not applied
                1=Brake pedal applied
                '''
                data_for_BrkPedal = self.find_odometer([x-signal_for_BrkPedal.timestamps.tolist()[0] for x in signal_for_BrkPedal.timestamps.tolist()],signal_for_BrkPedal)
                for sample in data_for_BrkPedal['samples']:
                    if sample == b'Brake pedal not applied':
                        data_dict['BrkPedal']['samples'].append(0)
                    elif sample == b'Brake pedal applied':
                        data_dict['BrkPedal']['samples'].append(1)
                    else:
                        data_dict['BrkPedal']['samples'].append(-1)
                # 6 
                # '''
                # # 驾驶员操作 ACC 关闭
                # signal_for_ACCButtInfo_main = self.mf.get('EMS_ACCButtInfo')
                # '''
                # # 数据错误，暂时忽略
                # data_for_ACCButtInfo_main = self.find_odometer([x-signal_for_ACCButtInfo_main.timestamps.tolist()[0] for x in signal_for_ACCButtInfo_main.timestamps.tolist()],signal_for_ACCButtInfo_main)
                # for sample in data_for_ACCButtInfo_main['samples']:
                #     if sample == b'Brake pedal not applied':
                #         data_dict['ACCButtInfo_main']['samples'].append(0)
                #     elif sample == b'Brake pedal applied':
                #         data_dict['ACCButtInfo_main']['samples'].append(1)
                #     else:
                #         data_dict['ACCButtInfo_main']['samples'].append(-1)

                # 7 
                # """
                # # 驾驶员取消 ACC（慢速退出）
                # signal_for_ACCButtInfo_cancel = self.mf.get('EMS_ACCButtInfo')
                # """
                # # 数据错误，暂时忽略
                # data_for_ACCButtInfo_main = self.find_odometer([x-signal_for_ACCButtInfo_cancel.timestamps.tolist()[0] for x in signal_for_ACCButtInfo_cancel.timestamps.tolist()],signal_for_ACCButtInfo_cancel)
                # for sample in data_for_ACCButtInfo_cancel['samples']:
                #     if sample == b'Brake pedal not applied':
                #         data_dict['ACCButtInfo_cancel']['samples'].append(0)
                #     elif sample == b'Brake pedal applied':
                #         data_dict['ACCButtInfo_cancel']['samples'].append(1)
                #     else:
                #         data_dict['ACCButtInfo_cancel']['samples'].append(-1)

                # 8
                '''
                # 报警信号持续3s
                signal_for_IFC = self.mf.get('IFC_LKS_TakeoverReq')
                0=Not active
                1=Active
                '''
                data_for_IFC = self.find_odometer([x-signal_for_IFC.timestamps.tolist()[0] for x in signal_for_IFC.timestamps.tolist()],signal_for_IFC)
                for sample in data_for_IFC['samples']:
                    if sample == b'Not active':
                        data_dict['IFC']['samples'].append(0)
                    elif sample == b'Active':
                        data_dict['IFC']['samples'].append(1)
                    else:
                        data_dict['IFC']['samples'].append(-1)
                
                # 9
                '''
                # EPS未就绪
                signal_for_EPS = self.mf.get('EPS_SteeringModeSt')
                0=Not ready
                1=Ready
                2=In transition
                3=Fault

                '''
                data_for_EPS = self.find_odometer([x-signal_for_EPS.timestamps.tolist()[0] for x in signal_for_EPS.timestamps.tolist()],signal_for_EPS)
                for sample in data_for_EPS['samples']:
                    if sample == b'Not ready':
                        data_dict['EPS']['samples'].append(0)
                    elif sample == b'Ready':
                        data_dict['EPS']['samples'].append(1)
                    elif sample == b'In transition':
                        data_dict['EPS']['samples'].append(2)
                    elif sample == b'In Fault':
                        data_dict['EPS']['samples'].append(3)
                    else:
                        data_dict['EPS']['samples'].append(-1)

                # 10
                '''
                # 危险报警灯开启
                signal_for_Hazard = self.mf.get('BCM_HazardLampSt')
                0=Not active
                1=Active

                '''
                data_for_Hazard = self.find_odometer([x-signal_for_Hazard.timestamps.tolist()[0] for x in signal_for_Hazard.timestamps.tolist()],signal_for_Hazard)
                for sample in data_for_Hazard['samples']:
                    if sample == b'Not active':
                        data_dict['Hazard']['samples'].append(0)
                    elif sample == b'Active':
                        data_dict['Hazard']['samples'].append(1)
                    else:
                        data_dict['Hazard']['samples'].append(-1)

                # 11
                '''
                # 横摆角速率过高
                signal_for_YawRate = self.mf.get('BCS_YawRate')
                Linear:
                -resolution: 0.0009765625 rad/s per bit
                -offset:-2.0943
                '''
                data_for_YawRate = self.find_odometer([x-signal_for_YawRate.timestamps.tolist()[0] for x in signal_for_YawRate.timestamps.tolist()],signal_for_YawRate)
                for sample in data_for_YawRate['samples']:
                    if sample > 0.25:
                        data_dict['YawRate']['samples'].append(1)
                    else:
                        data_dict['YawRate']['samples'].append(0)

                # 12
                '''
                # 车道线曲率过低
                signal_for_LnMarkingCurvature = self.mf.get('ADAS_LnMarkingCurvature')
                Linear
                - Resolution：0.00001 1/m per bit
                - offset：-0.01023 1/m
                Positive value means left bending
                '''
                data_for_LnMarkingCurvature = self.find_odometer([x-signal_for_LnMarkingCurvature.timestamps.tolist()[0] for x in signal_for_LnMarkingCurvature.timestamps.tolist()],signal_for_LnMarkingCurvature)
                for sample in data_for_LnMarkingCurvature['samples']:
                    if abs(sample)/0.00001 < 250:
                        data_dict['LnMarkingCurvature']['samples'].append(1)
                    else:
                        data_dict['LnMarkingCurvature']['samples'].append(0)


                sample_data = {}
                for key in data_dict.keys():
                    sample_data[key] = data_dict[key]['samples']
                index_list = []
                index_num = 0
                print('开始构建DataFrame')
                this_data = pd.DataFrame(sample_data)
                for i in range(len(this_data.index.tolist())):
                    index_list.append(index_num)
                    index_num += 0.01
                this_data.index = Series(index_list)
                # this_data = pd.DataFrame(sample_data, index=index_num)
                # 判断条件
                # 开始判断，得到结果后添加新的column
                message_list = []
                columns_list = list(this_data)
                print('开始计算单一时间的状态')
                for indexs in this_data.index:
                    # 单行数据转化列表
                    one_result = []
                    one_data = this_data.loc[indexs].values[0:-1].tolist()
                    for i in range(len(one_data)):
                        if i not in [4,6,7]:
                            if one_data[i] == 0:
                                pass
                            else:
                                for key,value in data_dict[columns_list[i]]['condition'].items():
                                    if one_data[i] == value:
                                        one_result.append(columns_list[i] + ': ' + key)
                                        break
                                    # else:
                                    #     one_result.appen(columns_list[i] + ': ' + '错误未定义')
                        else:
                            if one_data[i] == 1:
                                pass
                            else:
                                for key,value in data_dict[columns_list[i]]['condition'].items():
                                    if one_data[i] == value:
                                        one_result.append(columns_list[i] + ': ' + key)
                                        break
                    if one_result == []:
                        message = '功能运行正常。'
                    else:
                        message = ';'.join(one_result)
                    message_list.append(message)
                this_data['Final_result'] = message_list
                
                print(this_data['Final_result'])
                this_data.to_csv('./'+ self.file_name +'.csv')
                # print(this_data)
                # print(index_list)
            self.close_file()

# 获取全部的文件路径
def file_path_list(path):
    '''
    parms: {path} Base path address
    '''
    file_list = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if i.endswith('MF4'):
                file_list.append(os.path.join(root,i))
    return file_list



if __name__ == "__main__":
    base_file_path = 'G:/loc/szh/DA/Driving/System_APP/02_GAC/01_A18/DASy/'
    file_list = file_path_list(base_file_path)
    while True:
        try:
            file_path = file_list.pop()
            print(file_path)
        except IndexError as e:
            break
        else:
            file_name = file_path.split('\\')[-1].split('.')[0]
            mf = openMDF(file_path)
            mf.task()
        break
