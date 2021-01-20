from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
import os
import csv
from datetime import datetime
"""
这个程序是用来输出 块-交易 的，用来连接header和输入输出的。
"""
tic1 = datetime.now()
tx_s_list=[]
for x in range(2291,2292):   #更改里面的数值即可实现提取的.dat文件的范围
    tic = datetime.now()
    if x < 1000:
        blockchains = Blockchain(os.path.expanduser('/home/zhang/.bitcoin/blocks/blk0{k}.dat').format(k=x))
        for blocks in blockchains.get_unordered_blocks():
            for tx in blocks.transactions:
                result = ("%s, %s, %s, %s, %s, %s, %s, %s, %s " % (
                    blocks.hash, tx.txid, tx.n_inputs,tx.n_outputs,tx.vsize, tx.size, tx.weight, tx.outputs, tx.inputs))
                # print(result)
                result = result.split(",")
                tx_s_list.append(result)
    else:
        blockchains = Blockchain(os.path.expanduser('/home/zhang/.bitcoin/blocks/blk0{k}.dat').format(k=x))
        for blocks in blockchains.get_unordered_blocks():
            for tx in blocks.transactions:
                result = ("%s, %s, %s, %s, %s, %s, %s, %s, %s " % (
                    blocks.hash, tx.txid, tx.n_inputs,tx.n_outputs,tx.vsize, tx.size, tx.weight, tx.outputs, tx.inputs))
                # print(result)
                result = result.split(",")
                tx_s_list.append(result)
    toc = datetime.now()
    print("第" + "%d" %x + "个dat块解析完成!" + '运行时间: %f 秒' % (toc - tic).total_seconds())

try:
    with open("/home/zhang/下载/python-bitcoin-blockchain-parser-master/create_file/tx_2291.csv",'w',encoding='utf-8',newline='' ) as f:
        csv_write = csv.writer(f)
        csv_head = ["块哈希","交易id","输入个数", "输出个数", "虚拟大小", "交易大小", "交易重量", "输出金额", "输入信息"]
        csv_write.writerow(csv_head)
        csv_write.writerows(tx_s_list)
except:
    print("下载失败！")

toc1 = datetime.now()
print('总共运行时间: %f 秒' % (toc1 - tic1).total_seconds())


'''
1.  tx.txid和tx.hash在不使用隔离见证前结果是一样的，但是使用了隔离见证之后tx.txid绝对正确，tx.hash会出现错误

2.  tx.vsize是虚拟字节; tx.txid是每一笔交易的ID，具有唯一行，在使用隔离见证之后绝对正确; 
    tx.size是大小 (rawtx);
    tx.weight是交易重量 
    tx.hash是每一笔交易的哈希值，在使用隔离见证之前和tx.txid的值一样;
    tx.n_inputs是每一笔交易输入的个数; 
    tx.n_outputs是每一笔交易输出的个数; 
    tx.outputs是输出金额，以列表的形式显示出来
    tx.inputs是该交易的输入来源，包括上个交易的交易ID和输出的索引，具体看input.py

    output.addresses是交易的输出地址；
    output.script是交易的输出脚本;
    outputno是每一笔交易输出的索引，从0开始递增; 
    output.type是输出类型(还没有搞清楚具体干啥的)；
    output.value是每一笔交易某个输出对应的输出值

3.会看到transaction.py里面的内容是交易的属性，比如交易的hash:tx.hash，交易id:tx.txid，虚拟交易大小tx.vsize，交易输入个数:tx.n_inputs 交易输出个数:tx.n_inputs，这些属性是共同的，都可以在input_test.py ooutput_test.py找得到。而具体到某一个输入输出交易的内容要在相应的input.py和output.py等程序寻找
'''

# 记录一下一个问题，在9行括号里面的是output，但是可以在结果里面输出input的个数，明天试一试直接在transaction里面输出



