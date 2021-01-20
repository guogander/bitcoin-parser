# Copyright (C) 2015-2016 The bitcoin-blockchain-parser developers
#
# This file is part of bitcoin-blockchain-parser.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of bitcoin-blockchain-parser, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.

from math import ceil

from .utils import decode_varint, decode_uint32, double_sha256, format_hash
from .input import Input
from .output import Output


def bip69_sort(data):
    return list(sorted(data, key=lambda t: (t[0], t[1])))


class Transaction(object):
    """Represents a bitcoin transaction"""
    """
    BTC的交易
    结构如下：
    大小(字节)  名称                      数据类型            描述
    4          version                  uint32             交易版本号
    varies     tx_in_count              uint               交易输入数量
    varies     tx_in                    tx_in              交易输入
    varies     tx_out_count             uint               交易输出数量
    varies     tx_out                   tx_out             交易输出
    4          lock_time                uint32             锁定时间
    """

    def __init__(self, raw_hex):
        self._hash = None
        self._txid = None
        self.inputs = None
        self.outputs = None
        self.all_outputs = None
        self._version = None
        self._locktime = None
        self._size = None
        self.n_inputs = 0
        self.n_outputs = 0
        self.is_segwit = False

        offset = 4
        sun = 0
        # adds basic support for segwit transactions 添加对segwit事务的基本支持
        #   - https://bitcoincore.org/en/segwit_wallet_dev/
        #   - https://en.bitcoin.it/wiki/Protocol_documentation#BlockTransactions
        if b'\x00\x01' == raw_hex[offset:offset + 2]:     #查看是否使用了隔离见证
            self.is_segwit = True
            offset += 2

        self.n_inputs, varint_size = decode_varint(raw_hex[offset:])
        offset += varint_size

        # 这里的inputs是一笔交易的输入，以列表的形式输出，具体会输出什么看input.py这个函数
        #输出的内容是一个列表，列表的内容是：Input(ff3bf716c0a1b555952090c0a858c2570b4f0a020829f731f2de1b83ff31d29a,0)
        #其中里面的64位是交易id，后面的0代表的是这个交易的第一个输出，假如是1就是第二个输出
        self.inputs = []
        for i in range(self.n_inputs):
            input = Input.from_hex(raw_hex[offset:])
            offset += input.size
            self.inputs.append(input)

        self.n_outputs, varint_size = decode_varint(raw_hex[offset:])
        offset += varint_size


        # def all_outputs(self):
        #     global offset
        #     for i in range(self.n_outputs):
        #         output = Output.from_hex(raw_hex[offset:])
        #         offset += output.size
        #         self.all_outputs += output
        #     return self.all_outputs


        self.outputs = []       #这里的outputs是交易输出的金额
        for i in range(self.n_outputs):
            output = Output.from_hex(raw_hex[offset:])
            offset += output.size
            self.outputs.append(output)

        if self.is_segwit:
            self._offset_before_tx_witnesses = offset
            for inp in self.inputs:
                tx_witnesses_n, varint_size = decode_varint(raw_hex[offset:])
                offset += varint_size
                for j in range(tx_witnesses_n):
                    component_length, varint_size = decode_varint(
                        raw_hex[offset:])
                    offset += varint_size
                    witness = raw_hex[offset:offset + component_length]
                    inp.add_witness(witness)
                    offset += component_length

        self._size = offset + 4
        self.hex = raw_hex[:self._size]

        if self._size != len(self.hex):
            raise Exception("Incomplete transaction!")

    def __repr__(self):
        return "Transaction(%s)" % self.hash

    @classmethod
    def from_hex(cls, hex):
        return cls(hex)

    @property
    def version(self):
        """Returns the transaction's version number"""
        if self._version is None:
            self._version = decode_uint32(self.hex[:4])   #前四个字节为版本
        return self._version








    @property
    def locktime(self):
        """Returns the transaction's locktime as an int 以int形式返回交易的锁定时间"""
        #lock_time是一个多意字段，表示在某个高度的Block之前或某个时间点之前该交易处于锁定态，无法收录进Block。
        #具体查看   https://blog.csdn.net/jason_cuijiahui/article/details/100612681
        if self._locktime is None:
            self._locktime = decode_uint32(self.hex[-4:])   #后四个为锁定时间
        return self._locktime

    @property
    def hash(self):
        """Returns the transaction's id. Equivalent to the hash for non SegWit transactions,
        it differs from it for SegWit ones.
        返回交易的ID。 等同于非SegWit交易的哈希，与SegWit交易的哈希不同
        """
        if self._hash is None:
            self._hash = format_hash(double_sha256(self.hex))

        return self._hash

    @property
    def size(self):
        """Returns the transactions size in bytes including the size of the
        witness data if there is any.  返回以字节为单位的事务大小，包括见证数据的大小（如果有）"""
        return self._size               #大小 (rawtx)

    @property
    def vsize(self):
        """Returns the transaction size in virtual bytes.  返回以虚拟字节为单位的事务大小。"""
        if not self.is_segwit:
            return self._size
        else:
            # the witness is the last element in a transaction before the
            # 4 byte locktime and self._offset_before_tx_witnesses is the
            # position where the witness starts
            # 见证是事务中4字节锁定时间之前的最后一个元素，self.offset_before_tx_witness是见证开始的位置
            witness_size = self._size - self._offset_before_tx_witnesses - 4

            # size of the transaction without the segwit marker (2 bytes) and the witness  没有segwit标记（2字节）和见证的交易的大小
            stripped_size = self._size - (2 + witness_size)   #基础交易大小：移除见证数据后的交易大小
            weight = stripped_size * 3 + self._size           #交易重量=基础交易大小*3+总交易大小

            # vsize is weight / 4 rounded up
            return ceil(weight / 4)  #虚拟交易大小

    #下面这个函数是我自己写的
    @property
    def weight(self):
        """返回交易的重量。"""
        if not self.is_segwit:
            weight = self._size * 4  #在这里判断是不是使用了隔离见证，加入没有使用隔离见证，那么weight = self._size * 4
            return weight
        else:
            witness_size = self._size - self._offset_before_tx_witnesses - 4

            # size of the transaction without the segwit marker (2 bytes) and the witness  没有segwit标记（2字节）和见证的交易的大小
            stripped_size = self._size - (2 + witness_size)  # 基础交易大小：移除见证数据后的交易大小
            weight = stripped_size * 3 + self._size  # 交易重量=基础交易大小*3+总交易大小
            return weight


    @property
    def txid(self):
        """Returns the transaction's id. Equivalent to the hash for non SegWit transactions,
        it differs from it for SegWit ones. """
        if self._txid is None:
            """
            # segwit transactions have two transaction ids/hashes, txid and wtxid
            # txid is a hash of all of the legacy transaction fields only
            隔离见证交易具有两个交易ID /哈希：txid和wtxid，txid仅是所有旧有交易字段的哈希
            """
            if self.is_segwit:
                txid_data = self.hex[:4] + self.hex[
                                           6:self._offset_before_tx_witnesses] + self.hex[
                                                                                 -4:]
            else:
                txid_data = self.hex
            self._txid = format_hash(double_sha256(txid_data))

        return self._txid

    def is_coinbase(self):
        """Returns whether the transaction is a coinbase transaction
        返回交易是否为coinbase交易
        """
        for input in self.inputs:
            if input.transaction_hash == "0" * 64:   #假如是64个0的话，就是coinbase交易
                return True
        return False


    # RPC是啥看这个：https://sickworm.com/?p=409
    def uses_replace_by_fee(self):
        """Returns whether the transaction opted-in for RBF"""
        # Coinbase transactions may have a sequence number that signals RBF
        # but they cannot use it as it's only enforced for non-coinbase txs
        if self.is_coinbase():
            return False

        # A transactions opts-in for RBF when having an input
        # with a sequence number < MAX_INT - 1
        for input in self.inputs:
            if input.sequence_number < 4294967294:
                return True
        return False

    def uses_bip69(self):
        """Returns whether the transaction complies to BIP-69,
        lexicographical ordering of inputs and outputs"""
        # Quick check
        if self.n_inputs == 1 and self.n_outputs == 1:
            return True

        input_keys = [
            (i.transaction_hash, i.transaction_index)
            for i in self.inputs
        ]

        if bip69_sort(input_keys) != input_keys:
            return False

        output_keys = [(o.value, o.script.value) for o in self.outputs]

        return bip69_sort(output_keys) == output_keys
