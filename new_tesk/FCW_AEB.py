import numpy as np
import pandas as pd



# 警戒型告警（距离报警）
a = ['IFC_AEBTarMotionState','BCS_VehSpd','MRR_FCWLatentWarn','BCS_VDCActiveSt','BCS_TCSActiveSt','MRR_FCWOffSt','VCU_VehRdySt','MRR_ACCActiveSt']
# 迫近型告警
b = [
    "EBB_BrkPedalApplied",'EBB_BrkPedPst',  #and
    'SAS_SteeringAngle','SAS_SteeringAngleSpd', #or
    'EMS_GasPedalActPstforMRR','EBB_BrkPedalApplied','EBB_BrkPedPst',
    'VCU_CrntGearLvl','MRR_AWBReq',
    'MRR_FCWOffSt',
    'MRR_FCWPreWarn',
    'BCS_VehSpd',
    'BCS_VDCActiveSt',
    'BCS_TCSActiveSt',
    'VCU_VehRdySt']
# 短促制动
c = [
    'EBB_BrkPedalApplied', 'EBB_BrkPedPst', 'MRR_AEBDecelCtrlReq', 'SAS_SteeringAngle', 'SAS_SteeringAngleSpd', 
    'EMS_GasPedalActPstforMRR', 'MRR_AWBReq', 'VCU_CrntGearLvl', 'BCS_VDCActiveSt', 'BCS_VDCOff', 'BCS_TCSActiveSt', 
    'BCS_TCSOff', 'BCS_VDCOff', 'BCS_VDCFaultSt', 'BCS_VehSpd', 'VCU_VehRdySt', 'MRR_FCWOffSt']
# Prefill
d = [
    "SAS_SteeringAngle","SAS_SteeringAngleSpd",
    'EMS_GasPedalActPstforMRR',
    "EBB_BrkPedalApplied","EBB_BrkPedPst",
    'VCU_CrntGearLvl',
    'MRR_ABPReq',
    'BCS_VehSpd',
    'AEB_OffSt',
    'BCS_VDCActiveSt',
    'BCS_TCSActiveSt',
    'BCS_HDCCtrlSt',
    "BCS_VDCOff BCS_VDCFaultSt",
    'VCU_VehRdySt']

e = ["EBB_BrkPedalApplied","EBB_BrkPedPst",
    "SAS_SteeringAngle","SAS_SteeringAngleSpd",
    'EMS_GasPedalActPstforMRR',
    'VCU_CrntGearLvl',
    'MRR_AEBDecelCtrlReq',
    'MRR_AEBOffSt',
    'BCS_VDCActiveSt',
    'BCS_TCSActiveSt',
    'BCS_HDCCtrlSt',
    "SRS_DriverSeatBeltSt","BCS_VehSpd",
    "BCM_DriverDoorAjarSt","MRR_AEBLVehHoldReq",
    'BCS_VehSpd',
    'VCU_VehRdySt']

f = [
    "SAS_SteeringAngle","SAS_SteeringAngleSpd",
    'EMS_GasPedalActPstforMRR',
    'MRR_AEBTargetDecel',
    'MRR_AEBOffSt',
    'VCU_EMS_BrkPedalSt',
    "VCU_CrntGearLvl","BCS_MasterCylinderPr",
    "BCS_VDCActiveSt","BCS_VDCOff",
    "BCS_TCSActiveSt","BCS_TCSOff",
    'BCS_HDCCtrlSt',
    'BCM_DriverDoorAjarSt',
    'SRS_DriverSeatBeltSt',
    'BCS_VehSpd',
    'VCU_VehRdySt']
g = ['MRR_AEBOffSt',
    'IFC_CameraBlockageSt',
    'BCS_VehSpd',
    "SAS_SteeringAngle","SAS_SteeringAngleSpd",
    "EBB_BrkPedalApplied","EBB_BrkPedPst",
    'EMS_GasPedalActPstforMRR',
    'VCU_VehRdySt',
    'BCS_VDCActiveSt',
    'BCS_TCSActiveSt',
    'VCU_CrntGearLvl']

        
