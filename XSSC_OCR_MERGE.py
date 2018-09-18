# -*- coding: UTF-8 -*-
from aip import AipOcr
import re
import os
config = {
    'appId': '********',
    'apiKey': '********',
    'secretKey': '********'
}

client = AipOcr(**config)

def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()

def img_to_str(image_path):
    image = get_file_content(image_path)
    result = client.basicGeneral(image)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])

def merge(folder_path,category):
    tt = open(folder_path+category+'\\test.txt', 'w')
    filedir = os.walk(folder_path + category)
    for i in filedir:
        for each_file in i[2]:
            if each_file.endswith('.png'):
                tt.write(img_to_str(i[0]+'\\'+each_file)+ '\n')
                if category == 'judge':
                    tt.write('对\n错\n')
                if category == 'select':
                    num = re.findall(r'\d+',each_file)
                    tmp = open(i[0]+'\\'+num[0]+'.txt'.format(i), 'r')
                    tt.write(tmp.read() + '\n')
                    tmp.close()
    tt.close()
if __name__=='__main__':
    merge('E:\\xsscBU\\','judge')
    merge('E:\\xsscBU\\','select')