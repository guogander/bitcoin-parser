from binascii import hexlify
import hashlib
import struct   #在 Python 中跟二进制数据打交道的时候，就要用到 struct 这个模块了。struct 模块为 Python 与 C 的混合编程，处理二进制文件以及进行网络协议交互提供了便利。https://www.cnblogs.com/CHENHAOZ/articles/10457395.html


# hashlib详情  https://www.liaoxuefeng.com/wiki/897692888725344/923057313018752

def btc_ripemd160(data):
    h1 = hashlib.sha256(data).digest() #函数将使用sha256算法计算data的散列并返回二进制的值
    r160 = hashlib.new("ripemd160")    # 使用 new(name, string=”) 构造新的哈系对象;ripemd160是一个160位的hash算法.
    r160.update(h1)
    return r160.digest()

#对header进行两次hash，可以得到区块的hash值，下面的代码就是
def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()  #两次哈希并返回二进制的值


# hash字段使内部字节顺序存储；其他的值以小端序存储。
# 其中，内部字节顺序需要以字节为单位逆序读取
# data为读取的32字节的二进制数据
# 看此博客  https://blog.csdn.net/weixin_41545330/article/details/79551881
def format_hash(hash_):
    return str(hexlify(hash_[::-1]).decode("utf-8"))  # hash_[::-1]：从后往前读取


# struct.unpack用法：  https://blog.csdn.net/weiwangchao_/article/details/80395941
def decode_uint32(data):
    assert(len(data) == 4)      #
    return struct.unpack("<I", data)[0]   #unpack(fmt, string) 按照给定的格式(fmt格式化字符串(format strings))解析字节流string，返回解析出来的tuple。在这里是使用无符号整形(unsignedint)对数据进行解包，返回一个由解包数据(data )得到的一个元组(tuple)


def decode_uint64(data):
    assert(len(data) == 8)
    return struct.unpack("<Q", data)[0]  #在这里是使用unsignedlonglong对数据进行解包


#看这个博客  https://blog.csdn.net/weixin_41545330/article/details/79551881
#交易中使用可变长度整数来表示下一条数据中的字节数。对于不同的数值，存储的空间不一样。
#对于0～252的值，只占用一个字节；对于其他小于0xffffffffffffffff的值，第一个字节将成为长度标识位。
#下面代码'<H''<I''<Q'可能是存储空间，size不同的值对应不同的存储空间
#下面是用来描述个数使用的是变长整数（VarInt）
def decode_varint(data):
    assert(len(data) > 0)  #assert（断言）用于判断一个表达式，在表达式条件为 false 的时候触发异常。
    size = int(data[0])
    assert(size <= 255)

    if size < 253:
        return size, 1

    if size == 253:
        format_ = '<H'
    elif size == 254:
        format_ = '<I'
    elif size == 255:
        format_ = '<Q'
    else:
        # Should never be reached 不应该接触到
        assert 0, "unknown format_ for size : %s" % size

    size = struct.calcsize(format_)    #calcsize()计算格式字符串描述的结构的字节大小.这里是计算以上三种情况'<H','<I','<q'对应字节大小
    return struct.unpack(format_, data[1:size+1])[0], size + 1     #unpack 将字节字符串解包成为变量。
