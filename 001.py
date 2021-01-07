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
        # # AEB触发
        # signal_for_AEB = 'MRR_AEBDecelCtrlReq'
        # # VDC（Vehicle Dynamics Control）激活
        # signal_for_VDC = 'BCS_VDCActiveSt'
        # # ABS激活
        # signal_for_ABS = 'BCS_ABSActiveSt'
        # # TCS（Traction Control System）激活
        # signal_for_TCS = 'BCS_TCSActiveSt'
        # # HDC（Hill Descent Control）打开或激活
        # signal_for_HDC = 'BCS_HDCCtrlSt'
        # # EPB拉起
        # signal_for_EPB = 'EPB_SwitchSt'
        # # 制动踏板踩下两个cycle
        # signal_for_cycle = 'EBB_BrkPedalApplied'
        # # 发动机不运转
        # signal_for_engine = 'VCU_VehRdySt'
        # # 制动盘过热
        # signal_for_Brake = 'BCS_BrakeOverHeat'
        # # 雷达故障
        # ## 前角雷达
        # signal_for_Front_angle_radar = 'FRR_ErrSt'
        # ## 后角雷达
        # signal_for_Rear_angle_radar = 'BSDM_MRRSt'
        # # ESP关闭
        # signal_for_ESP = 'BCS_VDCOff'
        # # TCS关闭
        # signal_for_TCS = 'BCS_TCSOff'
        # # 溜坡
        # ## 左前
        # signal_for_FL = 'BCS_FLWheelRotatedDirection'
        # ## 左后
        # signal_for_RL = 'BCS_RLWheelRotatedDirection'
        # ## 右前
        # signal_for_FR = 'BCS_FRWheelRotatedDirection'
        # ## 右后
        # signal_for_RR = 'BCS_RRWheelRotatedDirection'
        # # 制动力不足
        # signal_for_Brake = 'BCS_NoBrakeForce'
        # # Override 超过 15 分钟
        # signal_for_Over_ride = 'MRR_ACCMode'
        # # 不在前进挡（N档（慢速退出，延时200ms））
        # signal_for_GearLvl = 'VCU_CrntGearLvl'
        # # 驾驶员侧车门打开（Standstill 延时 400ms）
        # signal_for_Door = 'BCM_DriverDoorAjarSt'
        # # 驾驶员侧安全带打开（Standstill 延时 400ms）
        # signal_for_SeatBelt = 'SRS_DriverSeatBeltSt'
        # # 驾驶员操作 ACC 关闭
        # signal_for_SeatBelt = 'EMS_ACCButtInfo'
        # # 驾驶员取消 ACC（慢速退出）
        # signal_for_SeatBelt = 'EMS_ACCButtInfo'
        if self.mf:
            try:
                # AEB触发
                signal_for_AEB = self.mf.get('MRR_AEBDecelCtrlReq')
                # VDC（Vehicle Dynamics Control）激活
                signal_for_VDC = self.mf.get('BCS_VDCActiveSt')
                # ABS激活
                signal_for_ABS = self.mf.get('BCS_ABSActiveSt')
                # TCS（Traction Control System）激活
                signal_for_TCS_Activate = self.mf.get('BCS_TCSActiveSt')
                # HDC（Hill Descent Control）打开或激活
                signal_for_HDC = self.mf.get('BCS_HDCCtrlSt')
                # EPB拉起
                signal_for_EPB = self.mf.get('EPB_SwitchSt')
                # 制动踏板踩下两个cycle
                signal_for_cycle = self.mf.get('EBB_BrkPedalApplied')
                # 发动机不运转
                signal_for_engine = self.mf.get('VCU_VehRdySt')
                # 制动盘过热
                signal_for_BrakeOverHeat = self.mf.get('BCS_BrakeOverHeat')
                # 雷达故障
                ## 前角雷达
                signal_for_Front_angle_radar = self.mf.get('FRR_ErrSt')
                ## 后角雷达
                # signal_for_Rear_angle_radar = self.mf.get('BSDM_MRRSt')
                # ESP关闭
                signal_for_ESP = self.mf.get('BCS_VDCOff')
                # TCS关闭
                signal_for_TCS_Off = self.mf.get('BCS_TCSOff')
                # 溜坡
                ## 左前
                signal_for_FL = self.mf.get('BCS_FLWheelRotatedDirection')
                ## 左后
                signal_for_RL = self.mf.get('BCS_RLWheelRotatedDirection')
                ## 右前
                signal_for_FR = self.mf.get('BCS_FRWheelRotatedDirection')
                ## 右后
                signal_for_RR = self.mf.get('BCS_RRWheelRotatedDirection')
                # 制动力不足
                signal_for_NoBrakeForce = self.mf.get('BCS_NoBrakeForce')
                # Override 超过 15 分钟
                signal_for_Over_ride = self.mf.get('MRR_ACCMode')
                # 不在前进挡（N档（慢速退出，延时200ms））
                signal_for_GearLvl = self.mf.get('VCU_CrntGearLvl')
                # 驾驶员侧车门打开（Standstill 延时 400ms）
                signal_for_Door = self.mf.get('BCM_DriverDoorAjarSt')
                # 驾驶员侧安全带打开（Standstill 延时 400ms）
                signal_for_SeatBelt = self.mf.get('SRS_DriverSeatBeltSt')
                # 驾驶员操作 ACC 关闭
                signal_for_ACCButtInfo_main = self.mf.get('EMS_ACCButtInfo')
                # 驾驶员取消 ACC（慢速退出）
                signal_for_ACCButtInfo_cancel = self.mf.get('EMS_ACCButtInfo')
            except Exception as e:
                print(e)
                return False
            else:
                print('数据获取完毕')
                data_dict = {
                    'AEB': {'samples': [], 'timestamps': [], 'condition':{'No_request': 0, 'Request': 1}},
                    'VDC': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
                    'ABS': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Active': 1}},
                    'TCS_Activate': {'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
                    'HDC': {'samples': [], 'timestamps': [], 'condition':{'Off': 0, 'On_active_braking': 1, 'On_not_active_braking': 2}},
                    'EPB': {'samples': [], 'timestamps': [], 'condition':{'Brake_pedal_not_applied': 0, 'Brake_pedal_applied': 1}},
                    'cycle': {'samples': [], 'timestamps': [], 'condition':{'Not_active': 0, 'Released': 1, 'Applied': 2}},
                    'engine': {'samples': [], 'timestamps': [], 'condition':{'Not_ready': 0, 'Ready': 1}},
                    'BrakeOverHeat': {'samples': [], 'timestamps': [], 'condition':{'Not_high': 0, 'Temp_too_high': 1}},
                    'Front_angle_radar': {'samples': [], 'timestamps': [], 'condition':{'on': 0, 'sensor_blocked': 1, 'Temporary_Error': 2, 'System_Error': 3}},
                    'ESP': {'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
                    'TCS_Off': {'samples': [], 'timestamps': [], 'condition':{'On': 0, 'Off': 1}},
                    'FLWheelRotated': {'samples': [], 'timestamps': [], 'condition':{'Forward': 0, 'Backward': 1}},
                    'RLWheelRotated': {'samples': [], 'timestamps': [], 'condition':{'Forward': 0, 'Backward': 1}},
                    'FRWheelRotated': {'samples': [], 'timestamps': [], 'condition':{'Forward': 0, 'Backward': 1}},
                    'RRWheelRotated': {'samples': [], 'timestamps': [], 'condition':{'Forward': 0, 'Backward': 1}},
                    'NoBrakeForce': {'samples': [], 'timestamps': [], 'condition':{'Exist_brake_force': 0, 'No_brakeforce': 1}},
                    'Over_ride': {'samples': [], 'timestamps': [], 'condition':{'Off_mode': 0, 'passive_mode': 1, 'Standby_mode': 2, 'Active_control_mode': 3,'Brake_only_mode': 4,'Override': 5,'Not_used': 6,'Failure_mode': 7}},
                    'GearLvl': {'samples': [], 'timestamps': [], 'condition':{'Invalid': 0, "D_Drive gear": 1, "N_Neutral_gear": 2, "R_Reverse_gear": 3,'P_Park_gear': 4}},
                    'Door': {'samples': [], 'timestamps': [], 'condition':{'Closed': 0, 'Open': 1}},
                    'SeatBelt': {'samples': [], 'timestamps': [], 'condition':{'Fastened': 0, 'Unfastened': 1, 'Not_used': 2, 'Invalid': 3}},
                    
                    # 'ACCButtInfo_main': {'samples': [], 'timestamps': [], 'condition':{'No_request': 0, 'Request': 1, 'key': 2, 'key': 3}},
                    # 'ACCButtInfo_cancel': {'samples': [], 'timestamps': [], 'condition':{'No_request': 0, 'Request': 1, 'key': 2, 'key': 3}}
                }
                data_for_AEB = self.find_odometer([x-signal_for_AEB.timestamps.tolist()[0] for x in signal_for_AEB.timestamps.tolist()],signal_for_AEB)
                # 1 {'samples': [], 'timestamps': []}
                #0=No request    1=Request
                for sample in data_for_AEB['samples']:
                    if sample == b'No request':
                        data_dict['AEB']['samples'].append(0)
                    elif sample == b'Request':
                        data_dict['AEB']['samples'].append(1)
                    else:
                        data_dict['AEB']['samples'].append(-1)
                # 2  0=Not active  1=Active
                data_for_VDC = self.find_odometer([x-signal_for_VDC.timestamps.tolist()[0] for x in signal_for_VDC.timestamps.tolist()],signal_for_VDC)
                for sample in data_for_VDC['samples']:
                    if sample == b'Not active':
                        data_dict['VDC']['samples'].append(0)
                    elif sample == b'Active':
                        data_dict['VDC']['samples'].append(1)
                    else:
                        data_dict['VDC']['samples'].append(-1)
                # 3  0=Not active  1=Active
                data_for_ABS = self.find_odometer([x-signal_for_ABS.timestamps.tolist()[0] for x in signal_for_ABS.timestamps.tolist()],signal_for_ABS)
                for sample in data_for_ABS['samples']:
                    if sample == b'Not active':
                        data_dict['ABS']['samples'].append(0)
                    elif sample == b'Active':
                        data_dict['ABS']['samples'].append(1)
                    else:
                        data_dict['ABS']['samples'].append(-1)
                # 4  0=On 1=Off
                data_for_TCS_activate = self.find_odometer([x-signal_for_TCS_Activate.timestamps.tolist()[0] for x in signal_for_TCS_Activate.timestamps.tolist()],signal_for_TCS_Activate)
                for sample in data_for_TCS_activate['samples']:
                    if sample == b'On':
                        data_dict['TCS_Activate']['samples'].append(0)
                    elif sample == b'Off':
                        data_dict['TCS_Activate']['samples'].append(1)
                    else:
                        data_dict['TCS_Activate']['samples'].append(-1)
                # 5  BCS_HDCCtrlSt
                """
                0=Off
                1=On active braking
                2=On not active braking
                3=Not used
                """
                data_for_HDC = self.find_odometer([x-signal_for_HDC.timestamps.tolist()[0] for x in signal_for_HDC.timestamps.tolist()],signal_for_HDC)
                for sample in data_for_HDC['samples']:
                    if sample == b'Off':
                        data_dict['HDC']['samples'].append(0)
                    elif sample == b'On active braking':
                        data_dict['HDC']['samples'].append(1)
                    elif sample == b'On not active braking':
                        data_dict['HDC']['samples'].append(2)
                    else:
                        data_dict['HDC']['samples'].append(-1)
                # 6  EBB_BrkPedalApplied
                """
                0=Brake pedal not applied
                1=Brake pedal applied
                """
                data_for_EPB = self.find_odometer([x-signal_for_EPB.timestamps.tolist()[0] for x in signal_for_EPB.timestamps.tolist()],signal_for_EPB)
                for sample in data_for_EPB['samples']:
                    if sample == b'Brake pedal not applied':
                        data_dict['EPB']['samples'].append(0)
                    elif sample == b'Brake pedal applied':
                        data_dict['EPB']['samples'].append(1)
                    else:
                        data_dict['EPB']['samples'].append(-1)
                # 7  EBB_BrkPedalApplied
                """
                0=Not active
                1=Released
                2=Applied
                3=Not used
                """
                data_for_cycle = self.find_odometer([x-signal_for_cycle.timestamps.tolist()[0] for x in signal_for_cycle.timestamps.tolist()],signal_for_cycle)
                for sample in data_for_cycle['samples']:
                    if sample == b'Not active':
                        data_dict['cycle']['samples'].append(0)
                    elif sample == b'Released':
                        data_dict['cycle']['samples'].append(1)
                    elif sample == b'Applied':
                        data_dict['cycle']['samples'].append(2)
                    elif sample == b'Not used':
                        data_dict['cycle']['samples'].append(3)
                    else:
                        data_dict['cycle']['samples'].append(-1)
                # 8 VCU_VehRdySt
                """
                0=Not ready
                1=Ready
                """
                data_for_engine = self.find_odometer([x-signal_for_engine.timestamps.tolist()[0] for x in signal_for_engine.timestamps.tolist()],signal_for_engine)
                for sample in data_for_engine['samples']:
                    if sample == b'Not ready':
                        data_dict['engine']['samples'].append(0)
                    elif sample == b'Ready':
                        data_dict['engine']['samples'].append(1)
                    else:
                        data_dict['engine']['samples'].append(-1)
                # 9 BCS_BrakeOverHeat
                """
                0=Not high
                1=Temp too high
                """
                data_for_BrakeOverHeat = self.find_odometer([x-signal_for_BrakeOverHeat.timestamps.tolist()[0] for x in signal_for_BrakeOverHeat.timestamps.tolist()],signal_for_BrakeOverHeat)
                for sample in data_for_BrakeOverHeat['samples']:
                    if sample == b'Not high':
                        data_dict['BrakeOverHeat']['samples'].append(0)
                    elif sample == b'Temp too high':
                        data_dict['BrakeOverHeat']['samples'].append(1)
                    else:
                        data_dict['BrakeOverHeat']['samples'].append(-1)
                # 10 FRR_ErrSt
                """
                0x0=on
                0x1=sensor blocked
                0x2= Temporary Error
                0x3=System Error
                """
                data_for_Front_angle_radar = self.find_odometer([x-signal_for_Front_angle_radar.timestamps.tolist()[0] for x in signal_for_Front_angle_radar.timestamps.tolist()],signal_for_Front_angle_radar)
                for sample in data_for_Front_angle_radar['samples']:
                    if sample == b'on':
                        data_dict['Front_angle_radar']['samples'].append(0)
                    elif sample == b'sensor blocked':
                        data_dict['Front_angle_radar']['samples'].append(1)
                    elif sample == b'Temporary Error':
                        data_dict['Front_angle_radar']['samples'].append(2)
                    elif sample == b'System Error':
                        data_dict['Front_angle_radar']['samples'].append(3)
                    else:
                        data_dict['Front_angle_radar']['samples'].append(-1)

                # 11 BCS_VDCOff
                """
                0=On
                1=Off
                """
                data_for_ESP = self.find_odometer([x-signal_for_ESP.timestamps.tolist()[0] for x in signal_for_ESP.timestamps.tolist()],signal_for_ESP)
                for sample in data_for_ESP['samples']:
                    if sample == b'On':
                        data_dict['ESP']['samples'].append(0)
                    elif sample == b'Off':
                        data_dict['ESP']['samples'].append(1)
                    else:
                        data_dict['ESP']['samples'].append(-1)
                # 11 BCS_TCSOff
                """
                0=On
                1=Off
                """
                data_for_TCS_Off = self.find_odometer([x-signal_for_TCS_Off.timestamps.tolist()[0] for x in signal_for_TCS_Off.timestamps.tolist()],signal_for_TCS_Off)
                for sample in data_for_TCS_Off['samples']:
                    if sample == b'On':
                        data_dict['TCS_Off']['samples'].append(0)
                    elif sample == b'Off':
                        data_dict['TCS_Off']['samples'].append(1)
                    else:
                        data_dict['TCS_Off']['samples'].append(-1)
                # 12 BCS_FLWheelRotatedDirection
                """
                0=Forward
                1=Backward
                """
                data_for_FLWheelRotated = self.find_odometer([x-signal_for_FL.timestamps.tolist()[0] for x in signal_for_FL.timestamps.tolist()],signal_for_FL)
                for sample in data_for_FLWheelRotated['samples']:
                    if sample == b'Forward':
                        data_dict['FLWheelRotated']['samples'].append(0)
                    elif sample == b'Backward':
                        data_dict['FLWheelRotated']['samples'].append(1)
                    else:
                        data_dict['FLWheelRotated']['samples'].append(-1)
                # 13 BCS_RLWheelRotatedDirection
                """
                0=Forward
                1=Backward
                """
                data_for_RLWheelRotated = self.find_odometer([x-signal_for_RL.timestamps.tolist()[0] for x in signal_for_RL.timestamps.tolist()],signal_for_RL)
                for sample in data_for_RLWheelRotated['samples']:
                    if sample == b'Forward':
                        data_dict['RLWheelRotated']['samples'].append(0)
                    elif sample == b'Backward':
                        data_dict['RLWheelRotated']['samples'].append(1)
                    else:
                        data_dict['RLWheelRotated']['samples'].append(-1)
                # 14 BCS_FRWheelRotatedDirection
                """
                0=Forward
                1=Backward
                """
                data_for_FRWheelRotated = self.find_odometer([x-signal_for_FR.timestamps.tolist()[0] for x in signal_for_FR.timestamps.tolist()],signal_for_FR)
                for sample in data_for_FRWheelRotated['samples']:
                    if sample == b'Forward':
                        data_dict['FRWheelRotated']['samples'].append(0)
                    elif sample == b'Backward':
                        data_dict['FRWheelRotated']['samples'].append(1)
                    else:
                        data_dict['FRWheelRotated']['samples'].append(-1)
                # 15 BCS_RRWheelRotatedDirection
                """
                0=Forward
                1=Backward
                """
                data_for_RRWheelRotated = self.find_odometer([x-signal_for_RR.timestamps.tolist()[0] for x in signal_for_RR.timestamps.tolist()],signal_for_RR)
                for sample in data_for_RRWheelRotated['samples']:
                    if sample == b'Forward':
                        data_dict['RRWheelRotated']['samples'].append(0)
                    elif sample == b'Backward':
                        data_dict['RRWheelRotated']['samples'].append(1)
                    else:
                        data_dict['RRWheelRotated']['samples'].append(-1)
                # 16 BCS_NoBrakeForce
                """
                0=Exist brake force
                1=No brakeforce

                """
                data_for_NoBrakeForce = self.find_odometer([x-signal_for_NoBrakeForce.timestamps.tolist()[0] for x in signal_for_NoBrakeForce.timestamps.tolist()],signal_for_NoBrakeForce)
                for sample in data_for_NoBrakeForce['samples']:
                    if sample == b'Exist brake force':
                        data_dict['NoBrakeForce']['samples'].append(0)
                    elif sample == b'No brakeforce':
                        data_dict['NoBrakeForce']['samples'].append(1)
                    else:
                        data_dict['NoBrakeForce']['samples'].append(-1)
                # 17 MRR_ACCMode
                """
                0=Off mode
                1=passive mode
                2=Standby mode
                3=Active control mode
                4=Brake only mode
                5=Override
                6=Not used
                7=Failure mode

                """
                data_for_Over_ride = self.find_odometer([x-signal_for_Over_ride.timestamps.tolist()[0] for x in signal_for_Over_ride.timestamps.tolist()],signal_for_Over_ride)
                for sample in data_for_Over_ride['samples']:
                    if sample == b'Off mode':
                        data_dict['Over_ride']['samples'].append(0)
                    elif sample == b'passive mode':
                        data_dict['Over_ride']['samples'].append(1)
                    elif sample == b'Standby mode':
                        data_dict['Over_ride']['samples'].append(2)
                    elif sample == b'Active control mode':
                        data_dict['Over_ride']['samples'].append(3)
                    elif sample == b'Brake only mode':
                        data_dict['Over_ride']['samples'].append(4)
                    elif sample == b'Override':
                        data_dict['Over_ride']['samples'].append(5)
                    elif sample == b'Not used':
                        data_dict['Over_ride']['samples'].append(6)
                    elif sample == b'Failure mode':
                        data_dict['Over_ride']['samples'].append(7)
                    else:
                        data_dict['Over_ride']['samples'].append(-1)
                # 18 VCU_CrntGearLvl
                '''
                0=Invalid
                1='D' Drive gear
                2='N' Neutral gear
                3='R' Reverse gear
                4='P' Park gear
                5=Not used
                6=Not used
                7=Not used
                '''
                data_for_GearLvl = self.find_odometer([x-signal_for_GearLvl.timestamps.tolist()[0] for x in signal_for_GearLvl.timestamps.tolist()],signal_for_GearLvl)
                for sample in data_for_GearLvl['samples']:
                    if sample == b'Invalid':
                        data_dict['GearLvl']['samples'].append(0)
                    elif sample == b"'D' Drive gear":
                        data_dict['GearLvl']['samples'].append(1)
                    elif sample == b"'N' Neutral gear":
                        data_dict['GearLvl']['samples'].append(2)
                    elif sample == b"'R' Reverse gear":
                        data_dict['GearLvl']['samples'].append(3)
                    elif sample == b"'P' Park gear":
                        data_dict['GearLvl']['samples'].append(4)
                    else:
                        data_dict['GearLvl']['samples'].append(-1)
                # 19 BCM_DriverDoorAjarSt
                '''
                0=Closed
                1=Open

                '''
                data_for_Door = self.find_odometer([x-signal_for_Door.timestamps.tolist()[0] for x in signal_for_Door.timestamps.tolist()],signal_for_Door)
                for sample in data_for_Door['samples']:
                    if sample == b'Closed':
                        data_dict['Door']['samples'].append(0)
                    elif sample == b"Open":
                        data_dict['Door']['samples'].append(1)
                    else:
                        data_dict['Door']['samples'].append(-1)
                # 20 SRS_DriverSeatBeltSt
                '''
                0=Fastened
                1=Unfastened
                2=Not used
                3=Invalid
                '''
                data_for_SeatBelt = self.find_odometer([x-signal_for_SeatBelt.timestamps.tolist()[0] for x in signal_for_SeatBelt.timestamps.tolist()],signal_for_SeatBelt)
                for sample in data_for_SeatBelt['samples']:
                    if sample == b'Fastened':
                        data_dict['SeatBelt']['samples'].append(0)
                    elif sample == b"Unfastened":
                        data_dict['SeatBelt']['samples'].append(1)
                    elif sample == b"Not used":
                        data_dict['SeatBelt']['samples'].append(2)
                    elif sample == b"Invalid":
                        data_dict['SeatBelt']['samples'].append(3)
                    else:
                        data_dict['SeatBelt']['samples'].append(-1)
                
                
                ##########################################################
                # ?
                # 21 EMS_ACCButtInfo
                '''
                Bit0: main switch
                0=not press
                1=press
                Bit1: cancel switch
                0=not press
                1=press
                Bit2: set switch
                0=not press
                1=press
                Bit3: resume switch
                0=not press
                1=press
                Bit4: distance switch
                0=not press
                1=press
                Bit5: Not used
                Bit6: Not used
                Bit7: button status
                0=Normal
                1=Abnormal
                '''
                # data_for_ACCButtInfo_main = self.find_odometer([x-signal_for_ACCButtInfo_main.timestamps.tolist()[0] for x in signal_for_ACCButtInfo_main.timestamps.tolist()],signal_for_ACCButtInfo_main)
                # for sample in data_for_ACCButtInfo_main['samples']:
                #     if sample == b'':
                #         data_dict['ACCButtInfo_main']['samples'].append(0)
                #     elif sample == b"":
                #         data_dict['ACCButtInfo_main']['samples'].append(1)
                #     elif sample == b"":
                #         data_dict['ACCButtInfo_main']['samples'].append(2)
                #     elif sample == b"":
                #         data_dict['ACCButtInfo_main']['samples'].append(3)
                #     else:
                #         data_dict['ACCButtInfo_main']['samples'].append(-1)
                # 22 EMS_ACCButtInfo
                '''
                Bit0: main switch
                0=not press
                1=press
                Bit1: cancel switch
                0=not press
                1=press
                Bit2: set switch
                0=not press
                1=press
                Bit3: resume switch
                0=not press
                1=press
                Bit4: distance switch
                0=not press
                1=press
                Bit5: Not used
                Bit6: Not used
                Bit7: button status
                0=Normal
                1=Abnormal
                '''
                # data_for_ACCButtInfo_cancel = self.find_odometer([x-signal_for_ACCButtInfo_cancel.timestamps.tolist()[0] for x in signal_for_ACCButtInfo_cancel.timestamps.tolist()],signal_for_ACCButtInfo_cancel)
                # for sample in data_for_ACCButtInfo_cancel['samples']:
                #     if sample == b'':
                #         data_dict['ACCButtInfo_cancel']['samples'].append(0)
                #     elif sample == b"":
                #         data_dict['ACCButtInfo_cancel']['samples'].append(1)
                #     elif sample == b"":
                #         data_dict['ACCButtInfo_cancel']['samples'].append(2)
                #     elif sample == b"":
                #         data_dict['ACCButtInfo_cancel']['samples'].append(3)
                #     else:
                #         data_dict['ACCButtInfo_cancel']['samples'].append(-1)
                #######################################################
                
                
                # print(signal_for_VDC)
                # print(signal_for_ABS)
                # print(signal_for_TCS)
                # print(signal_for_HDC)
                # print(signal_for_EPB)
                # print(signal_for_cycle)
                # print(signal_for_engine)
                # print(signal_for_BrakeOverHeat)
                # print(signal_for_Front_angle_radar)
                # print(signal_for_ESP)
                # print(signal_for_TCS)
                # print(signal_for_FL)
                # print(signal_for_RL)
                # print(signal_for_FR)
                # print(signal_for_RR)
                # print(signal_for_NoBrakeForce)
                # print(signal_for_Over_ride)
                # print(signal_for_GearLvl)
                # print(signal_for_Door)
                # print(signal_for_SeatBelt)
                # print(signal_for_ACCButtInfo_main)
                # print(signal_for_ACCButtInfo_cancel)
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
                        if i != 7 and i != 18:
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
                this_data['Final_resule'] = message_list
                
                print(this_data)
                this_data.to_csv('./resule_data.csv')
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
    # file_list = file_path_list(base_file_path)
    file_list = [r'G:\loc\szh\DA\Driving\System_APP\02_GAC\01_A18\BAP\000_dataexchange\20201112_6914_in_out_ramp\GAC_A18_2020-11-12_11-32_37_0005.MF4']
    i = 0
    while i < 1:
        i += 1
        try:
            file_path = file_list.pop()
            print(file_path)
        except IndexError as e:
            break
        else:
            file_name = file_path.split('\\')[-1].split('.')[0]
            mf = openMDF(r'G:\loc\szh\DA\Driving\System_APP\02_GAC\01_A18\BAP\000_dataexchange\20201112_6914_in_out_ramp\GAC_A18_2020-11-12_11-32_37_0005.MF4')
            mf.task()
