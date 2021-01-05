from asammdf import MDF
import json,os,time
import numpy as np
import pandas as pd


class OpenMDF:
    def __init__(self, path):
        # 构建初始化文件路径列表
        self.file_list = []
        for root,dirs,files in os.walk(path):
            for i in files:
                if i.endswith('MF4'):
                    self.file_list.append(os.path.join(root,i))
        while True:
            try:
                file_path = self.file_list.pop()
            except IndexError as e:
                break
            else:
                print(file_path)
                self.task_2(file_path)
    # 打开mf4文件
    def open_file(self,path):
        try:
            mf = MDF(path)
        except:
            pass
        else:
            return mf
    
    # 关闭mf4文件
    def close_file(self, mf:object):
        mf.close()
    # 0
    # 总里程数信息获取
    def task_0(self, mf:object):
        try:
            odometer = mf.get('ICM_TotalOdometer')
        except:
            pass
        else:
            return odometer
    # 1
    # 数据不全， 暂停
    def task_1(self, path):
        signal_left = 'BSDS_LCAWarnLeft'
        signal_right = 'BSDM_LCAWarnRight'
        signal_LCASt = 'BSDM_LCASt'
        mf = self.open_file(path)
        if mf:
            try:
                left = mf.get(signal_left)
            except:
                return False
            else:
                print(left)
            try:
                right = mf.get(signal_right)
            except:
                return False
            else:
                print(right)
            try:
                LCASt = mf.get(signal_LCASt)
            except:
                return False
            else:
                print(LCASt)
            try:
                odometer = self.task_0(mf)
            except:
                return False
            else:
                print(odometer)
            self.close_file(mf)
    # 19
    def task_2(self, path):
        signal = 'IFC_LKS_St'
        mf = self.open_file(path)
        if mf:
            try:
                data = mf.get(signal)
                odometer = self.task_0(mf)
            except:
                pass
            else:
                print(data)
                print(odometer)
            self.close_file(mf)
        else:
            print('mdf开启失败')
    # 3
    def task_3(self, path):
        pass
    # 4
    def task_4(self, path):
        pass


if __name__ == "__main__":
    new_file = OpenMDF('G:/loc/szh/DA/Driving/System_APP/02_GAC/01_A18/DASy/')

        