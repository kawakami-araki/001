import json
import os,re
import time
import asyncio
from asammdf import MDF
import asyncio
from multiprocessing import Pool
import numpy
import shutil
import pymysql
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)
    return round(fsize, 2)
time_1 = [0.5*x for x in range(1,21)]
time_1.append('10<')
# 没有数据的文件的名称
if os.path.exists('./loser_file.json'):
    with open('./loser_file.json', 'r') as f:
        loser_file_data = json.load(f)
else:
    loser_file_data = []

if os.path.exists('./result_data.json'):
    with open('./result_data.json', 'r') as f:
        result_dict = json.load(f)
else:
    result_dict = {
        '0~40':{'left':[0,[]],'right':[0,[]]},
        '40-60':{'left':[0,[]],'right':[0,[]]},
        '60-80':{'left':[0,[]],'right':[0,[]]},
        '80-100':{'left':[0,[]],'right':[0,[]]}
        }
if os.path.exists('./new_result_data.json'):
    with open('./new_result_data.json', 'r') as f:
        new_result_dict = json.load(f)
else:
    new_result_dict = {
        '0~40':[0 for x in time_1],
        '40-60':[0 for x in time_1],
        '60-80':[0 for x in time_1],
        '80-100':[0 for x in time_1]
    }
import copy
if os.path.exists('./mysql_data.json'):
    with open('./mysql_data.json', 'r') as f:
        mysql_data = json.load(f)
        mysql_data_1 = copy.deepcopy(mysql_data)
else:
    mysql_data = []
    mysql_data_1 = copy.deepcopy(mysql_data)
from decimal import Decimal
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
if os.path.exists('./Pre_prepared_data.json'):
    with open('./mysql_data.json', 'r') as f:
        Pre_prepared_data = json.load(f)
else:
    Pre_prepared_data = []
Line_pressing = []
# 总里程和时间
all_odometer = 0
all_time = 0


