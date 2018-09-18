# -*- coding: UTF-8 -*-
import os
import hashlib
import re
def md5count(filename):
    f = open(filename,'rb')
    md5 = hashlib.md5()
    while True:
        fb = f.read(8096)
        if not fb:
            break
        md5.update(fb)
    f.close()
    return md5.hexdigest()
def del_duplicate(folder_path,category):
    md5_set = {}
    filedir = os.walk(folder_path+category)
    for i in filedir:
        for each_file in i[2]:
            if each_file.endswith('.png'):
                if md5count(i[0]+'\\'+each_file) in md5_set.values():
                    os.remove(i[0]+'\\'+each_file)
                    num = re.findall(r'\d+', each_file)
                    os.remove(i[0]+'\\'+num[0]+'.txt')
                else:
                    md5_set[each_file] = md5count(i[0]+'\\'+each_file)

if __name__=='__main__':
    del_duplicate('E:\\xsscBU\\','judge')
    del_duplicate('E:\\xsscBU\\','select')