h = [
    "ADAS_SensorBlockedSts","ADAS_SensorFailure",
    'BCS_VehSpd',
    "SAS_SteeringAngle","SAS_SteeringAngleSpd",
    "EBB_BrkPedalApplied","EBB_BrkPedPst",
    'EMS_GasPedalActPstforMRR',
    'VCU_VehRdySt',
    'BCS_VDCActiveSt',
    'BCS_TCSActiveSt',
    'VCU_CrntGearLvl',
    'ADAS_LnMarkingCurvature']
class FcwAeb:
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
    def alert_warning(self):
        timestamps, datalist = self.data_analysis(a)
        result = {
            # 1 目标状态
            'IFC_AEBTarMotionState': {'samples': [], 'timestamps': [], 'condition':{'Stationary': 1, 'Moving': 2}},
            # 2 车速范围
            'BCS_VehSpd': {'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 3 报警触发间隔
            'MRR_FCWLatentWarn': {'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Warning': 1}},
            # 4 VDC
            'BCS_VDCActiveSt': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 5 TCS
            'BCS_TCSActiveSt': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 6 FCW
            'MRR_FCWOffSt': {'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 7 发动机运转
            'VCU_VehRdySt': {'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
            # 8
            'MRR_ACCActiveSt': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}}
        }
        for key in result.keys():
            result[key]['timestamps'] = timestamps
            if key in datalist:
                result[key]['samples'] = datalist[key]
            else:
                result[key]['samples'] = [0 for i in range(len(timestamps))]
            if key == 'BCS_VehSpd' and key in datalist:
                result[key]['samples'] = []
                for value in datalist[key]:
                    if 55 <= float(value) <= 130:
                        result[key]['samples'].append(0)
                    else:
                        result[key]['samples'].append(1)
            if key == 'MRR_FCWLatentWarn' and key in datalist:
                result[key]['samples'] = []
                print(datalist[key])
                sum = 0
                for value in range(len(datalist[key])-1):
                    result[key]['samples'].append(0)
                    if int(datalist[key][value]) == 1 and int(datalist[key][value+1]) == 0:
                        sum += 1
                    if int(datalist[key][value]) == 0 and  int(datalist[key][value+1]) == 1:
                        if sum >= 20:
                            pass
                        else:
                            left_index = value-sum
                            right_index = value + 1
                            for i in range(left_index, right_index):
                                result[key]['samples'][i] = 1
                            sum = 0
        this_dataFrame = self.create_DataFrame(result, [0,5])
        return this_dataFrame
    def approaching_warning(self):
        timestamps, datalist = self.data_analysis(b)
        result = {
            # 1 制动状态
            'Braking_state': {'key': ["EBB_BrkPedalApplied",'EBB_BrkPedPst'], 'samples': [], 'timestamps': [], 'condition':{'No_braking': 1, 'braking': 0}},
            # 2 转向状态
            'Steering_state': {'key': ['SAS_SteeringAngle','SAS_SteeringAngleSpd'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Steering_inhibition': 1, 'exit': 2}},
            # 3 油门状态
            'Throttle_status': {'key': ['EMS_GasPedalActPstforMRR','EBB_BrkPedalApplied','EBB_BrkPedPst'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Throttle_inhibition': 1, 'exit': 2}},
            # 4 档位状态
            'Gear_state': {'key': ['VCU_CrntGearLvl','MRR_AWBReq'], 'samples': [], 'timestamps': [], 'condition':{'Not_warning': 0, 'Gear_inhibition': 1, 'exit': 2}},
            # 5 FCW
            'FCW': {'key': ["MRR_FCWOffSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 6 报警间隔
            'Alarm_interval': {'key': ['MRR_FCWPreWarn'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Warning': 1}},
            # 7 速度范围
            'Spd_range': {'key': ["BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 8 VDC
            'VDC': {'key': ["BCS_VDCActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 9 TCS
            'TCS': {'key': ["BCS_TCSActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 10 发动机运转
            'engine': {'key': ["VCU_VehRdySt"], 'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}}
        }
        '''
        判断条件
        '''
        for key in result.keys():
            result[key]['timestamps'] = timestamps
            if key == 'Braking_state':
                key_1, key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_2][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Steering_state':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        try:
                            if float(datalist[key_1][i]) > 60 or float(datalist[key_2][i]) > 37.5:
                                result[key]['samples'].append(1)
                            else:
                                result[key]['samples'].append(0)
                        except IndexError:
                            break
                elif key_1 in datalist and key_2 not in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) > 600:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_1 not in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_2][i]) > 37.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)

            if key == 'Throttle_status':
                key_1,key_2,key_3 = result[key]['key']
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) >= 85:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                    if key_2 in datalist and key_3 in datalist:
                        for i in range(len(datalist[key_2])):
                            if int(datalist[key_2][i]) == 1 and float(datalist[key_3][i]) > 510:
                                result[key]['samples'][i] = 2
            
            if key == 'Gear_state':
                key_1, key_2 = result[key]['key']
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                    if key_2 in datalist:
                        for i in range(len(datalist[key_2])):
                            if int(datalist[key_2][i]) == 1:
                                result[key]['samples'][i] = 1

            key_1 = result[key]['key'][0]
            if key_1 in datalist:
                if key in ['FCW', 'VDC', 'TCS', 'engine']:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'Alarm_interval':
                    sum = 0
                    for i in range(len(datalist[key_1])-1):
                        result[key]['samples'].append(0)
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_1][i+1]) == 0:
                            sum += 1
                        if int(datalist[key_1][i]) == 0 and  int(datalist[key_1][i+1]) == 1:
                            if sum >= 20:
                                pass
                            else:
                                left_index = i-sum
                                right_index = i + 1
                                for j in range(left_index, right_index):
                                    result[key]['samples'][j] = 1
                                sum = 0
                if key == 'Spd_range':
                    for i in range(len(datalist[key_1])):
                        if 28 < float(datalist[key_1][i]) < 130:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
        this_dataFrame = self.create_DataFrame(result, [0,6,9])
        return this_dataFrame
    def short_brake(self):
        timestamps, datalist = self.data_analysis(c)
        result = {
            # 1 不满足制动抑制 
            'Braking_state': {'key': ["EBB_BrkPedalApplied",'EBB_BrkPedPst'], 'samples': [], 'timestamps': [], 'condition':{'No_braking': 1, 'braking': 0}},
            # 2 AEB/EBA 未触发 
            'AEB': {'key': ["MRR_AEBDecelCtrlReq"], 'samples': [], 'timestamps': [], 'condition':{'No_request': 1, 'Request': 0}},
            # 3 转向状态
            'Steering_state': {'key': ['SAS_SteeringAngle','SAS_SteeringAngleSpd'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Steering_inhibition': 1, 'exit': 2}},
            # 4 油门状态
            'Throttle_status': {'key': ['EMS_GasPedalActPstforMRR'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Throttle_inhibition': 1, 'exit': 2}},
            # 5 短促制动时间间隔
            'AWB': {'key': ['MRR_AWBReq'], 'samples': [], 'timestamps': [], 'condition':{'No_request': 0, 'Request': 1}},
            # 6 n档
            'VUC': {'key': ['VCU_CrntGearLvl'], 'samples': [], 'timestamps': [], 'condition':{'No_N_Neutral_gear': 0, 'N_Neutral_gear': 1}},
            # 7 VDC
            'VDC': {'key': ["BCS_VDCActiveSt", 'BCS_VDCOff'], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 8 TCS
            'TCS': {'key': ["BCS_TCSActiveSt", 'BCS_TCSOff'], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 9 ESP
            'ESP': {'key': ["BCS_VDCOff", 'BCS_VDCFaultSt'], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 10 速度范围
            'Spd_range': {'key': ["BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 11 发动机运转
            'engine': {'key': ["VCU_VehRdySt"], 'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
            # 12 FCW开启
            'FCW': {'key': ["MRR_FCWOffSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
        }
        for key in result.keys():
            if key == 'Braking_state':
                key_1, key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_2][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Steering_state':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        try:
                            if float(datalist[key_1][i]) > 60 or float(datalist[key_2][i]) > 37.5:
                                result[key]['samples'].append(1)
                            else:
                                result[key]['samples'].append(0)
                        except IndexError:
                            break
                elif key_1 in datalist and key_2 not in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) > 600:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_1 not in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_2][i]) > 37.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Throttle_status':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) >= 85:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key in ['VDC', 'TCS']:
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 0 and int(datalist[key_2][i]) == 0:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
            if key == 'ESP':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 0 and int(datalist[key_2][i]) == 0:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                    
            key_1 = result[key]['key'][0]
            if key_1 in datalist:
                if key in ['FCW', 'engine', 'AEB']:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'AWB':
                    sum = 0
                    for i in range(len(datalist[key_1])-1):
                        result[key]['samples'].append(0)
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_1][i+1]) == 0:
                            sum += 1
                        if int(datalist[key_1][i]) == 0 and  int(datalist[key_1][i+1]) == 1:
                            if sum >= 20:
                                pass
                            else:
                                left_index = i-sum
                                right_index = i + 1
                                for j in range(left_index, right_index):
                                    result[key]['samples'][j] = 1
                                sum = 0
                if key == 'Spd_range':
                    for i in range(len(datalist[key_1])):
                        if 30 < float(datalist[key_1][i]) < 130:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                if key == 'VUC':
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
        this_dataFrame = self.create_DataFrame(result, [0,10])
        return this_dataFrame
    def prefill(self):
        timestamps, datalist = self.data_analysis(d)
        result = {
            # 1 转向状态
            'Steering_state': {'key': ['SAS_SteeringAngle','SAS_SteeringAngleSpd'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Steering_inhibition': 1, 'exit': 2}},
            # 2 油门状态
            'Throttle_status': {'key': ['EMS_GasPedalActPstforMRR'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Throttle_inhibition': 1, 'exit': 2}},
            # 3 不满足制动抑制 
            'Braking_state': {'key': ["EBB_BrkPedalApplied",'EBB_BrkPedPst'], 'samples': [], 'timestamps': [], 'condition':{'No_braking': 1, 'braking': 0}},
            # 4 n档
            'VUC': {'key': ['VCU_CrntGearLvl'], 'samples': [], 'timestamps': [], 'condition':{'No_N_Neutral_gear': 0, 'N_Neutral_gear': 1}},
            # 5 触发时间间隔
            'ABP': {'key': ['MRR_ABPReq'], 'samples': [], 'timestamps': [], 'condition':{'No_request': 0, 'Request': 1}},
            # 6 速度范围
            'Spd_range': {'key': ["BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 8 Prefill
            'Prefill': {'key': ["MRR_AEBOffSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 8 VDC
            'VDC': {'key': ["BCS_VDCActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 9 TCS
            'TCS': {'key': ["BCS_TCSActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 10 HDC
            'HDC': {'key': ["BCS_HDCCtrlSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 11 ESP
            'ESP': {'key': ["BCS_VDCOff", 'BCS_VDCFaultSt'], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 12 发动机运转
            'engine': {'key': ["VCU_VehRdySt"], 'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
        }
        for key in result.keys():
            if key == 'Steering_state':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        try:
                            if float(datalist[key_1][i]) > 60 or float(datalist[key_2][i]) > 37.5:
                                result[key]['samples'].append(1)
                            else:
                                result[key]['samples'].append(0)
                        except IndexError:
                            break
                elif key_1 in datalist and key_2 not in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) > 60:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_1 not in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_2][i]) > 37.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Throttle_status':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) >= 85:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Braking_state':
                key_1, key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_2][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'VUC':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'ABP':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    sum = 0
                    for i in range(len(datalist[key_1])-1):
                        result[key]['samples'].append(0)
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_1][i+1]) == 1:
                            sum += 1
                        if int(datalist[key_1][i]) == 1 and  int(datalist[key_1][i+1]) == 0:
                            sum += 1
                            if 10 > sum > 3:
                                pass
                            else:
                                left_index = i-sum
                                right_index = i + 1
                                for j in range(left_index, right_index):
                                    result[key]['samples'][j] = 1
                                sum = 0
            if key == 'VDC':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1 or int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'ESP':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 0 and int(datalist[key_2][i]) == 0:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
            key_1 = result[key]['key'][0]
            if key_1 in datalist:
                if key in ['VDC', 'TCS', 'engine']:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'Spd_range':
                    for i in range(len(datalist[key_1])):
                        if 5 < float(datalist[key_1][i]) < 80:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
        this_dataFrame = self.create_DataFrame(result, [0,11])
        print(this_dataFrame)
        return this_dataFrame
    def AEB(self):
        timestamps, datalist = self.data_analysis(e)
        result = {
            # 1 转向状态
            'Steering_state': {'key': ['SAS_SteeringAngle','SAS_SteeringAngleSpd'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Steering_inhibition': 1, 'exit': 2}},
            # 2 油门状态
            'Throttle_status': {'key': ['EMS_GasPedalActPstforMRR'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Throttle_inhibition': 1, 'exit': 2}},
            # 3 不满足制动抑制 
            'Braking_state': {'key': ["EBB_BrkPedalApplied",'EBB_BrkPedPst'], 'samples': [], 'timestamps': [], 'condition':{'No_braking': 1, 'braking': 0}},
            # 4 n档
            'VUC': {'key': ['VCU_CrntGearLvl'], 'samples': [], 'timestamps': [], 'condition':{'No_N_Neutral_gear': 0, 'N_Neutral_gear': 1}},
            # 5 触发时间间隔
            'AEB_time': {'key': ['MRR_AEBDecelCtrlReq'], 'samples': [], 'timestamps': [], 'condition':{'No_request': 0, 'Request': 1}},
            # 6 AEB
            'AEB': {'key': ["MRR_AEBOffSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 7 VDC
            'VDC': {'key': ["BCS_VDCActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 8 TCS
            'TCS': {'key': ["BCS_TCSActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 9 HDC
            'HDC': {'key': ["BCS_HDCCtrlSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 10 驾驶员未系安全带
            'Belt': {'key': ["SRS_DriverSeatBeltSt", "BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1, 'Exit': 2}},
            # 11 驾驶员车门
            'DoorAjar': {'key': ["BCM_DriverDoorAjarSt", "MRR_AEBLVehHoldReq"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 12 速度范围
            'Spd_range': {'key': ["BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 13 碰撞风险
            #'Collision_risk': {'key': ["BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 13 发动机运转
            'engine': {'key': ["VCU_VehRdySt"], 'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
        }
        for key in result.keys():
            if key == 'Steering_state':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        try:
                            if float(datalist[key_1][i]) > 60 or float(datalist[key_2][i]) > 37.5:
                                result[key]['samples'].append(1)
                            else:
                                result[key]['samples'].append(0)
                        except IndexError:
                            break
                elif key_1 in datalist and key_2 not in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) > 60:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_1 not in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_2][i]) > 37.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Throttle_status':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) >= 85:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Braking_state':
                key_1, key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_2][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'VUC':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            
            if key == 'Belt':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) in [1,2]:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                    if key_2 in datalist:
                        for i in range(len(datalist[key_2])-1):
                            if abs(float(datalist[key_1][i])-float(datalist[key_1][i+1])) > 40:
                                result[key]['samples'][i] = 2
            if key == 'DoorAjar':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 0:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                    if key_2 in datalist:
                        sum = 0
                        for i in range(len(datalist[key_2])-1):
                            result[key]['samples'].append(0)
                            if int(datalist[key_2][i]) == 1 and int(datalist[key_2][i+1]) == 1:
                                sum += 1
                            if int(datalist[key_2][i]) == 1 and  int(datalist[key_2][i+1]) == 0:
                                sum += 1
                                if sum >= 20:
                                    pass
                                else:
                                    left_index = i-sum
                                    right_index = i + 1
                                    for j in range(left_index, right_index):
                                        result[key]['samples'][j] = 1
                                    sum = 0
            key_1 = result[key]['key'][0]
            if key_1 in datalist:
                if key in ['VDC', 'TCS', 'engine', 'AEB']:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'Spd_range':
                    for i in range(len(datalist[key_1])):
                        if 5 < float(datalist[key_1][i]) < 80:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                if key == 'AEB_time':
                    sum = 0
                    for i in range(len(datalist[key_1])-1):
                        result[key]['samples'].append(0)
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_1][i+1]) == 0:
                            sum += 1
                        if int(datalist[key_1][i]) == 0 and  int(datalist[key_1][i+1]) == 1:
                            if sum >= 20:
                                pass
                            else:
                                left_index = i-sum
                                right_index = i + 1
                                for j in range(left_index, right_index):
                                    result[key]['samples'][j] = 1
                                sum = 0
        this_dataFrame = self.create_DataFrame(result, [0,12])
        print(this_dataFrame)
        return this_dataFrame
    def EBA(self):
        timestamps, datalist = self.data_analysis(f)
        result = {
            # 1 转向状态
            'Steering_state': {'key': ['SAS_SteeringAngle','SAS_SteeringAngleSpd'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Steering_inhibition': 1, 'Exit': 2}},
            # 2 油门状态
            'Throttle_status': {'key': ['EMS_GasPedalActPstforMRR'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Throttle_inhibition': 1, 'Exit': 2}},
            # 3 不满足制动抑制    < -3.5
            'Braking_state': {'key': ["MRR_AEBTargetDecel"], 'samples': [], 'timestamps': [], 'condition':{'No_braking': 1, 'braking': 0}},
            # 4 EBA开启
            'EBA': {'key': ["MRR_AEBOffSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 5 触发时间间隔
            'BrkPedal': {'key': ['VCU_EMS_BrkPedalSt'], 'samples': [], 'timestamps': [], 'condition':{'No_request': 0, 'Request': 1}},
            # 6 n档  主缸压力过小
            'VUC': {'key': ['VCU_CrntGearLvl', 'BCS_MasterCylinderPr'], 'samples': [], 'timestamps': [], 'condition':{'No_N_Neutral_gear': 0, 'N_Neutral_gear': 1, 'Exit': 2}},
            # 7 VDC
            'VDC': {'key': ["BCS_VDCActiveSt", 'BCS_VDCOff'], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 8 TCS
            'TCS': {'key': ["BCS_TCSActiveSt", 'BCS_TCSOff'], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 9 HDC
            'HDC': {'key': ["BCS_HDCCtrlSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 10 驾驶员车门
            'DoorAjar': {'key': ["BCM_DriverDoorAjarSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 11 驾驶员未系安全带
            'Belt': {'key': ["SRS_DriverSeatBeltSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 12 速度范围  5-80
            'Spd_range': {'key': ["BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 13 发动机运转
            'engine': {'key': ["VCU_VehRdySt"], 'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
        }
        for key in result.keys():
            if key == 'Steering_state':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        try:
                            if float(datalist[key_1][i]) > 60 or float(datalist[key_2][i]) > 37.5:
                                result[key]['samples'].append(1)
                            else:
                                result[key]['samples'].append(0)
                        except IndexError:
                            break
                elif key_1 in datalist and key_2 not in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) > 60:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_1 not in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_2][i]) > 37.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Throttle_status':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) >= 85:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Braking_state':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) < -3.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'VUC':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                    if key_2 in datalist:
                        for i in range(len(datalist[key_2])):
                            if float(datalist[key_2][i]) < 20:
                                result[key]['samples'][i] = 2
            if key in ['VDC', 'TCS']:
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 0 and int(datalist[key_2][i]) == 0:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)

            key_1 = result[key]['key'][0]
            if key_1 in datalist:
                if key in ['HDC', 'engine', 'EBA', 'DoorAjar', 'Belt']:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'Spd_range':
                    for i in range(len(datalist[key_1])):
                        if 5 < float(datalist[key_1][i]) < 80:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                if key == 'BrkPedal':
                    sum = 0
                    for i in range(len(datalist[key_1])-1):
                        result[key]['samples'].append(0)
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_1][i+1]) == 0:
                            sum += 1
                        if int(datalist[key_1][i]) == 0 and  int(datalist[key_1][i+1]) == 1:
                            if sum >= 20:
                                pass
                            else:
                                left_index = i-sum
                                right_index = i + 1
                                for j in range(left_index, right_index):
                                    result[key]['samples'][j] = 1
                                sum = 0
        this_dataFrame = self.create_DataFrame(result, [0,12])
        return this_dataFrame
    def AEB_pedestrian(self):
        timestamps, datalist = self.data_analysis(g)
        result = {
            # 1 开启AEB
            'AEB': {'key': ['MRR_AEBOffSt'], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 2 摄像头检测到行人
            'camera': {'key': ["IFC_CameraBlockageSt"], 'samples': [], 'timestamps': [], 'condition':{'Not_blocked': 0, 'Blocked': 1}},
            # 3 速度范围  5-64
            'Spd_range': {'key': ["BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 4 转向状态
            'Steering_state': {'key': ['SAS_SteeringAngle','SAS_SteeringAngleSpd'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Steering_inhibition': 1, 'Exit': 2}},
            # 5 油门状态
            'Throttle_status': {'key': ['EMS_GasPedalActPstforMRR'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Throttle_inhibition': 1, 'Exit': 2}},
            # 6 不满足制动抑制    < -3.5
            'Braking_state': {'key': ["MRR_AEBTargetDecel"], 'samples': [], 'timestamps': [], 'condition':{'No_braking': 1, 'braking': 0}},
            # 7 发动机运转
            'engine': {'key': ["VCU_VehRdySt"], 'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
            # 8 VDC
            'VDC': {'key': ["BCS_VDCActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 9 TCS
            'TCS': {'key': ["BCS_TCSActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 10 n档
            'VUC': {'key': ['VCU_CrntGearLvl'], 'samples': [], 'timestamps': [], 'condition':{'No_N_Neutral_gear': 0, 'N_Neutral_gear': 1}},
            # 11 轨迹半径大于0.008 1m/s
            'Trajectory_radius': {'key': ['ADAS_LnMarkingCurvature'], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}}
        }
        for key in result.keys():
            if key == 'Steering_state':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        try:
                            if float(datalist[key_1][i]) > 60 or float(datalist[key_2][i]) > 37.5:
                                result[key]['samples'].append(1)
                            else:
                                result[key]['samples'].append(0)
                        except IndexError:
                            break
                elif key_1 in datalist and key_2 not in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) > 60:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_1 not in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_2][i]) > 37.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Throttle_status':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) >= 85:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Braking_state':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) < -3.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            key_1 = result[key]['key'][0]
            if key_1 in datalist:
                if key in ['AEB', 'camera', 'engine', 'VDC', 'TCS']:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'VUC':
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'Spd_range':
                    for i in range(len(datalist[key_1])):
                        if 5 < float(datalist[key_1][i]) < 64:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                if key == 'Trajectory_radius':
                    for i in range(len(datalist[key_1])):
                        if abs(float(datalist[key_1][i])) > 0.008:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
        this_dataFrame = self.create_DataFrame(result, [3,6])
        print(this_dataFrame)
        return this_dataFrame
    def AEB_two_wheeled_vehicle(self):
        timestamps, datalist = self.data_analysis(h)
        result = {
            # 1 开启AEB
            'AEB': {'key': ['MRR_AEBOffSt'], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 2 系统检测到两轮车
            'system_detection': {'key': ["ADAS_SensorBlockedSts", "ADAS_SensorFailure"], 'samples': [], 'timestamps': [], 'condition':{'Not_blocked': 0, 'Blocked': 1}},
            # 3 速度范围  5-64
            'Spd_range': {'key': ["BCS_VehSpd"], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 4 转向状态
            'Steering_state': {'key': ['SAS_SteeringAngle','SAS_SteeringAngleSpd'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Steering_inhibition': 1, 'Exit': 2}},
            # 5 油门状态
            'Throttle_status': {'key': ['EMS_GasPedalActPstforMRR'], 'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Throttle_inhibition': 1, 'Exit': 2}},
            # 6 不满足制动抑制    < -3.5
            'Braking_state': {'key': ["MRR_AEBTargetDecel", 'EBB_BrkPedPst'], 'samples': [], 'timestamps': [], 'condition':{'No_braking': 1, 'braking': 0}},
            # 7 发动机运转
            'engine': {'key': ["VCU_VehRdySt"], 'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
            # 8 VDC
            'VDC': {'key': ["BCS_VDCActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 9 TCS
            'TCS': {'key': ["BCS_TCSActiveSt"], 'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 10 n档
            'VUC': {'key': ['VCU_CrntGearLvl'], 'samples': [], 'timestamps': [], 'condition':{'No_N_Neutral_gear': 0, 'N_Neutral_gear': 1}},
            # 11 轨迹半径大于0.008 1m/s
            'Trajectory_radius': {'key': ['ADAS_LnMarkingCurvature'], 'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}}
        }
        for key in result.keys():
            if key == 'Steering_state':
                key_1,key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        try:
                            if float(datalist[key_1][i]) > 60 or float(datalist[key_2][i]) > 37.5:
                                result[key]['samples'].append(1)
                            else:
                                result[key]['samples'].append(0)
                        except IndexError:
                            break
                elif key_1 in datalist and key_2 not in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) > 60:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                elif key_1 not in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_2][i]) > 37.5:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Throttle_status':
                key_1 = result[key]['key'][0]
                if key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if float(datalist[key_1][i]) >= 85:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'Braking_state':
                key_1, key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1 and int(datalist[key_2][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
            if key == 'system_detection':
                key_1, key_2 = result[key]['key']
                if key_1 in datalist and key_2 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == int(b'00000000') or int(datalist[key_2][i]) == int(b'00000000'):
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                elif key_1 in datalist:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == int(b'00000000'):
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                elif key_2 in datalist:
                    for i in range(len(datalist[key_2])):
                        if int(datalist[key_2][i]) == int(b'00000000'):
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
            key_1 = result[key]['key'][0]
            if key_1 in datalist:
                if key in ['AEB', 'engine', 'VDC', 'TCS']:
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 1:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'VUC':
                    for i in range(len(datalist[key_1])):
                        if int(datalist[key_1][i]) == 2:
                            result[key]['samples'].append(1)
                        else:
                            result[key]['samples'].append(0)
                if key == 'Spd_range':
                    for i in range(len(datalist[key_1])):
                        if 5 < float(datalist[key_1][i]) < 64:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
                if key == 'Trajectory_radius':
                    for i in range(len(datalist[key_1])):
                        if abs(float(datalist[key_1][i])) > 0.008:
                            result[key]['samples'].append(0)
                        else:
                            result[key]['samples'].append(1)
        this_dataFrame = self.create_DataFrame(result, [3,6])
        return this_dataFrame