my_list = []




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
                print(len(Left_lane_line))
                print(len(left.samples.tolist()))
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
                # 处理数据长度问题  speed, vxvRef
                st = speed.timestamps.tolist()
                start_time = 0
                stop_time = -2
                # 计算差值
                left_data = []
                left_time = left.timestamps.tolist()

                old_spd = speed.samples.tolist()
                old_vxv = vxvRef.samples.tolist()
                old_spd_time = speed.timestamps.tolist()
                old_vxvRef = vxvRef.samples.tolist()
                new_spd = ['' for x in left_time]
                new_vxvRef = ['' for x in left_time]
                for tt in range(len(old_spd_time)):
                    this_index = index_number(left_time, old_spd_time[tt])
                    new_spd[this_index] = old_spd[tt]
                    new_vxvRef[this_index] = old_vxvRef[tt]
                for i in range(len(new_spd)):
                    if new_spd[i] == '':
                        if i==0:
                            if new_spd[i+1] != 0:
                                new_spd[i] = new_spd[i+1]
                            else:
                                new_spd[i] = 0
                        else:
                            new_spd[i] = new_spd[i-1]
                    if new_vxvRef[i] == '':
                        if i==0:
                            if new_vxvRef[i+1] != 0:
                                new_vxvRef[i] = new_vxvRef[i+1]
                            else:
                                new_vxvRef[i] = 0
                        else:
                            new_vxvRef[i] = new_vxvRef[i-1]
                left_index_list = func(left)
                right_index_list = func(right)
                if left_index_list == [] and right_index_list == []:
                    self.close_file()
                    return False
                new_data = {
                    'left': [],
                    'left_time': [],
                    'right': [],
                    'right_time': [],
                    'spd': [],
                    'wheel': [],
                    'Left_heading_angle': [],
                    'left_lane': [],
                    'Right_heading_angle': [],
                    'right_lane': [],
                    'vxvRef': [],
                    'left_line': [],
                    'right_line': []
                }
                # 
                for index in range(len(left_index_list)-1):
                    new_data['left'].append(left.samples.tolist()[left_index_list[index]:left_index_list[index+1]])
                    new_data['left_time'].append(left.timestamps.tolist()[left_index_list[index]:left_index_list[index+1]])
                    new_data['right'].append([])
                    new_data['right_time'].append([])
                    new_data['spd'].append(new_spd[left_index_list[index]:left_index_list[index+1]])
                    new_data['wheel'].append(RoadWheelAngle[left_index_list[index]:left_index_list[index+1]])

                    new_data['Left_heading_angle'].append(Left_heading_angle[left_index_list[index]:left_index_list[index+1]])
                    new_data['left_lane'].append(Left_lane_line[left_index_list[index]:left_index_list[index+1]])
                    new_data['Right_heading_angle'].append(Right_heading_angle[left_index_list[index]:left_index_list[index+1]])
                    new_data['right_lane'].append(Right_lane_line[left_index_list[index]:left_index_list[index+1]])
                    new_data['vxvRef'].append(new_vxvRef[left_index_list[index]:left_index_list[index+1]])
                    new_data['left_line'].append(left_line[left_index_list[index]:left_index_list[index+1]])
                    new_data['right_line'].append([])
                for index in range(len(right_index_list)-1):
                    new_data['left'].append([])
                    new_data['left_time'].append([])
                    new_data['right'].append(right.samples.tolist()[right_index_list[index]:right_index_list[index+1]])
                    new_data['right_time'].append(right.timestamps.tolist()[right_index_list[index]:right_index_list[index+1]])
                    new_data['spd'].append(new_spd[right_index_list[index]:right_index_list[index+1]])
                    new_data['wheel'].append(RoadWheelAngle[right_index_list[index]:right_index_list[index+1]])

                    new_data['Left_heading_angle'].append(Left_heading_angle[right_index_list[index]:right_index_list[index+1]])
                    new_data['left_lane'].append(Left_lane_line[right_index_list[index]:right_index_list[index+1]])
                    new_data['Right_heading_angle'].append(Right_heading_angle[right_index_list[index]:right_index_list[index+1]])
                    new_data['right_lane'].append(Right_lane_line[right_index_list[index]:right_index_list[index+1]])
                    new_data['vxvRef'].append(new_vxvRef[right_index_list[index]:right_index_list[index+1]])
                    new_data['left_line'].append([])
                    new_data['right_line'].append(right_line[right_index_list[index]:right_index_list[index+1]])
                # for key,value in new_data.items():
                #     print(len(value))
                # 车道线判断逻辑函数
                def func2(i,direction,speed,max_spd,min_spd):
                    print(direction)
                    return_data = 0
                    lane_list = []
                    overrun = []
                    for lane_line in range(len(new_data[f'{direction}_lane'][i])-1):
                        if new_data[f'{direction}_lane'][i][lane_line] == 2048:
                            print('无信号')
                            continue
                        this_num = new_data[f'{direction}_lane'][i][lane_line] * 0.015625 - 32
                        next_num = new_data[f'{direction}_lane'][i][lane_line + 1] * 0.015625 - 32
                        print(next_num - this_num)
                        if abs(next_num - this_num) >= 2.4:
                            lane_list.append(lane_line)
                    print(lane_list)
                    if lane_list != []:
                        if len(lane_list) > 1:
                            print('多次变道， 不做计算')
                        else:
                            print(f'单次变道{direction}')
                            new_lane = new_data[f'{direction}_lane'][i][lane_list[0]+1:]
                            this_len = int(len(new_lane)/5)
                            new_list = [sum(new_lane[:this_len])/len(new_lane[:this_len]),sum(new_lane[this_len:this_len*2])/len(new_lane[this_len:this_len*2]),sum(new_lane[this_len*2:this_len*3])/len(new_lane[this_len*2:this_len*3]),sum(new_lane[this_len*3:this_len*4])/len(new_lane[this_len*3:this_len*4]),sum(new_lane[this_len*4:])/len(new_lane[this_len*4:])]
                            if new_list[0] > new_list[1] > new_list[2] > new_list[3] > new_list[4]:
                                # 变道到车轮压线时间
                                Time_from_lighting_to_pressing_line = new_data[f'{direction}_time'][i][lane_list[0]] - new_data[f'{direction}_time'][i][0]
                                Line_pressing_data = [self.filename,speed,max_spd,min_spd,Time_from_lighting_to_pressing_line, self.roadType]
                                if Line_pressing_data not in Line_pressing:
                                    Line_pressing.append(Line_pressing_data)
                                    return_data = 1
                    else:
                        this_len = int(len(new_data[f'{direction}_lane'][i])/5)
                        new_list = [
                            sum(new_data[f'{direction}_lane'][i][:this_len])/len(new_data[f'{direction}_lane'][i][:this_len]),
                            sum(new_data[f'{direction}_lane'][i][this_len:this_len*2])/len(new_data[f'{direction}_lane'][i][this_len:this_len*2]),
                            sum(new_data[f'{direction}_lane'][i][this_len*2:this_len*3])/len(new_data[f'{direction}_lane'][i][this_len*2:this_len*3]),
                            sum(new_data[f'{direction}_lane'][i][this_len*3:this_len*4])/len(new_data[f'{direction}_lane'][i][this_len*3:this_len*4]),
                            sum(new_data[f'{direction}_lane'][i][this_len*4:])/len(new_data[f'{direction}_lane'][i][this_len*4:])]
                        if min(new_list) == new_list[-1] and new_data[f'{direction}_lane'][i] != new_data[f'{direction}_lane'][-1]:
                            this_lane_list = new_data[f'{direction}_lane'][i][this_len*4:]
                            if len(new_data[f'{direction}_lane'][i+1]) >= 200:
                                this_lane_list.extend(new_data[f'{direction}_lane'][i+1][:200])
                            else:
                                this_lane_list.extend(new_data[f'{direction}_lane'][i+1])
                            for lane_line in range(len(this_lane_list)-1):
                                if this_lane_list[lane_line] == 2048:
                                    print('无信号')
                                    continue
                                this_num = this_lane_list[lane_line] * 0.015625 - 32
                                next_num = this_lane_list[lane_line + 1] * 0.015625 - 32
                                print(next_num - this_num)
                                if abs(next_num - this_num) >= 2.4:
                                    lane_list.append(lane_line)
                            if lane_list != []:
                                if len(lane_list) > 1:
                                    print('多次变道， 不做计算')
                                else:
                                    print(f'单次变道{direction}')
                                    new_lane = new_data[f'{direction}_lane'][i][lane_list[0]+1:]
                                    this_len = int(len(new_lane)/5)
                                    new_list = [sum(new_lane[:this_len])/len(new_lane[:this_len]),sum(new_lane[this_len:this_len*2])/len(new_lane[this_len:this_len*2]),sum(new_lane[this_len*2:this_len*3])/len(new_lane[this_len*2:this_len*3]),sum(new_lane[this_len*3:this_len*4])/len(new_lane[this_len*3:this_len*4]),sum(new_lane[this_len*4:])/len(new_lane[this_len*4:])]
                                    if new_list[0] > new_list[1] > new_list[2] > new_list[3] > new_list[4]:
                                        # 变道到车轮压线时间
                                        Time_from_lighting_to_pressing_line = new_data[f'{direction}_time'][i][lane_list[0]] - new_data[f'{direction}_time'][i][0]
                                        Line_pressing_data = [self.filename,speed,max_spd,min_spd,Time_from_lighting_to_pressing_line, self.roadType]
                                        if Line_pressing_data not in Line_pressing:
                                            Line_pressing.append(Line_pressing_data)
                                            return_data = 1
                    return return_data
                    
                    
                def func3(key,i,speed,max_spd,min_spd,direction):
                    result_dict[key][direction][0] += 1
                    this_time = new_data['{}_time'.format(direction)][i][-1] - new_data['{}_time'.format(direction)][i][0]
                    #################################
                    this_index = index_number(time_1,this_time)
                    new_result_dict[key][this_index] += 1
                    #################################
                    mysql_data_sql = [self.filename,direction, speed,max_spd,min_spd, this_time, self.roadType]
                    if mysql_data_sql not in mysql_data:
                        mysql_data.append(mysql_data_sql)
                    #################################
                    result_dict[key][direction][1].append(this_time)
                # 数据规整完成， 长度一致，无变化
                for i in range(len(new_data['spd'])):
                    judgment_basis = 0
                    for j in new_data['wheel'][i]:
                        if j > 0.1:
                            judgment_basis = 1
                            break
                    if judgment_basis == 0:
                        try:
                            # 车速计算
                            speed = int(sum(new_data['spd'][i]))/len(new_data['spd'][i]) * 3.6
                            # 最大车速留档
                            max_spd = int(max(new_data['spd'][i])) * 3.6
                            # 最小车速留档
                            min_spd = int(min(new_data['spd'][i])) * 3.6
                        except IndexError:
                            break
                        else:
                            if speed >=80:
                                if 1 in new_data['left'][i] and 1 not in new_data['right'][i]:
                                    # 判断车道线情况
                                    # Time_from_lighting_to_pressing_line 为开启变道灯到压线的时间
                                    # 这里的判断逻辑需要重新计算， 考虑变道中跳变仅存在一次，并且确实变道完成
                                    # 如：
                                    # 1.跨过车道线完成跳变之后， 继续变动完成变道操作
                                    # 2.跨过车到线之后的数据迅速达到正常车位， 即车道线扣除车身之后最大值应该为60公分，否则视为未变道成功， 需要继续查看后续数据来判断
                                    lane = func2(i,'left',speed,max_spd,min_spd)
                                    # 车道线检测
                                    if lane == 1:
                                        func3('80-100',i,speed,max_spd,min_spd,'left')
                                elif 1 not in new_data['left'][i] and 1 in new_data['right'][i]:
                                    lane = func2(i,'right',speed,max_spd,min_spd)
                                    if lane == 1:
                                        
                                        func3('80-100',i,speed,max_spd,min_spd,'right')
                                else:
                                    continue
                            elif speed >=60:
                                if 1 in new_data['left'][i] and 1 not in new_data['right'][i]:
                                    # 判断车道线情况
                                    lane = func2(i,'left',speed,max_spd,min_spd)
                                    if lane == 1:
                                        func3('60-80',i,speed,max_spd,min_spd,'left')
                                elif 1 not in new_data['left'][i] and 1 in new_data['right'][i]:
                                    # 判断车道线情况
                                    lane = func2(i,'right',speed,max_spd,min_spd)
                                    if lane == 1:
                                        func3('60-80',i,speed,max_spd,min_spd,'right')
                                else:
                                    continue
                            elif speed >=40:
                                if 1 in new_data['left'][i] and 1 not in new_data['right'][i]:
                                    # 判断车道线情况
                                    lane = func2(i,'left',speed,max_spd,min_spd)
                                    if lane == 1:
                                        func3('40-60',i,speed,max_spd,min_spd,'left')
                                elif 1 not in new_data['left'][i] and 1 in new_data['right'][i]:
                                    # 判断车道线情况
                                    lane = func2(i,'right',speed,max_spd,min_spd)
                                    if lane == 1:
                                        func3('40-60',i,speed,max_spd,min_spd,'right')
                                else:
                                    continue
                            elif speed > 0:
                                if 1 in new_data['left'][i] and 1 not in new_data['right'][i]:
                                    # 判断车道线情况
                                    lane = func2(i,'left',speed,max_spd,min_spd)
                                    if lane == 1:
                                        func3('0~40',i,speed,max_spd,min_spd,'left')
                                elif 1 not in new_data['left'][i] and 1 in new_data['right'][i]:
                                    # 判断车道线情况
                                    lane = func2(i,'right',speed,max_spd,min_spd)
                                    if lane == 1:
                                        func3('0~40',i,speed,max_spd,min_spd,'right')
                                        # result_dict['0~40']['right'][1].append(this_time)
                                else:
                                    continue
                            else:
                                continue
                            
                            this_odometer = odometer.samples.tolist()
                            this_time = odometer.timestamps.tolist()
                            odo = this_odometer[-1] - this_odometer[0]
                            t = this_time[-1] - this_time[0]
                            global all_odometer
                            all_odometer += odo
                            global all_time
                            all_time += t
                self.close_file()
                return new_result_dict
            finally:
                self.close_file()
            
