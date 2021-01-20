from find_newfile.find_new_blk import *
from blockchain_parser.blockchain import get_files
import os

path = '/home/guoyaqun/.bitcoin/blocks/'

x = get_files(path)
print('test1----->',x[-1])
# i = x[-1].rfind('/')
# print(x[-1][i+1:])
# print('test2----->',new_datfile1())
# print('test3----->',new_datfile2(path))
# x = real_path()
# print(x)

# file = os.getcwd()
# print(file)