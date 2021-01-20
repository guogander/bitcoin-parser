from datetime import datetime
from bitcoin.core import CBlockHeader

from .utils import decode_uint32, format_hash


class BlockHeader(object):
    """Represents a block header"""

    def __init__(self, raw_hex):
        self._version = None
        self._previous_block_hash = None
        self._merkle_root = None
        self._timestamp = None
        self._bits = None
        self._nonce = None
        self._difficulty = None

        self.hex = raw_hex[:80]    #比特币区块头有80个字节长度

    def __repr__(self):
        return "BlockHeader(previous_block_hash=%s)" % self.previous_block_hash

    @classmethod
    def from_hex(cls, raw_hex):
        """Builds a BlockHeader object from its bytes representation"""
        return cls(raw_hex)

    @property
    def version(self):
        """Return the block's version 版本"""
        if self._version is None:
            self._version = decode_uint32(self.hex[:4])    #前4个字节是区块版本号
        return self._version

    @property
    def previous_block_hash(self):
        """Return the hash of the previous block"""
        if self._previous_block_hash is None:
            self._previous_block_hash = format_hash(self.hex[4:36])   #其次32个字节是父区块头哈希值
        return self._previous_block_hash

    @property
    def merkle_root(self):
        """Returns the block's merkle root 默克尔根"""
        if self._merkle_root is None:
            self._merkle_root = format_hash(self.hex[36:68])        #其次32个字节是默克尔树根哈希值
        return self._merkle_root

    @property
    def timestamp(self):
        """Returns the timestamp of the block as a UTC datetime object
        以UTC日期时间对象的形式返回块的时间戳"""
        if self._timestamp is None:
            self._timestamp = datetime.utcfromtimestamp(
                decode_uint32(self.hex[68:72])                      #其次4个字节是时间戳
            )
        return self._timestamp

    @property
    def bits(self):
        """Returns the bits (difficulty target) of the block  返回块的位（难度目标）"""
        if self._bits is None:
            self._bits = decode_uint32(self.hex[72:76])            #其次4个字节是难度目标
        return self._bits

    @property
    def nonce(self):
        """Returns the block's nonce"""
        if self._nonce is None:
            self._nonce = decode_uint32(self.hex[76:80])           #其次4个字节是Nonce
        return self._nonce

    @property
    def difficulty(self):
        """Returns the block's difficulty target as a float以浮点形式返回块的难度目标"""
        if self._difficulty is None:
            self._difficulty = CBlockHeader.calc_difficulty(self.bits)

        return self._difficulty
