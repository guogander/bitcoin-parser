"""
    BTC的交易输出
    结构如下：
    大小(字节)  名称                      数据类型            描述
    8          value                    int64              花费的数量，单位是聪
    1+         pk_script_size           uint               pubkey脚本中的字节数量
    varies     pk_script                char[]             花费这笔输出需要满足的条件

    https://developer.bitcoin.org/reference/transactions.html
"""
"""
这个程序是我进行交易的输出的测试，
"""

from blockchain_parser.blockchain import Blockchain,get_files,get_blocks
from blockchain_parser.block import Block
import os
from find_newfile.find_new_blk import new_datfile1


blockchain = Blockchain(os.path.expanduser('/home/guoyaqun/.bitcoin/blocks/{}'.format(new_datfile1())))
for block in blockchain.get_unordered_blocks():
    for tx in block.transactions:
        for outputno, output in enumerate(tx.outputs):
            # print("tx=%s outputno=%d type=%s value=%s" % (tx.hash, no, output.type, output.value))
            # if tx.hash == 'eee77d421df62022f45466c39298289db4423ed03108c3c391fcb23af45b4f02':
            #     print("tx=%s outputno=%d type=%s value=%s" % (tx.hash, no, output.type, output.value))

            # print("tx=%s outputno=%d type=%s value=%s" % (tx.hash, no, output.type, output.value))
            print("块哈希=%s, 交易ID=%s, 交易哈希=%s, 输出个数=%d, 输出索引=%d, 输出类型=%s, 输出金额=%s, 输出地址=%s, 输出类型=%s, 输出脚本=%s" % (
                block.hash, tx.txid, tx.hash, tx.n_outputs, outputno, output.type, output.value, output.addresses, output.type, output.script))






