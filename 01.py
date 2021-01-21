import json
import os
import time
from asammdf import MDF
import numpy
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, bytes):
                return str(obj, encoding='utf-8')
            if isinstance(obj, (numpy.int_, numpy.intc, numpy.intp, numpy.int8,numpy.int16, numpy.int32, numpy.int64, numpy.uint8,numpy.uint16,numpy.uint32, numpy.uint64)):
                return int(obj)
            elif isinstance(obj, (numpy.float_, numpy.float16, numpy.float32,numpy.float64)):
                return float(obj)
            elif isinstance(obj, (numpy.ndarray,)): # add this line
                return obj.tolist() # add this line
            return json.JSONEncoder.default(self, obj)
        except UnicodeDecodeError:
            pass
def fun():
    mf = MDF('./GAC_A18_2020-06-26_15-01_11_0016.MF4')
    file_name = 'GAC_A18_2020-06-26_15-01_11_0016.json'
    signal_list = []
    data_dict = {}
    with open('./Book1.txt', 'r') as f:
        for line in f.readlines():
            signal_list.append(line[:-1])
    while True:
        try:
            signal = signal_list.pop()
        except IndexError:
            break
        else:
            try:
                data = mf.get(signal)
            except Exception:
                continue
            else:
                data_dict[signal] = {
                    'samples': data.samples.tolist(),
                    'timestamps':data.timestamps.tolist()
                }
    with open('./data.josn', 'w') as f:
        json.dump(data_dict, f, cls=MyEncoder, ensure_ascii=False)

if __name__ == "__main__":
    fun()