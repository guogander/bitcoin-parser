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

from .utils import decode_varint, decode_uint64
from .script import Script
from .address import Address


class Output(object):
    """Represents a Transaction output"""
    """
    BTC的交易输出
    结构如下：
    大小(字节)  名称                      数据类型            描述
    8          value                    int64              花费的数量，单位是聪
    1+         pk_script_size           uint               pubkey脚本中的字节数量
    varies     pk_script                char[]             花费这笔输出需要满足的条件

    https://developer.bitcoin.org/reference/transactions.html
    """

    def __init__(self, raw_hex):
        self._value = None
        self._script = None
        self._addresses = None

        script_length, varint_size = decode_varint(raw_hex[8:])
        script_start = 8 + varint_size

        self._script_hex = raw_hex[script_start:script_start+script_length]
        self.size = script_start + script_length
        self._value_hex = raw_hex[:8]

    @classmethod
    def from_hex(cls, hex_):
        return cls(hex_)

    def __repr__(self):
        # return "输出金额satoshis=%d" %  这个啥意思呢，就是假如直接调用Output这个类，就会返回self.value这个结果，比如打印tx.outputs
        return "%d" % self.value

    @property
    def value(self):
        """Returns the value of the output exprimed in satoshis 返回以satoshis为首的输出值"""
        if self._value is None:
            self._value = decode_uint64(self._value_hex)
        return self._value

    @property
    def script(self):
        """Returns the output's script as a Script object返回输出的脚本作为脚本对象"""
        #使用了Script这个类，想看具体输出什么看这个类
        if self._script is None:
            self._script = Script.from_hex(self._script_hex)
        return self._script

    @property
    def addresses(self):
        """Returns a list containinng all the addresses mentionned
        in the output's script  返回包含输出脚本中提到的所有地址的列表
        """
        #下面备注是掉的是之前的，因为显示的地址是一个列表，看着不好看，所以我尝试将列表去掉，但是怕出错，所以将原本的保留了下来
        # if self._addresses is None:
        #     self._addresses = []
        #     if self.type == "pubkey":
        #         address = Address.from_public_key(self.script.operations[0])
        #         self._addresses.append(address)
        #     elif self.type == "pubkeyhash":
        #         address = Address.from_ripemd160(self.script.operations[2])
        #         self._addresses.append(address)
        #     elif self.type == "p2sh":
        #         address = Address.from_ripemd160(self.script.operations[1],
        #                                          type="p2sh")
        #         self._addresses.append(address)
        #     elif self.type == "multisig":
        #         n = self.script.operations[-2]
        #         for operation in self.script.operations[1:1+n]:
        #             self._addresses.append(Address.from_public_key(operation))
        #     elif self.type == "p2wpkh":
        #         address = Address.from_bech32(self.script.operations[1], 0)
        #         self._addresses.append(address)
        #     elif self.type == "p2wsh":
        #         address = Address.from_bech32(self.script.operations[1], 0)
        #         self._addresses.append(address)
        #
        # return self._addresses

        #下面就是我修改的，运行了一次没有出现错误。time:2020/11/11
        if self._addresses is None:
            if self.type == "pubkey":
                self._addresses = Address.from_public_key(self.script.operations[0])
            elif self.type == "pubkeyhash":
                self._addresses = Address.from_ripemd160(self.script.operations[2])
            elif self.type == "p2sh":
                self._addresses = Address.from_ripemd160(self.script.operations[1],
                                                 type="p2sh")
            elif self.type == "multisig":
                n = self.script.operations[-2]
                for operation in self.script.operations[1:1+n]:
                    self._addresses = (Address.from_public_key(operation))
            elif self.type == "p2wpkh":
                self._addresses = Address.from_bech32(self.script.operations[1], 0)
            elif self.type == "p2wsh":
                self._addresses = Address.from_bech32(self.script.operations[1], 0)
        return self._addresses

    def is_return(self):
        return self.script.is_return()

    def is_p2sh(self):
        return self.script.is_p2sh()

    def is_pubkey(self):
        return self.script.is_pubkey()

    def is_pubkeyhash(self):
        return self.script.is_pubkeyhash()

    def is_multisig(self):
        return self.script.is_multisig()

    def is_unknown(self):
        return self.script.is_unknown()

    def is_p2wpkh(self):
        return self.script.is_p2wpkh()

    def is_p2wsh(self):
        return self.script.is_p2wsh()

    @property
    def type(self):
        """Returns the output's script type as a string
        以字符串形式返回输出的脚本类型"""
        # Fix for issue 11
        if not self.script.script.is_valid():
            return "invalid"

        if self.is_pubkeyhash():
            return "pubkeyhash"

        if self.is_pubkey():
            return "pubkey"

        if self.is_p2sh():
            return "p2sh"

        if self.is_multisig():
            return "multisig"

        if self.is_return():
            return "OP_RETURN"

        if self.is_p2wpkh():
            return "p2wpkh"

        if self.is_p2wsh():
            return "p2wsh"

        return "unknown"
