import csv
import pandas as pd
user_info = pd.read_csv("first_tyr6.csv", iterator=True)
count = 0
for i in range(300):
    try:
        user = user_info.get_chunk(10000)
        count += user.shape[0]
    except StopIteration:
        break
print(count)