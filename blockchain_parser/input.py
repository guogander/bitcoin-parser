from .utils import decode_varint, decode_uint32, format_hash
from .script import Script


class Input(object):
    """Represents a transaction input"""
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

    def __init__(self, raw_hex):
        self._transaction_hash = None
        self._transaction_index = None
        self._script = None
        self._sequence_number = None
        self._witnesses = []

        self._script_length, varint_length = decode_varint(raw_hex[36:])
        self._script_start = 36 + varint_length

        self.size = self._script_start + self._script_length + 4
        self.hex = raw_hex[:self.size]

    def add_witness(self, witness):
        self._witnesses.append(witness)

    @classmethod
    def from_hex(cls, hex_):
        return cls(hex_)


    #这个会被transcation.py那里的self.inputs = [] 那里用到，在程序中使用tx.inputs会跳转到transcation.py那里的self.inputs = [] 那里，然后会发现input.py这个函数，而下面这个是最终的显示，会以列表的形式显示。
    def __repr__(self):
        return "Input(%s,%d)" % (self.pre_transaction_hash, self.pre_transaction_index)   #

    @property
    def pre_transaction_hash(self):
        """Returns the hash of the transaction containing the output
        redeemed by this input 返回包含此输入赎回的输入的交易的哈希值
        啥意思呢，就是能够返回输入地址的那一笔交易（输入就是上一笔交易的输出，通过这个试着找到一笔交易的输入地址）
        例如：搜索 交易a:6e72d39e9d6f8c55a231873f74a3518f8dd4f7273a64644728f14c3813fe1957会显示它有一个输入两个输出，
        （输出地址已经能够找到，但是找不到输入的地址（经查证，比特币交易里其实是没有地址的。只有一些特定的锁定（输出）脚本对应地址）
        详情请看 https://www.chainnode.com/post/411765）
        这时候对应的transaction_hash是:766362bda5a6b899a575a6e65cd3a3fa0448d18a6e391e64b2615cbb7bc6cd00，搜索该交易哈希，
        会发现该交易有一个输入两个输出，而且其中一个输出就是交易a的输入。。。。。。。。
        所以说尝试这种方法能不能找得到一笔交易的输入地址和输出值，由于时间较紧暂且放在这里 time:10/28
        这里的哈希就是一笔交易的输出，也就是上一个交易的输出  time:11/9
        """
        if self._transaction_hash is None:
            self._transaction_hash = format_hash(self.hex[:32])   #就是上一交易的输出
        return self._transaction_hash



    @property
    def pre_transaction_index(self):
        """Returns the index of the output inside the transaction that is
        redeemed by this input 返回此输入所兑换的交易内输入的索引  啊啊啊，这个也不知道具体干啥的
        这个是上一个交易输出的索引，也就是第几个输出，从0开始。可以通过这个索引得知这笔交易的输入来源于上一笔交易输出的第几个。我让它与上面pre_transaction_hash这个函数配合就能找到一笔交易的输入地址和输入金额，但是这个过程需要在数据解析出来后进行数据处理的过程中实现（我自己想的，是因为上下两笔交易不是连续的时间发生的，所以不太可能出现在同一个块里面，甚至不再同一个.dat文件里面，但是我解析最大的目录就是.dat文件，所以我想此操作用该在数据库或者使用python对数据进行整合清理的时候进行。）。
        """
        if self._transaction_index is None:
            self._transaction_index = decode_uint32(self.hex[32:36])
        return self._transaction_index

    @property
    def sequence_number(self):
        """Returns the input's sequence number
        返回输入的序列号 我也不知道这个是干啥的
        序列号。比特币核心和几乎所有其他程序的默认值是0xffffffff。
        """
        if self._sequence_number is None:
            self._sequence_number = decode_uint32(
                self.hex[self.size-4:self.size]
            )
        return self._sequence_number

    @property
    def script(self):
        """Returns a Script object representing the redeem script
        返回表示兑换脚本的脚本对象
        """
        if self._script is None:
            end = self._script_start + self._script_length
            self._script = Script.from_hex(self.hex[self._script_start:end])
        return self._script

    @property
    def witnesses(self):
        """Return a list of witness data attached to this input, empty if non segwit
        返回附加到此输入的见证数据列表，如果不是segwit，则为空。
        我把它理解为使用了隔离见证的输入脚本，在比特比浏览器里输入脚本可以看到(witness) ，只有使用了隔离见证打交易才有
        """
        return self._witnesses
