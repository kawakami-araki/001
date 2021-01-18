import numpy as np
import pandas as pd



# 警戒型告警（距离报警）
a = ['IFC_AEBTarMotionState','BCS_VehSpd','MRR_FCWLatentWarn','BCS_VDCActiveSt','BCS_TCSActiveSt','MRR_FCWOffSt','VCU_VehRdySt','MRR_ACCActiveSt']
# 迫近型告警
b = ["EBB_BrkPedalApplied",'EBB_BrkPedPst','SAS_SteeringAngle','SAS_SteeringAngleSpd','EMS_GasPedalActPstforMRR',
    'EBB_BrkPedalApplied','EBB_BrkPedPst','VCU_CrntGearLvl','MRR_AWBReq','MRR_FCWOffSt','MRR_FCWPreWarn',
    'BCS_VehSpd','BCS_VDCActiveSt','BCS_TCSActiveSt','VCU_VehRdySt']
# 短促制动
c = ['EBB_BrkPedalApplied', 'EBB_BrkPedPst', 'MRR_AEBDecelCtrlReq', 'SAS_SteeringAngle', 'SAS_SteeringAngleSpd', 
    'EMS_GasPedalActPstforMRR', 'MRR_AWBReq', 'VCU_CrntGearLvl', 'BCS_VDCActiveSt', 'BCS_VDCOff', 'BCS_TCSActiveSt', 
    'BCS_TCSOff', 'BCS_VDCOff', 'BCS_VDCFaultSt', 'BCS_VehSpd', 'VCU_VehRdySt', 'MRR_FCWOffSt']
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
                    print('信号', key, '不存在！')
                    continue
                data.reverse()
                if key in all_data:
                    all_data[key].extend(data)
                else:
                    all_data[key] = data
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
                if i not in [0]:
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
        samples, datalist = self.data_analysis(a)
        result = {
            # 1 目标状态
            'Target_state': {'samples': [], 'timestamps': [], 'condition':{'Stationary': 1, 'Moving': 2}},
            # 2 车速范围
            'Spd_range': {'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 3 报警触发间隔
            'MRR_FCWLatentWarn': {'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Warning': 1}},
            # 4 VDC
            'VDC': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 5 TCS
            'TCS': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 6 FCW
            'FCW': {'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 7 发动机运转
            'engine': {'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
            # 8
            'ACC': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}}
        }
        for key in result.keys():
            result[key]['timestamps'] = samples
            if key in datalist:
                result[key]['samples'] = datalist[key]
            else:
                result[key]['samples'] = [0 for i in range(len(samples))]
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
        this_dataFrame = self.create_DataFrame(result)
        return this_dataFrame
    def approaching_warning(self):
        samples, datalist = self.data_analysis(b)
        result = {
            # 1
            'IFC_AEBTarMotionState': {'samples': [], 'timestamps': [], 'condition':{'Stationary': 1, 'Moving': 2}},
            # 2 55~130
            'BCS_VehSpd': {'samples': [], 'timestamps': [], 'condition':{'Normal': 0, 'Out_of_range': 1}},
            # 3
            'MRR_FCWLatentWarn': {'samples': [], 'timestamps': [], 'condition':{'No_warning': 0, 'Warning': 1}},
            # 4
            'BCS_VDCActiveSt': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 5
            'BCS_TCSActiveSt': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
            # 6
            'MRR_FCWOffSt': {'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
            # 7
            'VCU_VehRdySt': {'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
            # 8
            'MRR_ACCActiveSt': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}}
        }
        for key in b:
            result[key]['timestamps'] = samples
            if key in datalist:
                result[key]['samples'] = datalist[key]
            else:
                result[key]['samples'] = [0 for i in range(len(samples))]
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
        this_dataFrame = self.create_DataFrame(result)
        return this_dataFrame
    def short_brake(self):
        for key in c:
            pass
    def prefill(self):
        for key in d:
            pass
    def AEB(self):
        for key in e:
            pass
    def EBA(self):
        for key in f:
            pass
    def AEB_pedestrian(self):
        for key in g:
            pass
    def AEB_two_wheeled_vehicle(self):
        for key in h:
            pass