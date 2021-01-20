"""
这个程序是实现块的header数据提取和存储为csv格式
"""

import csv
import os
from datetime import datetime
from blockchain_parser.blockchain import Blockchain

tic1 = datetime.now()
header_list=[]

for x in range(500,1300):   #更改里面的数值即可实现提取的.dat文件的范围
    tic = datetime.now()
    if x < 1000:
        blockchains = Blockchain(os.path.expanduser('/home/zhang/.bitcoin/blocks/blk00{k}.dat').format(k=x))
        for block in blockchains.get_unordered_blocks():
            result = ("%s, %s, %d, %s, %s, %s, %d, %s, %d, %s" %(block.hash, block.header.previous_block_hash, block.size, block.header.timestamp, block.header.version, block.header.merkle_root, block.n_transactions, block.header.nonce, block.header.difficulty, block.header.bits))
            result = result.split(",")
            header_list.append(result)
        # print(header_list)
        # toc = datetime.now()
        # print("第" + "%d" %x + "个dat块解析完成!" + '运行时间: %f 秒' % (toc - tic).total_seconds())
    else:
        blockchains = Blockchain(os.path.expanduser('/home/zhang/.bitcoin/blocks/blk0{k}.dat').format(k=x))
        for block in blockchains.get_unordered_blocks():
            result = ("%s, %s, %d, %s, %s, %s, %d, %s, %d, %s" %(block.hash, block.header.previous_block_hash, block.size, block.header.timestamp, block.header.version, block.header.merkle_root, block.n_transactions, block.header.nonce, block.header.difficulty, block.header.bits))
            result = result.split(",")
            header_list.append(result)
        # print(header_list)
    toc = datetime.now()
    print("第" + "%d" %x + "个dat块解析完成!" + '运行时间: %f 秒' % (toc - tic).total_seconds())

print("共有" + "%d"%len(header_list) + "区块！" )

#
try:
    with open("/home/zhang/下载/python-bitcoin-blockchain-parser-master/create_file/header00500.csv",'w',encoding='utf-8',newline='' ) as f:
        csv_write = csv.writer(f)
        csv_head = ["块哈希","前一个块","大小", "时间戳", "块头版本", "默克尔根", "交易数量", "随机数", "难度", "难度"]
        csv_write.writerow(csv_head)
        csv_write.writerows(header_list)
except:
    print("下载失败！")

toc1 = datetime.now()
print('总共运行时间: %f 秒' % (toc1 - tic1).total_seconds())





    ###区块头应该有块哈希('块哈希=%s':'block.hash')  ('时间戳=%s':'block.header.timestamp')  ('块头版本=%s':'block.header.version')  ('默克尔根=%s':'block.header.merkle_root')  ('交易数量=%d':'block.n_transactions')  ('Nonce=%s':'block.header.nonce')  ('前一个块=%s':'block.header.previous_block_hash')  ('难度=%s':'block.header.difficulty')  ('大小=%d':'block.size')  ('':'')  ('':'')