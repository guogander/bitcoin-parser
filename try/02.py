import os
import csv
from blockchain_parser.blockchain import Blockchain

# To get the blocks ordered by height, you need to provide the path of the
# `index` directory (LevelDB index) being maintained by bitcoind. It contains
# .ldb files and is present inside the `blocks` directory.
blockchains = Blockchain(os.path.expanduser('/home/zhang/.bitcoin/blocks'))
result_list=[]
for block in blockchains.get_ordered_blocks(os.path.expanduser('/home/zhang/.bitcoin/blocks/index'), start=653931, end=653800):
    # print("%d,%s,%d,%d" % (block.height, block.hash,block.n_transactions,block.size))

    result=("%d,%s,%d,%d" % (block.height, block.hash,block.n_transactions,block.size))
    result =result.split(",")
    print(result)
    result_list.append(result)

    #     print('是空的')
print(result_list)
print(len(result_list))
# with open("/home/zhang/下载/python-bitcoin-blockchain-parser-master/try/first_tyr0.csv",'w',encoding='utf-8',newline='' ) as f:
#     csv_write = csv.writer(f)
#     csv_head = ["height","block","no","size"]
#     csv_write.writerow(csv_head)
#     csv_write.writerows(result_list)