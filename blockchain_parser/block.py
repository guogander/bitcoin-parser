from .transaction import Transaction
from .block_header import BlockHeader
from .utils import format_hash, decode_varint, double_sha256


def get_block_transactions(raw_hex):
    """Given the raw hexadecimal representation of a block,
    yields the block's transactions  给定一个块的原始十六进制表示，产生该块的交易
    """
    # Skipping the header
    transaction_data = raw_hex[80:]

    # Decoding the number of transactions, offset is the size of
    # the varint (1 to 9 bytes)
    n_transactions, offset = decode_varint(transaction_data)

    for i in range(n_transactions):
        # Try from 1024 (1KiB) -> 1073741824 (1GiB) slice widths
        for j in range(0, 20):
            try:
                offset_e = offset + (1024 * 2 ** j)

                transaction = Transaction.from_hex(
                    transaction_data[offset:offset_e])
                yield transaction
                break
            except:
                continue

        # Skipping to the next transaction

        offset += transaction.size


class Block(object):
    """
    Represents a Bitcoin block, contains its header and its transactions.
    """

    def __init__(self, raw_hex, height=None):
        self.hex = raw_hex
        self._hash = None
        self._transactions = None
        self._header = None
        self._n_transactions = None
        self.size = len(raw_hex)
        self.height = height

    def __repr__(self):
        return "Block(%s)" % self.hash

    @classmethod
    def from_hex(cls, raw_hex):
        """Builds a block object from its bytes representation"""
        return cls(raw_hex)

    @property
    def hash(self):
        """Returns the block's hash (double sha256 of its 80 bytes header
        先对80个字节进行两次哈希可以得到区块的hash值，然后在使用format_hash函数以字节为单位逆序读取
        """
        if self._hash is None:
            self._hash = format_hash(double_sha256(self.hex[:80]))
        return self._hash

    @property
    def n_transactions(self):
        """Return the number of transactions contained in this block,
        it is faster to use this than to use len(block.transactions)
        as there's no need to parse all transactions to get this information
        返回此块中包含的交易数，使用它比使用len(block.transactions)因为不需要解析所有交易来获取这些信息
        """
        if self._n_transactions is None:
            self._n_transactions = decode_varint(self.hex[80:])[0]

        return self._n_transactions

    @property
    def transactions(self):
        """Returns a list of the block's transactions represented
        as Transaction objects 返回表示为事务对象的块事务的列表
        """
        if self._transactions is None:
            self._transactions = list(get_block_transactions(self.hex))

        return self._transactions

    @property
    def header(self):
        """Returns a BlockHeader object corresponding to this block
        返回与此块对应的BlockHeader对象"""
        if self._header is None:
            self._header = BlockHeader.from_hex(self.hex[:80])
        return self._header
