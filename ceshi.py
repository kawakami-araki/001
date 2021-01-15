import pandas as pd
import time
#将时间字符串转换为10位时间戳，时间字符串默认为2017-10-01 13:37:04格式
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp









def func(path):
    try:
        feature = pd.read_excel(path)
    except:
        return False
    vin_list = []
    columns_list = feature.columns.tolist()
    # print(columns_list)
    all_data = {}
    for i in feature.index.tolist():
        a_data = feature.loc[i]
        data = {}
        if a_data[1] in all_data.keys():
            pass
        else:
            all_data[a_data[1]] = {}
        for m in range(len(columns_list)):
            if columns_list[m] not in all_data[a_data[1]].keys():
                all_data[a_data[1]][columns_list[m]] = []
            if str(a_data[m]) == '':
                continue
            if m in [2,3,6]:
                if ',' not in str(a_data[m]):
                    all_data[a_data[1]][columns_list[m]].append(a_data[m])
                    continue
                if str(a_data[m]) == 'nan':
                    all_data[a_data[1]][columns_list[m]].append(a_data[m])
                    continue
                data_list = a_data[m].split(',')
                if len(data_list) == 10:
                    pass
                else:
                    for n in range(10 - len(data_list)):
                        data_list.append(0)
                all_data[a_data[1]][columns_list[m]].extend(data_list)
            elif m == 0:
                all_data[a_data[1]][columns_list[m]].append(date_to_timestamp(a_data[m]))
            elif m == 9:
                all_data[a_data[1]][columns_list[m]].append(float(a_data[m]) if str(a_data[m]) != 'nan' else 0)

            else:
                new_data = []
                for n in range(10):
                    new_data.insert(0, a_data[m])
                all_data[a_data[1]][columns_list[m]].extend(new_data)
    for i in all_data.keys():
        for j in all_data[i].keys():
            if type(all_data[i][j]) == type([]):
                this_value = all_data[i][j]
                this_value.reverse()
                all_data[i][j] = this_value
            if j == 'time':
                new_date_list = []
                for t in all_data[i][j]:
                    new_date= []
                    now_date = t
                    for index in range(10):
                        new_date.append(now_date)
                        now_date += 1
                    new_date_list.extend(new_date)
                all_data[i][j] = new_date_list
            if j == 'ICM_TotalOdometer':
                data_list = []
                index_list = []
                for k in range(len(all_data[i][j])):
                    if all_data[i][j][k] == 0:
                        data_list.append(0)
                        index_list.append(k)
                    else:
                        if index_list != []:
                            for o in range(len(index_list)):
                                data_list[index_list.pop()] = all_data[i][j][k]
                        data_list.append(all_data[i][j][k])
                new_data_list = []
                for o in data_list:
                    for m in range(10):
                        new_data_list.append(o)
                all_data[i][j] = new_data_list


    def split_data(file_data):
        temp = []
        split_list_samples = []
        split_list_timestamps = []
        # Function change record
        for i in range(len(file_data['BCS_VehSpd'])):
            if i < len(file_data['BCS_VehSpd']):
                if float(file_data['BCS_VehSpd'][i]) < 80:
                    if i == 0:
                        continue
                    temp.append(i)
        temp.append(len(file_data['BCS_VehSpd']))
        # Functional state segmentation
        index_list = [x for x in range(len(file_data['BCS_VehSpd']))]
        for j in range(len(temp)-1):
            if j == 0:
                if temp[j] - 0 >= 30:
                    split_list_samples.append(file_data['BCS_VehSpd'][:temp[j+1]])
                    split_list_timestamps.append(index_list[:temp[j+1]])
            if temp[j+1] - temp[j] >= 30:
                split_list_samples.append(file_data['BCS_VehSpd'][temp[j]+1:temp[j+1]])
                split_list_timestamps.append(index_list[temp[j]+1:temp[j+1]])
        return (split_list_samples, split_list_timestamps)

    all_odometter = 0
    # TJA 总时长/开启时长
    TJA_all_time = 0
    TJA_all_time_as_activate = 0
    # LightBar 总时长/开启时长
    LightBar_all_time = 0
    LightBar_all_time_as_open = 0
    LB_odo = 0
    
    tja_open_odo = 0
    import numpy as np
    for key,value in all_data.items():
        spd_list, index_list = split_data(value)
        # 总历程
        for index in index_list:
            # 速度区间内总里程
            all_odometter += abs(value['ICM_TotalOdometer'][index[-1]] - value['ICM_TotalOdometer'][index[0]])
            all_odo = value['ICM_TotalOdometer'][index[0]:index[-1]]
            all_open_TJA = value['IFC_TJA_ICA_St'][index[0]:index[-1]]
            TJA_all_time += len(all_open_TJA)
            all_open_lightBar = value['ADAS_HWAHF_Lightbar'][index[0]:index[-1]]
            
            lightBar_index_list =[]
            tja_open_index = []
            for tja_index in range(len(all_open_TJA)):
                if str(all_open_TJA[tja_index]) == 'nan':
                    continue
                if int(all_open_TJA[tja_index]) in [2, 3]:
                    tja_open_index.append(tja_index)
                    TJA_all_time_as_activate += 1
                    LightBar_all_time += 1
                    if int(all_open_lightBar[tja_index]) == 1:
                        LightBar_all_time_as_open += 1
                        lightBar_index_list.append(tja_index)
            odo_index = []
            if lightBar_index_list == []:
                pass
            else:
                sum = 0
                for lB_index in range(len(lightBar_index_list)-1):
                    if lightBar_index_list[lB_index]+1-lightBar_index_list[lB_index+1]==0:
                        sum+=1
                    else:
                        if sum > 0:
                            odo_index.append([lightBar_index_list[lB_index-sum-1],lightBar_index_list[lB_index]])
                            sum = 0
            
            for odo in odo_index:
                this_odo = all_odo[odo[1]] - all_odo[odo[0]]
                LB_odo += abs(this_odo)
            tja_odo_index = []
            if tja_open_index == []:
                pass
            else:
                sum = 0
                for index in range(len(tja_open_index)-1):
                    if tja_open_index[index]+1-tja_open_index[index+1]==0:
                        sum+=1
                    else:
                        if sum > 0:
                            tja_odo_index.append([tja_open_index[index-sum-1],tja_open_index[index]])
                            sum = 0
            odo_list = []
            for odo in tja_odo_index:
                a_list = [all_odo[odo[1]], all_odo[odo[0]]]
                if a_list not in odo_list:
                    a_list.reverse()
                    if a_list not in odo_list:                    
                        odo_list.append(a_list)
            for split_odo in odo_list:
                tja_odo = abs(split_odo[1] - split_odo[0])
                tja_open_odo += tja_odo
                # if tja_odo > 10:
                #     print(split_odo)
        print([all_odometter,TJA_all_time,TJA_all_time_as_activate,tja_open_odo,LightBar_all_time,LightBar_all_time_as_open,LB_odo])
    return [all_odometter,TJA_all_time,TJA_all_time_as_activate,tja_open_odo,LightBar_all_time,LightBar_all_time_as_open,LB_odo]
