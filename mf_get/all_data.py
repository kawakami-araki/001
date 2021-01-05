from asammdf import MDF
import json,os,time,sys
import numpy as np
import pandas as pd
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
    # 0
    def task_0(self):
        try:
            odometer = self.mf.get('ICM_TotalOdometer')
        except:
            pass
        else:
            return odometer
    # 17
    def task_17(self):
        signal_1 = 'IFC_HMA_Enable'
        signal_2 = 'IFC_HMA_St'
        if self.mf:
            try:
                data_1 = self.mf.get(signal_1)
                data_2 = self.mf.get(signal_2)
                data_3 = self.task_0()
            except:
                return False
            else:
                data_list = {
                    'function_enabled_status': {'samples': [], 'timestamps': []},
                    'function_activation_status': {'samples': [], 'timestamps': []},
                    'odometer': {'samples': [], 'timestamps': []}
                }
                
                if data_1.samples.tolist() == []:
                    pass
                else:
                    for enabled_status in data_1.samples.tolist():
                        if enabled_status == b'Disable':
                            data_list['function_enabled_status']['samples'].append(0)
                        elif enabled_status == b'Enable':
                            data_list['function_enabled_status']['samples'].append(1)
                if data_1.timestamps.tolist() == []:
                    pass
                else:
                    data_list['function_enabled_status']['timestamps'] = (data_1.timestamps-data_1.timestamps[np.argmin(data_1.timestamps)]).tolist()
                if data_2.samples.tolist() == []:
                    pass
                else:
                for active_status in data_2.samples.tolist():
                    if active_status == b'HMA off':
                        data_list['function_activation_status']['samples'].append(0)
                    elif active_status == b'HMA standby':
                        data_list['function_activation_status']['samples'].append(1)
                    elif active_status == b'HMA active':
                        data_list['function_activation_status']['samples'].append(2)
                    elif active_status == b'HMA failure':
                        data_list['function_activation_status']['samples'].append(3)
                    elif active_status == b'Camera blocked':
                        data_list['function_activation_status']['samples'].append(4)
                
                if data_2.timestamps.tolist() == []:
                    pass
                else:
                    data_list['function_activation_status']['timestamps'] = (data_2.timestamps-data_2.timestamps[np.argmin(data_2.timestamps)]).tolist()
                
                if data_3.samples.tolist() == []:
                    pass
                else:
                    data_list['odometer']['samples'] = data_3.samples.tolist()
                if data_3.timestamps.tolist() == []:
                    pass
                else:
                    data_list['odometer']['timestamps'] = data_3.timestamps-data_3.timestamps[np.argmin(data_3.timestamps)].tolist()
                self.close_file()
                return data_list


    # 18
    def task_18(self):
        signal_1 = 'IFC_TSR_Enable'
        signal_2 = 'IFC_TSR_OperatingSt'
        signal_3 = 'IFC_TSR_AudioWarnEnable'
        if self.mf:
            try:
                data_1 = self.mf.get(signal_1)
                data_2 = self.mf.get(signal_2)
                data_3 = self.mf.get(signal_3)
                data_4 = self.task_0()
            except:
                return False
            else:
                data_list = {
                    'open_status': {'samples': [], 'timestamps': []},
                    'data': {'samples': [], 'timestamps': []},
                    'warn_status': {'samples': [], 'timestamps': []},
                    'odometer': {'samples': [], 'timestamps': []}
                }
                # 功能状态记录
                if data_1.samples.tolist() == []:
                    pass
                else:
                    for open_status in data_1.samples.tolist():
                        if open_status == b'Disable':
                            data_list['open_status']['samples'].append(0)
                        elif open_status == b'Enable':
                            data_list['open_status']['samples'].append(1)
                if data_1.timestamps.tolist() == []:
                    pass
                else:
                    data_list['open_status']['timestamps'] = (data_1.timestamps-data_1.timestamps[np.argmin(data_1.timestamps)]).tolist()
                if data_2.samples.tolist() == []:
                    pass
                else:
                    for functional_status in data_2.samples.tolist():
                        if functional_status == b'Off':
                            data_list['data']['samples'].append(0)
                        elif functional_status == b'Fusion mode':
                            data_list['data']['samples'].append(1)
                        elif functional_status == b'Vision only mode':
                            data_list['data']['samples'].append(2)
                        elif functional_status == b'Navigation only mode':
                            data_list['data']['samples'].append(3)
                        elif functional_status == b'TSR failure':
                            data_list['data']['samples'].append(4)
                        else:
                            data_list['data']['samples'].append(-1)
                if data_2.timestamps.tolist() == []:
                    pass
                else:
                    data_list['data']['timestamps'] = data_2.timestamps-data_2.timestamps[np.argmin(data_2.timestamps)].tolist()
                if data_3.samples.tolist() == []:
                    pass
                else:
                    for warn_enable in data_3.samples.tolist():
                        if functional_status == b'Disable':
                            data_list['warn_status']['samples'].append(0)
                        else:
                            data_list['warn_status']['samples'].append(1)
                if data_3.timestamps.tolist() == []:
                    pass
                else:
                    data_list['warn_status']['timestamps'] = data_3.timestamps-data_3.timestamps[np.argmin(data_3.timestamps)].tolist()
                if data_4.samples.tolist() == []:
                    pass
                else:
                    data_list['odometer']['samples'] = data_4.samples.tolist()
                if data_4.timestamps.tolist() == []:
                    pass
                else:
                    data_list['odometer']['timestamps'] = data_4.timestamps-data_4.timestamps[np.argmin(data_4.timestamps)].tolist()
                self.close_file()
                return data_list

                
                
    # 19
    # Rough data processing
    def task_19(self):
        signal = 'IFC_LKS_St'
        if self.mf:
            try:
                data = self.mf.get(signal)
                odometer = self.task_0()
            except:
                return False
            else:
                data_list = {'data': {'samples': [], 'timestamps': []},'odometer': {'samples': [], 'timestamps': []}}
                for run_type in data.samples.tolist():
                    if run_type == b'LKS off':
                        data_list['data']['samples'].append(-1)
                    elif run_type == b'LKS active':
                        data_list['data']['samples'].append(1)
                    else:
                        data_list['data']['samples'].append(0)
                for run_time in data.timestamps.tolist():
                    data_list['data']['timestamps'].append(run_time - data.timestamps.tolist()[0])
                data_list['odometer']['samples'] = odometer.samples.tolist()
                for odo_time in odometer.timestamps.tolist():
                    data_list['odometer']['timestamps'].append(odo_time - odometer.timestamps.tolist()[0])
                self.close_file()
                return data_list

