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


import os
from blockchain_parser.blockchain import Blockchain

blockchains = Blockchain(os.path.expanduser('/home/zhang/.bitcoin/blocks/blk02291.dat'))
# blockchain = Blockchain(sys.argv[1])
for block in blockchains.get_unordered_blocks():
    for transaction in block.transactions:
        for output in transaction.outputs:
            if output.is_unknown():
                print(block.header.timestamp, output.script.value)