import os

# 获取全部的文件路径
def file_path_list(path):
    '''
    parms: {path} Base path address
    '''
    file_list = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if i.endswith('xlsx'):
                file_list.append(os.path.join(root,i))
    return file_list
if __name__ == "__main__":
    for folder in [r'C:\Users\FAC2SZH\Desktop\excel\11',r'C:\Users\FAC2SZH\Desktop\excel\12',r'C:\Users\FAC2SZH\Desktop\excel\1']:
        file_list = file_path_list(folder)
        file_data = []
        file_name_list = []
        while True:
            try:
                file_path = file_list.pop()
            except IndexError as e:
                break
            else:
                print(file_path)
                data = func(file_path)
                if data:
                    file_data.append(data)
                    file_name_list.append(file_path.split('\\')[-1].split('.')[0])
        # all_odometter,TJA_all_time,TJA_all_time_as_activate,LightBar_all_time,LightBar_all_time_as_open,LB_odo
        new_pd = pd.DataFrame(
            file_data,
            columns=[
                'Total mileage', 'TJA available time', 'TJA usage duration','TJA mileage', 'LightBar available time', 'LightBar usage duration', 'LightBar open mileage'
                ],index=file_name_list)
        folder_name = folder.split('\\')[-1]
        new_pd.to_csv('./{}.csv'.format(folder_name))




















# for key,value in all_data.items():
#     for i in value.values():
#         print(len(i))
#     break
    # ['2020-09-01 09:14:14', 'LNAB1AB35L5503315', '0,0,1.125,1.29375,1.8,1.63125,1.40625,0,1.63125,0', '0,0,0,0,0,0,0,0,0,0', nan, 36.67252777108737, '0,0,0,0,0,0,0,0,0,0', '0,0', 117.03077869656731, nan]