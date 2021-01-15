import os

def getPath(path):
    '''
    parms: {path} Base path address
    '''
    file_list = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if i.endswith('json'):
                file_list.append(os.path.join(root,i))
    return file_list