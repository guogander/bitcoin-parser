'''
获取最新的dat文件名
以下三个都是找出最新的dat文件,使用的方法不同
'''
import os

from blockchain_parser.blockchain import get_files
import glob  # 匹配文件的模块


# i = 0
def new_datfile1():
    file_list = []
    for name in glob.glob('/home/guoyaqun/.bitcoin/blocks/blk?????.dat'):  # blk?????.dat匹配所有的的blk.dat文件
        # i += 1
        file_name = name.split('/')  # 将得到的路径以/分割得到一个列表
        # print(file_name[-1])  #
        file_list.append(file_name[-1])  # 将此列表的最后文件既dat文件名添加进列表中
        file_list.sort()   # 将dat文件排序
    # print(file_list[-1])  #打印最后一个dat文件
    return file_list[-1]    # 返回最新的文件名
    # print("All have %d 'blk.dat' files!"%i)  # 计算有多少个blk.dat文件
# new_datfile()


def new_datfile2(path):
    file = get_files(path)
    temp = file[-1].rfind('/')
    dat_file = file[-1][temp+1:]
    return dat_file
    # print(dat_file)

def new_datfile3(path):
    path_add = os.path.split(path)
    return path_add[-1]
# 返回最新的dat绝对路径
path = '/home/guoyaqun/.bitcoin/blocks/'
def real_path():
    x = get_files(path)
    return x[-1]
# print(new_datfile2(path))