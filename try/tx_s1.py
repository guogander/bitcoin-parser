from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
import os

blockchains = Blockchain(os.path.expanduser('/home/zhang/.bitcoin/blocks/blk02291.dat'))
for blocks in blockchains.get_unordered_blocks():
    for tx in blocks.transactions:
        # result = ("%s, %s, %s, %s, %s, %s " % (
        #     blocks.hash, tx.txid, tx.n_inputs, tx.n_outputs, tx.outputs, tx.inputs))
        # print(result)


        tx_outputs = "%s" % tx.outputs
        b = tx_outputs.replace("[","").replace("]","")
        # c =b.split(",")
        # print(list(tx_outputs))
        print(b)
        print(type(b))