class CreatePlot:
    def __init__(self):
        self.create_subplots()
    # Initialize canvas
    def create_subplots(self, rows=None):
        if rows:
            self.fig = make_subplots(
                    rows=rows,
                    cols=1,
                    subplot_titles=[])
        else:
            self.fig = make_subplots(
                    rows=3,
                    cols=1,
                    subplot_titles=[])
    # 通用型数据切片函数
    def split_data(self, file_data):
        temp = []
        split_list_samples = []
        split_list_timestamps = []
        # Function change record
        for i in range(len(file_data['samples'])):
            if i < len(file_data['samples'])-1:
                if file_data['samples'][i] != file_data['samples'][i+1]:
                    temp.append(i+1)
        temp.append(len(file_data['samples']))
        # Functional state segmentation
        for j in range(len(temp)):
            if j == 0:
                split_list_samples.append(file_data['samples'][:temp[j]])
                split_list_timestamps.append(file_data['timestamps'][:temp[j]])
            else:
                split_list_samples.append(file_data['samples'][temp[j-1]:temp[j]])
                split_list_timestamps.append(file_data['timestamps'][temp[j-1]:temp[j]])
        return (split_list_samples, split_list_timestamps)
    # 通用型里程信息获取函数
    def find_odometer(self, data, hpa_real):
        # {hpa_real} Value as condition
        ec_hpa_df = pd.Series(data['timestamps'])
        range_max = ec_hpa_df[ec_hpa_df >= hpa_real].min()
        range_min = ec_hpa_df[ec_hpa_df <= hpa_real].max()
        # 判断更接近哪一个
        if abs(range_max-hpa_real) < abs(range_min - hpa_real):
                return range_max
        else:
                return range_min


    # 17
    def get_data_17(self, data):
        key_list = []
        # 功能关闭和开启时间
        on_and_off_time = []

    # 18
    def get_data_18(self, data):
        key_list = []
        # 功能关闭和开启时间
        on_and_off_time = []
        # 不同模式的使用比例
        proportion_of_five_modes = []
        # 功能激活时的总行驶里程
        total_mileage_list = []
        # 驾驶时长，里程数，功能激活次数
        driving_time__mileage__function_activation_times = []
        # def func(file_data):
        #     temp = []
        #     split_list_samples = []
        #     split_list_timestamps = []
        #     # Function change record
        #     for i in range(len(file_data['samples'])):
        #         if i < len(file_data['samples'])-1:
        #             if file_data['samples'][i] != file_data['samples'][i+1]:
        #                 temp.append(i+1)
        #     temp.append(len(file_data['samples']))
        #     # Functional state segmentation
        #     for j in range(len(temp)):
        #         if j == 0:
        #             split_list_samples.append(file_data['samples'][:temp[j]])
        #             split_list_timestamps.append(file_data['timestamps'][:temp[j]])
        #         else:
        #             split_list_samples.append(file_data['samples'][temp[j-1]:temp[j]])
        #             split_list_timestamps.append(file_data['timestamps'][temp[j-1]:temp[j]])
        #     return (split_list_samples, split_list_timestamps)
        def find_odometer(data, hpa_real):
            # {hpa_real} Value as condition
            ec_hpa_df = pd.Series(data['timestamps'])
            range_max = ec_hpa_df[ec_hpa_df >= hpa_real].min()
            range_min = ec_hpa_df[ec_hpa_df <= hpa_real].max()
            # 判断更接近哪一个
            if abs(range_max-hpa_real) < abs(range_min - hpa_real):
                    return range_max
            else:
                    return range_min

        for key in data.keys():
            functional_open_status_data = data[key]['open_status']
            functional_status_data = data[key]['data']
            warn_enable_data = data[key]['warn_status']
            odometer_data = data[key]['odometer']
            key_list.append(key)
            # 功能关闭时间和开启时间
            time_of_on = 0
            time_of_off = 0
            on_and_off_data = self.split_data(functional_open_status_data)
            for i in range(len(on_and_off_data[0])):
                if 0 in on_and_off_data[0][i]:
                    time_of_off += sum(on_and_off_data[1][i])
                else:
                    time_of_on += sum(on_and_off_data[1][i])
            on_and_off_time.append([time_of_on,time_of_off])
            # 不同模式的使用比例
            pattern_1 = 0
            pattern_2 = 0
            pattern_3 = 0
            pattern_4 = 0
            pattern_5 = 0
            pattern_list = self.split_data(functional_status_data)
            functional_active_list = []
            for i in range(len(pattern_list[0])):
                if 0 in pattern_list[0][i]:
                    pattern_1 += 1
                elif 1 in pattern_list[0][i]:
                    functional_active_list.append([pattern_list[1][i][0], pattern_list[1][i][-1]])
                    pattern_2 += 1
                elif 2 in pattern_list[0][i]:
                    functional_active_list.append([pattern_list[1][i][0], pattern_list[1][i][-1]])
                    pattern_3 += 1
                elif 3 in pattern_list[0][i]:
                    functional_active_list.append([pattern_list[1][i][0], pattern_list[1][i][-1]])
                    pattern_4 += 1
                elif 4 in pattern_list[0][i]:
                    functional_active_list.append([pattern_list[1][i][0], pattern_list[1][i][-1]])
                    pattern_5 += 1
            proportion_of_five_modes.append([pattern_1, pattern_2, pattern_3, pattern_4, pattern_5])
            # 功能激活时的总行驶里程
            total_mileage = 0
            for i in functional_active_list:
                # 获取对应的时间戳
                left_data = find_odometer(odometer_data, i[0])
                right_data = find_odometer(odometer_data, i[1])
                mileage = odometer_data['samples'][odometer_data['timestamps'].tolist().index(right_data)] - odometer_data['samples'][odometer_data['timestamps'].tolist().index(left_data)]
                total_mileage += mileage
            total_mileage_list.append(total_mileage)
            # 驾驶时长，里程数， 功能激活次数
            pattern_active_sum = (pattern_2+pattern_3+pattern_4)
            driving_time = (odometer_data['timestamps'][-1] - odometer_data['timestamps'][0]) if odometer_data['timestamps'] != [] else 0
            driving_mileage = (odometer_data['samples'][-1] - odometer_data['samples'][0]) if odometer_data['timestamps'] != [] else 0
            driving_time__mileage__function_activation_times.append([driving_time, driving_mileage, pattern_active_sum])
        # 
        self.create_subplots(rows=4)
        on_and_off_time = np.array(on_and_off_time).T.tolist()
        proportion_of_five_modes = [sum(x) for x in np.array(proportion_of_five_modes).T.tolist()]
        driving_time__mileage__function_activation_times = np.array(driving_time__mileage__function_activation_times).T.tolist()
        
        print('on_and_off_time: ', on_and_off_time)
        print('proportion_of_five_modes: ', proportion_of_five_modes)
        print('driving_time__mileage__function_activation_times: ', driving_time__mileage__function_activation_times)
        print('total_mileage_list: ', total_mileage_list)

        names_1 = ['Time as on', 'Time as off']
        names_2 = ['Off', 'Fusion mode', 'Vision only mode', 'Navigation only mode', 'TSR failure']
        names_3 = ['Function activation times', 'Vehicle running time', 'Vehicle mileage']
        names_4 = ['Total mileage']
        self.plot_create_pie(names_2, proportion_of_five_modes)
        self.create_subplots(rows=3)
        self.plot_append(names_1,key_list,on_and_off_time,1)
        self.plot_append(names_3,key_list,driving_time__mileage__function_activation_times,2)
        print(total_mileage_list)
        self.plot_append_1(names_4, key_list, total_mileage_list, 3)
        self.create_plot(filename='./tesk_18/2.html')




    # 19
    def get_data_19(self,data):
        '''
        parms: {data} Data to be processed
        '''
        trace1_data = []
        trace2_data = []
        trace3_data = []
        
        keys_list = []
        # Functions for data segmentation
        def func(hpa_real):
            # {hpa_real} Value as condition
            ec_hpa_df = pd.Series(file_odometer['timestamps'])
            range_max = ec_hpa_df[ec_hpa_df >= hpa_real].min()
            range_min = ec_hpa_df[ec_hpa_df <= hpa_real].max()
            # 判断更接近哪一个
            if abs(range_max-hpa_real) < abs(range_min - hpa_real):
                    return range_max
            else:
                    return range_min
        # Data processing cycle
        for key in data.keys():
            file_data = data[key]['data']
            # Time when the function is turned off
            off_times = 0
            # Time of function activation
            open_times = 0
            temp = []
            split_list_samples = []
            split_list_timestamps = []
            # Function change record
            for i in range(len(file_data['samples'])):
                if i < len(file_data['samples'])-1:
                    if file_data['samples'][i] != file_data['samples'][i+1]:
                        temp.append(i+1)
            temp.append(len(file_data['samples']))
            # Functional state segmentation
            for j in range(len(temp)):
                if j == 0:
                    split_list_samples.append(file_data['samples'][:temp[j]])
                    split_list_timestamps.append(file_data['timestamps'][:temp[j]])
                else:
                    split_list_samples.append(file_data['samples'][temp[j-1]:temp[j]])
                    split_list_timestamps.append(file_data['timestamps'][temp[j-1]:temp[j]])
            war_times = []
            # Duration of each function
            for timestam in split_list_timestamps:
                try:
                    war_times.append(timestam[-1]-timestam[0])
                except IndexError as e:
                    war_times.append(0)
            # Record the opening and closing time of extraction function
            for index in range(len(war_times)):
                if 1 in split_list_samples[index]:
                    open_times += war_times[index]
                if -1 in split_list_samples[index]:
                    off_times += war_times[index]
            # Data summary of function closing time and opening time
            off_on_list = [off_times, open_times]
            # Function activation times
            sum_1 = 0
            for index,value in enumerate(file_data['samples']):
                if index < len(file_data['samples'])-1 and value == -1 and file_data['samples'][index+1] == 1:
                    sum_1 += 1
            file_odometer = data[key]['odometer']
            # Vehicle running time
            run_time = file_odometer['timestamps'][-1] - file_odometer['timestamps'][0]
            # Total vehicle mileage
            run_odometer = file_odometer['samples'][-1] - file_odometer['samples'][0]
            # Summary of vehicle running time, function activation times and total vehicle mileage data
            time_odometer_active = [sum_1, run_time, run_odometer]

            # Total mileage at function activation
            open_odometer = []
            odometer_times = []
            # Get function switching time point
            for index in range(len(split_list_samples)):
                if 1 in split_list_samples[index]:
                    odometer_times.append([split_list_timestamps[index][0],split_list_timestamps[index][-1]])
            # According to the time point to find the corresponding mileage and calculate
            for index in odometer_times:
                open_odometer.append(file_odometer['samples'][file_odometer['timestamps'].index(func(index[1]))] - file_odometer['samples'][file_odometer['timestamps'].index(func(index[0]))])
            # Temporary data storage
            trace1_data.append(time_odometer_active)
            trace2_data.append(off_on_list)
            trace3_data.append(sum(open_odometer) if open_odometer != [] else 0)
            # Vehicle name record
            keys_list.append(key)
        # Transformation of morphological data
        trace1_data = np.array(trace1_data).T.tolist()
        trace2_data = np.array(trace2_data).T.tolist()
        trace3_data = np.array(trace3_data).T.tolist()
        print(trace3_data)
        names = ['Function activation times', 'Vehicle running time', 'Vehicle mileage']
        self.plot_append(names,keys_list, trace1_data, 1)
        # names = ['Time when the function is turned off', 'Time of function activation']
        self.plot_append(names,keys_list, trace2_data, 2)
        names = ['Total mileage at function activation']
        self.plot_append_1(names,keys_list, trace3_data, 3)
        self.create_plot()
    
    # create pie
    def plot_create_pie(self, file_names, data):
        pyplt = py.offline.plot
        trace = [go.Pie(labels=file_names,values=data)]
        fig = go.Figure(data=trace)
        if os.path.exists('./tesk_18'):
            pass
        else:
            os.mkdir('./tesk_18')
        pyplt(fig, filename='./tesk_18/1.html')

    # Building chart objects
    def plot_append(self, file_names, keys_list, data, rows):
        '''
        parms: [
            file_names: Information name
            keys_list: Vehicle name record
            data: Processed data
            rows: Chart of data
        ]
        '''
        for index in range(len(file_names)):
            trace = go.Bar(
                name=file_names[index],
                # fill='tozeroy',
                x=keys_list,
                y=data[index]
            )
            self.fig.append_trace(trace, rows, 1)
    # One dimensional data addition
    def plot_append_1(self, file_names, keys_list, data, rows):
        '''
        parms: [
            file_names: Information name
            keys_list: Vehicle name record
            data: Processed data
            rows: Chart of data
        ]
        '''
        trace = go.Bar(
            name=file_names[0],
            # fill='tozeroy',
            x=keys_list,
            y=data
        )
        self.fig.append_trace(trace, rows, 1)
    def create_plot(self, filename=None):
        if filename:
            pltoff.plot(self.fig, filename=filename + '.html')
        else:
            filename = input('请输入要生成的文件名(html格式)：')
            pltoff.plot(self.fig, filename=filename + '.html')

# Get data file address information
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
    # Base path address
    base_file_path = 'G:/loc/szh/DA/Driving/System_APP/02_GAC/01_A18/DASy/'
    # Get data file address information
    file_list = file_path_list(base_file_path)
    all_data_list_19 = {}
    all_data_list_18 = {}
    # Mf4 read file
    i = 0
    while i < 100:
        
        i += 1
        try:
            file_path = file_list.pop()
        except IndexError as e:
            break
        else:
            file_name = file_path.split('\\')[-1].split('.')[0]
            mf = openMDF(file_path)

            # data_list = mf.task_19()
            # all_data_list_19[file_name] = data_list

            data_list = mf.task_18()
            all_data_list_18[file_name] = data_list
            print('文件：{}读取完毕， 数据存储完成，开始下一个文件'.format(file_name))

    # Input data for drawing
    cp = CreatePlot()
    # cp.get_data_19(all_data_list_19)
    cp.get_data_18(all_data_list_18)