class OpenFile:
    def __init__(self,path):
        self.file_list = []
        for root,dirs,files in os.walk(path):
            for i in files:
                if i.endswith('.MF4'):
                    self.file_list.append(os.path.join(root,i))
def created_db(data):
    conn = pymysql.connect(host='10.178.229.1', port=3306, user='root', password='rbac2020',database='file_system')
    cursor = conn.cursor()
    sql = 'insert into cornering_lamps (file_name,direction,speed,duration,is_delete) values(%s,%s,%s,%s,0)'
    select_sql = 'select * from cornering_lamps where file_name=%s and direction=%s and speed=%s and duration=%s'
    for i in data:
        try:
            
            select_data = cursor.fetchall()
            if not cursor.execute(sql, (i[0],i[1],i[2],i[3])):
                cursor.execute(sql, (i[0],i[1],i[2],i[3]))
                conn.commit()
        except Exception as e:
            conn.rollback()# 发生错误时回滚
            print('提交失败：', i, e)
def created_db_2(data):
    conn = pymysql.connect(host='10.178.229.1', port=3306, user='root', password='rbac2020',database='file_system')
    print(data)
    cursor = conn.cursor()
    sql = 'insert into line_pressing (file_name,speed,time,is_delete) values(%s,%s,%s,0)'
    select_sql = 'select * from line_pressing where file_name=%s and speed=%s and time=%s'
    for i in data:
        try:
            
            select_data = cursor.fetchall()
            if not cursor.execute(sql, (i[0],i[1],i[2])):
                cursor.execute(sql, (i[0],i[1],i[2]))
                conn.commit()
        except Exception as e:
            conn.rollback()# 发生错误时回滚
            print('提交失败：', i, e)
