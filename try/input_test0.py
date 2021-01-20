from blockchain_parser.blockchain import Blockchain,get_files,get_blocks
from blockchain_parser.block import Block
import os
"""
    BTC的交易输入
    结构如下：
    大小(字节)  名称                      数据类型            描述
    32         previous_output_hash     outpoint           前置交易hash
    4          previous_output_index    uint32             前置交易index
    varint     script_bytes             uint               解锁脚本长度
    varies     signature_script         char[]             解锁脚本
    4          sequence                 uint32             序列号

    https://developer.bitcoin.org/reference/transactions.html
    """

# blockchain = Blockchain(os.path.expanduser('/home/zhang/.bitcoin/blocks/blk02291.dat'))
blockchain = Blockchain(os.path.expanduser('/home/guoyaqun/.bitcoin/blocks/blk00000.dat'))
for block in blockchain.get_unordered_blocks():
    for tx in block.transactions:
        for inputno, input in enumerate(tx.inputs):
            print(" 交易ID=%s 输入个数=%d  输入索引=%d, 上个块哈希=%s, 上块输出索引=%d, 解锁脚本=%s, 见证=%s" % (
                   tx.txid, tx.n_inputs, inputno,  input.pre_transaction_hash, input.pre_transaction_index, input.script, input.witnesses))




