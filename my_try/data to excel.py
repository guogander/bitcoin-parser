import pandas as pd
import numpy as np
# data = 'guoyaqun xue python!'

df=pd.DataFrame(np.random.randn(6,4),columns=list('ABCD'))

df.to_excel('/home/guoyaqun/python-bitcoin-blockchain-parser-master/my_try/list.xls')