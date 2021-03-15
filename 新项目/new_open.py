from multiprocessing import Pool
from asammdf import MDF
from decimal import Decimal
import json
import os,re
import time
import asyncio
import asyncio
import numpy
import shutil
import pymysql
import copy
# 文件大小获取函数
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)
    return round(fsize, 2)
# 获取最相近的数据
def index_number(li,defaultnumber):
    select = Decimal(str(defaultnumber)) - Decimal(str(li[0]))
    index = 0
    if defaultnumber < (li[-2] + 0.5):
        for i in range(1, len(li) - 2):
            select2 = Decimal(str(defaultnumber)) - Decimal(str(li[i]))
            if (abs(select) > abs(select2)):
                select = select2
                index = i
    else:
        index = len(li) -1
    return  index

# 总里程和时间
all_odometer = 0
all_time = 0

class openMDF:
    def __init__(self, path, roadtype=0):
        self.filename = path.split('/')[-1].split('.')[0]
        self.roadType = roadtype
        if self.filename not in loser_file_data:
            self.open_file(path)
            self.task_1()
    def open_file(self, path):
        print('开启mf4文件')
        self.mf = MDF(path)
    def close_file(self):
        print('关闭mf4文件')
        self.mf.close()

    # 统计转向灯开启时间
    def task_1(self):
        signal_left = '_g_PL_AD_fw_PL_AD_FCT_RunnableSppHmi_RunnableSppHmi_m_sppHmiInput_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_dirIndL'
        signal_right = '_g_PL_AD_fw_PL_AD_FCT_RunnableSppHmi_RunnableSppHmi_m_sppHmiInput_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_dirIndR'
        signal_speed = '_g_PL_AD_fw_PL_AD_FCT_RunnableFsm_RunnableFsm._m_fsmController._m_fip._m_displayedSpeedCalculator._m_displaySpeed._m_value'
        # 轮端转角
        signal_RoadWheelAngle = '_g_PL_AD_fw_VMC_VMC_FW_MvpVse_VseSes_VseSes_m_portVehicleStateEstimation_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_estimation_RoadWheelAngle_Front._m_value'
        # 左航向角
        Left_heading_angle_signal = '_g_GAC_A18_NET_net_apl_g_netRunnable_rbCanRxLD_serializer_m_CNetVFC_Line_SenderPort_1_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_vfc_lineInformation._0_._VFC_Line_HeadingAngle'
        # 左侧车道线
        Left_lane_line_signal = '_g_GAC_A18_NET_net_apl_g_netRunnable_rbCanRxLD_serializer_m_CNetVFC_Line_SenderPort_1_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_vfc_lineInformation._0_._VFC_Line_Dy'
        # 右航向角
        Right_heading_angle_signal = '_g_GAC_A18_NET_net_apl_g_netRunnable_rbCanRxLD_serializer_m_CNetVFC_Line_SenderPort_1_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_vfc_lineInformation._1_._VFC_Line_HeadingAngle'
        # 右侧车道线
        Right_lane_line_signal = '_g_GAC_A18_NET_net_apl_g_netRunnable_rbCanRxLD_serializer_m_CNetVFC_Line_SenderPort_1_local.TChangeableMemPool._._._m_arrayPool._0_._elem._m_vfc_lineInformation._1_._VFC_Line_Dy'
        # vxvRef
        vxvRef_signal = '_g_PL_AD_fw_DACoreCyclic_HV_PerPmeRunnable_PerPmeRunnable_m_pmePort_out_local.TChangeableMemPool._._._m_arrayPool._0_._elem._vxvRef_sw'
        odometer_signal = 'ICM_TotalOdometer'


        # Line ID    255
        left_line_signal = 'VFC_Line01_LineID'
        right_line_signal = 'VFC_Line02_LineID'

        if self.mf:
            try:
                left = self.mf.get(signal_left)
                right = self.mf.get(signal_right)
                speed = self.mf.get(signal_speed)
                RoadWheelAngle = self.mf.get(signal_RoadWheelAngle).samples.tolist()
                Left_heading_angle = self.mf.get(Left_heading_angle_signal).samples.tolist()
                Left_lane_line = self.mf.get(Left_lane_line_signal).samples.tolist()
                Right_heading_angle = self.mf.get(Right_heading_angle_signal).samples.tolist()
                Right_lane_line = self.mf.get(Right_lane_line_signal).samples.tolist()
                vxvRef = self.mf.get(vxvRef_signal)
                odometer = self.mf.get(odometer_signal)
                left_line = self.mf.get(left_line_signal).samples.tolist()
                right_line = self.mf.get(right_line_signal).samples.tolist()
            except Exception as e:
                print(e)
                loser_file_data.append(self.filename)
            else:
                lane = 0
                for i in range(len(Left_lane_line)-1):
                    if abs((Left_lane_line[i] - Left_lane_line[i+1]) * 0.015625 -32) >= 2.4:
                        lane = 1
                        break
                if lane == 0:
                    return
                else:
                    def func(data):
                        num = data.samples.tolist()[0]
                        index_list = [0]
                        for index in range(len(data.samples.tolist())):
                            if num != data.samples.tolist()[index]:
                                num = data.samples.tolist()[index]
                                index_list.append(index)
                        if len(data.samples.tolist())-1 not in index_list:
                            index_list.append(len(data.samples.tolist())-1)
                        return index_list