if __name__ == "__main__":
    # base_file = [
    #     r'\\abtvdfs.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\01_GAC'
    # ]
    # all_file_list = []
    # if os.path.exists('./mf4_file_path.json'):
    #     with open('./mf4_file_path.json', 'r') as f:
    #         all_file_list = json.load(f)
    # else:
    #     for i in base_file:
    #         print('开始检索文件')
    #         new_file = OpenFile(i)
    #         file_list = new_file.file_list
    #         print(file_list)
    #         new_file_list = []
    #         for i in file_list:
    #             file_size = get_FileSize(i)
    #             if file_size > 500:
    #                 # new_file_list.append(i)
    #                 all_file_list.append(i)
    #     with open('./mf4_file_path.json', 'w', encoding='UTF-8') as f:
    #         print('开始写入文件')
    #         json.dump(all_file_list,f)
    file_list = [
    #{
    #    'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-15//GAC_A18_2020-09-15_11-55_17_0016.MF4', 'roadType': '1'
    #},
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-15//GAC_A18_2020-09-15_13-52_35_0028.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-15//GAC_A18_2020-09-15_13-48_35_0026.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-20//GAC_A18_2020-09-20_14-33_19_0035.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-20//GAC_A18_2020-09-20_14-21_19_0029.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-20//GAC_A18_2020-09-20_13-56_49_0017.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-20//GAC_A18_2020-09-20_13-47_15_0028.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-20//GAC_A18_2020-09-20_14-31_19_0034.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-15//GAC_A18_2020-09-15_13-46_35_0025.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-15//GAC_A18_2020-09-15_13-44_35_0024.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-15//GAC_A18_2020-09-15_11-59_17_0018.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-15//GAC_A18_2020-09-15_12-01_17_0019.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-15//GAC_A18_2020-09-15_12-03_17_0020.MF4', 'roadType': '1'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-18//GAC_A18_2020-09-18_14-17_49_0036.MF4', 'roadType': '2'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-18//GAC_A18_2020-09-18_14-19_49_0037.MF4', 'roadType': '2'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-17//GAC_A18_2020-09-17_10-43_50_0033.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-17//GAC_A18_2020-09-17_10-45_50_0034.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-17//GAC_A18_2020-09-17_10-47_50_0035.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-17//GAC_A18_2020-09-17_10-49_50_0036.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-17//GAC_A18_2020-09-17_13-05_38_0037.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-17//GAC_A18_2020-09-17_13-50_58_0017.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-17//GAC_A18_2020-09-17_13-53_29_0018.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-18//GAC_A18_2020-09-18_14-15_49_0035.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-19//GAC_A18_2020-09-19_12-55_50_0046.MF4', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-20//GAC_A18_2020-09-20_10-09_42_0018', 'roadType': '3'
    },
    {
        'path':'//abtvdfs.de.bosch.com//ismdfs//loc//szh//DA//Radar//05_Radar_ER//01_GAC//02_A18HF//7043C//20200915-20200923//A18-7043C_2020-09-20//GAC_A18_2020-09-20_10-11_42_0019.MF4', 'roadType': '3'
    }
]
    for path in file_list:
        file_name = path['path'].split('//')[-1]
        print(file_name)
        if os.path.exists(path['path']):
            print('该文件已存在， 不需要重复复制')
        else:
            continue
        if os.path.exists('./{}'.format(file_name)):
            print('该文件已存在， 不需要重复复制')
        else:
            shutil.copy(path['path'], './')
        om = openMDF('./{}'.format(file_name), path['roadType'])
        print(mysql_data)
        print(Line_pressing)
        # with open('./result_data.json', 'w', encoding='utf-8') as f:
        #     json.dump(result_dict, f)
        # with open('./new_result_data.json', 'w', encoding='utf-8') as f:
        #     json.dump(new_result_dict, f)
        # list3=list(set(mysql_data).difference(set(mysql_data_1)))
        # created_db(list3)
        # with open('./mysql_data.json', 'w', encoding='utf-8') as f:
        #     json.dump(mysql_data, f)
        #     mysql_data_1 = copy.deepcopy(mysql_data)
        # created_db_2(Line_pressing)
        # with open('./Pre_prepared_data.json', 'w', encoding='utf-8') as f:
        #     json.dump(Pre_prepared_data, f)
        # print('正在删除文件', file_name)
        # with open('./loser_file.json', 'w', encoding='utf-8') as f:
        #     json.dump(loser_file_data, f)
        # os.remove('./{}'.format(file_name))
    print(my_list)
    with open('./ceshi.json') as f:
        json.dump(my_list,f)