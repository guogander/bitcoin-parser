

"""
这个程序是实现功能非常多的一个程序，我用来对其他的程序进行参考的。
"""

from blockchain_parser.blockchain import Blockchain,get_files,get_blocks
from blockchain_parser.block import Block
import os
from find_newfile.find_new_blk import real_path

path = '/home/guoyaqun/.bitcoin/blocks/'
blockchains = Blockchain(os.path.expanduser(get_files(path)[-1]))
for blocks in blockchains.get_unordered_blocks():
    for tx in blocks.transactions:
        for outputno, output in enumerate(tx.outputs):
    #
    #         # print("tx=%s outputno=%d type=%s value=%s" % (tx.hash, no, output.type, output.value))
    #
            print("blk=%s,n_tx=%d,txid=%s hash=%s vsize=%d  n_inputs=%d n_outputs=%d outputno=%d type=%s value=%s output_add=%s" % (
            blocks.hash,blocks.n_transactions, tx.txid, tx.hash, tx.vsize, tx.n_inputs,tx.n_outputs, outputno, output.type, output.value, output.addresses))
            # print(" txid=%s  output_value=%s output_add=%s script=%s" % (
            # tx.txid, output.value, output.addresses,output.script))
    # for block in blocks.header:
    #     print("pre_hash=%s" % block.previous_block_hash)




'''
1.  tx.txid和tx.hash在不使用隔离见证前结果是一样的，但是使用了隔离见证之后tx.txid绝对正确，tx.hash会出现错误

2.  tx.vsize是虚拟字节; tx.txid是每一笔交易的ID，具有唯一行，在使用隔离见证之后绝对正确; 
    tx.size是大小 (rawtx);
    tx.weight是交易重量 
    tx.hash是每一笔交易的哈希值，在使用隔离见证之前和tx.txid的值一样;
    tx.n_inputs是每一笔交易输入的个数; 
    tx.n_outputs是每一笔交易输出的个数; 
    tx.outputs是输出金额，以列表的形式显示出来;
    tx.inputs是输出的内容，具体看input.py;
   
        
    output.addresses是交易的输出地址；
    output.script是交易的输出脚本;
    outputno是每一笔交易输出的索引，从0开始递增; 
    output.type是输出类型(还没有搞清楚具体干啥的)；
    output.value是每一笔交易某个输出对应的输出值

3.会看到transaction.py里面的内容是交易的属性，比如交易的hash:tx.hash，交易id:tx.txid，虚拟交易大小tx.vsize，交易输入个数:tx.n_inputs 交易输出个数:tx.n_inputs，这些属性是共同的，都可以在input_test.py ooutput_test.py找得到。而具体到某一个输入输出交易的内容要在相应的input.py和output.py等程序寻找
'''


#记录一下一个问题，在9行括号里面的是output，但是可以在结果里面输出input的个数，明天试一试直接在transaction里面输出



